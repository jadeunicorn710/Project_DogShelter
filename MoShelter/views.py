"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from MoShelter import app
import json
import mysql.connector as mysql
import calendar

app.secret_key = 'gatechDemo'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    msg = ''
    if 'loggedin' in session:
        return redirect(url_for('home'))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Configure DB
        config = {
          'user': 'gatechUser',
          'password': 'GatechUser33!',
          'host': 'localhost',
          'database': 'cs6400_su20_team33',
          'raise_on_warnings': True
        }

        mydb = mysql.connect(**config)
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        query = ("SELECT regularVolunteerID, volunteer_first_name, volunteer_last_name, RegularVolunteer.volunteer_email, (adminVolunteerID IS NOT NULL) isAdmin " 
                 "FROM RegularVolunteer LEFT JOIN AdminVolunteer on AdminVolunteer.volunteer_email = RegularVolunteer.volunteer_email "
                 "WHERE RegularVolunteer.volunteer_email = %s AND password = %s")
        cursor.execute(query, (username, password))
        account = cursor.fetchone()
        cursor.close()
        mydb.close()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[3]
            session['fullname'] = account[1] + ' ' + account[2]
            session['isAdmin'] = account[4]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('fullname', None)
   session.pop('isAdmin', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/')
@app.route('/home')
@app.route('/Home')
def home():
    """Renders the home page."""
    if 'loggedin' in session:
        #Configure DB
        config = {
          'user': 'gatechUser',
          'password': 'GatechUser33!',
          'host': 'localhost',
          'database': 'cs6400_su20_team33',
          'raise_on_warnings': True
        }

        mydb = mysql.connect(**config)
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        TotalSpaces = 15
        query = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(query)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum
        )
    return redirect(url_for('login'))

@app.route('/DogDetail')
@app.route('/dogdetail')
def dogDetails():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        #Configure DB
        config = {
          'user': 'gatechUser',
          'password': 'GatechUser33!',
          'host': 'localhost',
          'database': 'cs6400_su20_team33',
          'raise_on_warnings': True
        }

        mydb = mysql.connect(**config)
        dogId = request.args.get('dogId')
        cursor = mydb.cursor(buffered=True)
        queryBreeds = ("SELECT breed_name FROM Breed")
        cursor.execute(queryBreeds)
        breednames = cursor.fetchall()
        query = ("SELECT Dog.dog_id, dog_name, sex, alteration_status, MicrochipId.value,\
        GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name,\
        dob, dog.surrender_date, dog.surrender_reason, Round(((DATEDIFF(CURDATE(), Dog.dob)) / 365.25 *12) + 0E0, 0) AS age_in_months,\
        surrendered_by_animal_control, volunteer_email, if(Dog.alteration_status = false OR value IS NULL, False , True) AS adoptabilityStatus, \
        if(Dog.application_number IS NULL, False , True) AS isAdopted, description \
        FROM Dog \
        LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id \
        INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id \
        WHERE Dog.dog_id = %s Group by Dog.dog_id")
        cursor.execute(query, (dogId,))
        dogDetails = cursor.fetchone()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]
        cursor.execute("SELECT ROUND(COALESCE(SUM(expense_amount),0),2) AS total_expenses FROM Expense WHERE dog_id= %s", (dogId,))
        totalExpense = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'dogDetail.html',
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        dogDetails = dogDetails,
        breednames = breednames,
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum,
        totalExpense = totalExpense
        )
    return redirect(url_for('login'))


@app.route('/AddAdoptionApplication')
@app.route('/addadoptionapplication')
def addAdoptionApplication():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        #Configure DB
        config = {
          'user': 'gatechUser',
          'password': 'GatechUser33!',
          'host': 'localhost',
          'database': 'cs6400_su20_team33',
          'raise_on_warnings': True
        }

        mydb = mysql.connect(**config)
        dogId = request.args.get('dogId')
        cursor = mydb.cursor(buffered=True)
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'addAdoptionApp.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum
        )
    return redirect(url_for('login'))

@app.route('/AddDog')
@app.route('/addDog')
def addDog():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        config = {
          'user': 'gatechUser',
          'password': 'GatechUser33!',
          'host': 'localhost',
          'database': 'cs6400_su20_team33',
          'raise_on_warnings': True
        }

        mydb = mysql.connect(**config)
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        query = ("SELECT breed_name FROM Breed")
        cursor.execute(query)
        breednames = cursor.fetchall()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'addDog.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        breednames = breednames,
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum
        )
    return redirect(url_for('login'))

@app.route('/ViewAdoptionApplication')
@app.route('/viewadoptionapplication')
def viewAdoptionApplication():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        #Configure DB
        config = {
          'user': 'gatechUser',
          'password': 'GatechUser33!',
          'host': 'localhost',
          'database': 'cs6400_su20_team33',
          'raise_on_warnings': True
        }

        mydb = mysql.connect(**config)
        dogId = request.args.get('dogId')
        cursor = mydb.cursor(buffered=True)
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'viewAllAdoptionApps.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum
        )
    return redirect(url_for('login'))

@app.route('/AddAdoption')
@app.route('/addAdoption')
def addAdoption():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        config = {
        'user': 'gatechUser',
        'password': 'GatechUser33!',
        'host': 'localhost',
        'database': 'cs6400_su20_team33',
        'raise_on_warnings': True
        }
        dogId = request.args.get('dogId')
        dogName = request.args.get('dogName')
        mydb = mysql.connect(**config)
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        queryDogAdoptionFee= ("SELECT IF (surrendered_by_animal_control, Round(0.15 * SUM(expense_amount),2),Round(1.15 * SUM(expense_amount),2)) AS adoption_fee "
                              "FROM Dog INNER JOIN Expense ON Dog.dog_id = Expense.dog_id "
                              "WHERE Dog.dog_id= %s")
        cursor.execute(queryDogAdoptionFee,(dogId,))
        adoptionFee = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'AddAdoption.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum,
        adoptionFee = adoptionFee,
        dogId = dogId,
        dogName = dogName
        )
    return redirect(url_for('login'))

@app.route('/AddExpenses')
@app.route('/addexpenses')
def addExpenses():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        dogId = request.args.get('dogId')
        dogName = request.args.get('dogName')
        config = {
        'user': 'gatechUser',
        'password': 'GatechUser33!',
        'host': 'localhost',
        'database': 'cs6400_su20_team33',
        'raise_on_warnings': True
        }
        mydb = mysql.connect(**config)
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        query = ("SELECT vendor_name FROM Vendor")
        cursor.execute(query)
        vendornames = cursor.fetchall()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
            'addExpense.html',
            year=datetime.now().year,
            username=session['username'],
            fullname=session['fullname'],
            isAdmin = session['isAdmin'],
            vendors = vendornames,
            availableSpaces = availableSpaces,
            pendingRevsNum = pendingRevsNum,
            dogId = dogId,
            dogName = dogName
        )
    return redirect(url_for('login'))


# Renders the animal control report page
@app.route('/AnimalControlReport')
@app.route('/animalcontrolreport')
def viewAnimalControlReport():
    if 'loggedin' in session:
        #Configure DB
        config = {
          'user': 'gatechUser',
          'password': 'GatechUser33!',
          'host': 'localhost',
          'database': 'cs6400_su20_team33',
          'raise_on_warnings': True
        }

        mydb = mysql.connect(**config)

        # Query for surrender summary
        mycursor_s = mydb.cursor(buffered=True)
        mycursor_s.reset()
        query_s = ("SELECT m.month, dognum\
            FROM (SELECT 1 as month UNION ALL\
            SELECT 2 UNION ALL\
            SELECT 3 UNION ALL\
            SELECT 4 UNION ALL\
            SELECT 5 UNION ALL\
            SELECT 6 UNION ALL\
            SELECT 7 UNION ALL\
            SELECT 8 UNION ALL\
            SELECT 9 UNION ALL\
            SELECT 10 UNION ALL\
            SELECT 11 UNION ALL\
            SELECT 12\
            ) m\
            LEFT JOIN (SELECT MONTH(Dog.surrender_date) month, \
            COUNT(DISTINCT(Dog.dog_id)) AS dognum\
            FROM Dog\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(NOW(), '%Y-%m-%d 23:59:59')\
            GROUP BY month) n ON n.month = m.month\
            WHERE m.month BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%m')\
            AND DATE_FORMAT(NOW(), '%m')\
            GROUP BY m.month\
            ORDER BY m.month DESC")
        mycursor_s.execute(query_s)
        myresult_s = mycursor_s.fetchall()
        mycursor_s.close()


        # Query for expense summary
        mycursor_e = mydb.cursor(buffered=True)
        mycursor_e.reset()
        query_e = ("SELECT m.month, ROUND(total_monthly_expenses_acs_adp,2)\
            FROM (SELECT 1 as month UNION ALL\
            SELECT 2 UNION ALL\
            SELECT 3 UNION ALL\
            SELECT 4 UNION ALL\
            SELECT 5 UNION ALL\
            SELECT 6 UNION ALL\
            SELECT 7 UNION ALL\
            SELECT 8 UNION ALL\
            SELECT 9 UNION ALL\
            SELECT 10 UNION ALL\
            SELECT 11 UNION ALL\
            SELECT 12\
            ) m\
            LEFT JOIN (SELECT MONTH(ApprovedApplication.adoption_date) month, \
            SUM(Expense.expense_amount) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(NOW(), '%Y-%m-%d 23:59:59')\
            GROUP BY month) n ON n.month = m.month\
            WHERE m.month BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%m')\
            AND DATE_FORMAT(NOW(), '%m')\
            GROUP BY m.month\
            ORDER BY m.month DESC")
        mycursor_e.execute(query_e)
        myresult_e = mycursor_e.fetchall()
        mycursor_e.close()

        # Query for rescue summary
        mycursor_r = mydb.cursor(buffered=True)
        mycursor_r.reset()
        query_r = ("SELECT m.month, num_of_acs_adp_60res​\
            FROM (SELECT 1 as month UNION ALL\
            SELECT 2 UNION ALL\
            SELECT 3 UNION ALL\
            SELECT 4 UNION ALL\
            SELECT 5 UNION ALL\
            SELECT 6 UNION ALL\
            SELECT 7 UNION ALL\
            SELECT 8 UNION ALL\
            SELECT 9 UNION ALL\
            SELECT 10 UNION ALL\
            SELECT 11 UNION ALL\
            SELECT 12\
            ) m\
            LEFT JOIN (SELECT MONTH(ApprovedApplication.adoption_date) month, \
            COUNT(DISTINCT(Dog.dog_id)) AS num_of_acs_adp_60res​\
            FROM Dog\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(NOW(), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY month) n ON n.month = m.month\
            WHERE m.month BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%m')\
            AND DATE_FORMAT(NOW(), '%m')\
            GROUP BY m.month\
            ORDER BY m.month DESC")
        mycursor_r.execute(query_r)
        myresult_r = mycursor_r.fetchall()
        mycursor_r.close()

        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()

        mydb.close()

        return render_template(
        'animalControlReport.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum,
        # Current month
        month_s1=calendar.month_name[myresult_s[0][0]],
        dog_s1=myresult_s[0][1],
        month_e1=calendar.month_name[myresult_e[0][0]],
        dog_e1=myresult_e[0][1],
        month_r1=calendar.month_name[myresult_r[0][0]],
        dog_r1=myresult_r[0][1],
        # Current month-1
        month_s2=calendar.month_name[myresult_s[1][0]],
        dog_s2=myresult_s[1][1],
        month_e2=calendar.month_name[myresult_e[1][0]],
        dog_e2=myresult_e[1][1],
        month_r2=calendar.month_name[myresult_r[1][0]],
        dog_r2=myresult_r[1][1],
        # Current month-2
        month_s3=calendar.month_name[myresult_s[2][0]],
        dog_s3=myresult_s[2][1],
        month_e3=calendar.month_name[myresult_e[2][0]],
        dog_e3=myresult_e[2][1],
        month_r3=calendar.month_name[myresult_r[2][0]],
        dog_r3=myresult_r[2][1],
        # Current month-3
        month_s4=calendar.month_name[myresult_s[3][0]],
        dog_s4=myresult_s[3][1],
        month_e4=calendar.month_name[myresult_e[3][0]],
        dog_e4=myresult_e[3][1],
        month_r4=calendar.month_name[myresult_r[3][0]],
        dog_r4=myresult_r[3][1],
        # Current month-4
        month_s5=calendar.month_name[myresult_s[4][0]],
        dog_s5=myresult_s[4][1],
        month_e5=calendar.month_name[myresult_e[4][0]],
        dog_e5=myresult_e[4][1],
        month_r5=calendar.month_name[myresult_r[4][0]],
        dog_r5=myresult_r[4][1],
        # Current month-5
        month_s6=calendar.month_name[myresult_s[5][0]],
        dog_s6=myresult_s[5][1],
        month_e6=calendar.month_name[myresult_e[5][0]],
        dog_e6=myresult_e[5][1],
        month_r6=calendar.month_name[myresult_r[5][0]],
        dog_r6=myresult_r[5][1],
        # Current month-6
        month_s7=calendar.month_name[myresult_s[6][0]],
        dog_s7=myresult_s[6][1],
        month_e7=calendar.month_name[myresult_e[6][0]],
        dog_e7=myresult_e[6][1],
        month_r7=calendar.month_name[myresult_r[6][0]],
        dog_r7=myresult_r[6][1],
        )
    return redirect(url_for('login'))


# Renders the expense analysis report page
@app.route('/ViewExpenseAnalysis')
@app.route('/viewexpenseanalysis')
def viewExpenseAnalysisReport():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        config = {
        'user': 'gatechUser',
        'password': 'GatechUser33!',
        'host': 'localhost',
        'database': 'cs6400_su20_team33',
        'raise_on_warnings': True
        }
        mydb = mysql.connect(**config)
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'expenseAnalysisReport.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum
        )
    return redirect(url_for('login'))


# Renders the volunteer lookup report page
@app.route('/ViewVolunteerLookup')
@app.route('/viewvolunteerlookup')
def viewVolunteerLookupReport():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        config = {
        'user': 'gatechUser',
        'password': 'GatechUser33!',
        'host': 'localhost',
        'database': 'cs6400_su20_team33',
        'raise_on_warnings': True
        }
        mydb = mysql.connect(**config)
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'volunteerLookupReport.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum
        )
    return redirect(url_for('login'))

# Renders the monthly adoption report page
@app.route('/ViewMonthlyAdoption')
@app.route('/viewmonthlyadoption')
def viewMonthlyAdoptionReport():
    # here we want to get the value of user (i.e. ?user=some-value)
    if 'loggedin' in session:
        config = {
        'user': 'gatechUser',
        'password': 'GatechUser33!',
        'host': 'localhost',
        'database': 'cs6400_su20_team33',
        'raise_on_warnings': True
        }
        mydb = mysql.connect(**config)
        cursor = mydb.cursor(buffered=True)
        cursor.reset()
        TotalSpaces = 15
        queryAvailableSpaces = ("SELECT (" + str(TotalSpaces) +" - COUNT(Dog.dog_id)) AS available_spaces FROM Dog WHERE Dog.application_number IS NULL")
        cursor.execute(queryAvailableSpaces)
        availableSpaces = cursor.fetchone()[0]

        #Get # of Pending Forms
        queryNumPending = ("SELECT Count(app.application_number) FROM Applicant Person NATURAL JOIN AdoptionApplication App \
            WHERE \
            NOT EXISTS (\
    	        SELECT 1 FROM ApprovedApplication WHERE \
        		application_number = App.application_number \
            )\
            AND \
            NOT EXISTS (\
    	        SELECT 1 FROM RejectedApplication WHERE \
        		application_number = App.application_number \
            )")
        cursor.execute(queryNumPending)
        pendingRevsNum = cursor.fetchone()[0]

        cursor.close()
        mydb.close()
        return render_template(
        'monthlyAdoptionReport.html',
        year=datetime.now().year,
        username=session['username'],
        fullname=session['fullname'],
        isAdmin = session['isAdmin'],
        availableSpaces = availableSpaces,
        pendingRevsNum = pendingRevsNum
        )
    return redirect(url_for('login'))