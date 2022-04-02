from flask import render_template, flash, redirect, url_for, request
from MoShelter import app
import mysql.connector as mysql
import json


# Define function to get the detailed animal control report for current month
@app.route('/Report/GetAnimalControlReport1', methods=['GET'])
def api_Get_Animal_Control_Report_1():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.args.get('type')
    query1 = None
    # Get the detailed surrender information for current month
    if type == "surrender":
        query1 = ("SELECT MONTH(Dog.surrender_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 0 MONTH, '%Y-%m-01 00:00:00') \
            AND DATE_FORMAT(NOW(), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, Dog.dog_id ASC")
    # Get the detailed expense information for current month
    elif type == "expense":
        query1 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name, \
            SUM(DISTINCT(Expense.expense_amount)) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 0 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(NOW(), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, SUM(DISTINCT(Expense.expense_amount)) DESC")
    # Get the detailed rescue information for current month
    else:
        query1 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, MicrochipId.value, \
            GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name, \
            DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) AS days_in_rescue\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 0 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(NOW(), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, days_in_rescue DESC, Dog.dog_id DESC")
    mycursor1 = mydb.cursor(buffered=True)
    mycursor1.reset()
    mycursor1.execute(query1)
    myresult1 = mycursor1.fetchall()
    mycursor1.close()
    mydb.close()
    animalcontrolreportVals1 = convertTupleToJsonFormat(myresult1)
    return animalcontrolreportVals1

# Define function to get the detailed animal control report for current month -1
@app.route('/Report/GetAnimalControlReport2', methods=['GET'])
def api_Get_Animal_Control_Report_2():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.args.get('type')
    query2 = None
    # Get the detailed surrender information for current month -1
    if type == "surrender":
        query2 = ("SELECT MONTH(Dog.surrender_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 1 MONTH, '%Y-%m-01 00:00:00') \
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, Dog.dog_id ASC")
    # Get the detailed expense information for current month -1
    elif type == "expense":
        query2 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name, \
            ROUND(SUM(DISTINCT(Expense.expense_amount)),2) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 1 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, SUM(DISTINCT(Expense.expense_amount)) DESC")
    # Get the detailed rescue information for current month -1
    elif type == "rescue":
        query2 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, MicrochipId.value, \
            GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name, \
            DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) AS days_in_rescue\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 1 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, days_in_rescue DESC, Dog.dog_id DESC")
    mycursor2 = mydb.cursor(buffered=True)
    mycursor2.reset()
    mycursor2.execute(query2)
    myresult2 = mycursor2.fetchall()
    mycursor2.close()
    mydb.close()
    animalcontrolreportVals2 = convertTupleToJsonFormat(myresult2)
    return animalcontrolreportVals2

# Define function to get the detailed animal control report for current month -2
@app.route('/Report/GetAnimalControlReport3', methods=['GET'])
def api_Get_Animal_Control_Report_3():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.args.get('type')
    query3 = None
    # Get the detailed surrender information for current month -2
    if type == "surrender":
        query3 = ("SELECT MONTH(Dog.surrender_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 2 MONTH, '%Y-%m-01 00:00:00') \
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 2 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, Dog.dog_id ASC")
    # Get the detailed expense information for current month -2
    elif type == "expense":
        query3 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name, \
            ROUND(SUM(DISTINCT(Expense.expense_amount)),2) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 2 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 2 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, SUM(DISTINCT(Expense.expense_amount)) DESC")
    # Get the detailed rescue information for current month -2
    elif type == "rescue":
        query3 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, MicrochipId.value, \
            GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name, \
            DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) AS days_in_rescue\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 2 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 2 MONTH), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, days_in_rescue DESC, Dog.dog_id DESC")
    mycursor3 = mydb.cursor(buffered=True)
    mycursor3.reset()
    mycursor3.execute(query3)
    myresult3 = mycursor3.fetchall()
    mycursor3.close()
    mydb.close()
    animalcontrolreportVals3 = convertTupleToJsonFormat(myresult3)
    return animalcontrolreportVals3

# Define function to get the detailed animal control report for current month -3
@app.route('/Report/GetAnimalControlReport4', methods=['GET'])
def api_Get_Animal_Control_Report_4():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.args.get('type')
    query4 = None
    # Get the detailed surrender information for current month -3
    if type == "surrender":
        query4 = ("SELECT MONTH(Dog.surrender_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 3 MONTH, '%Y-%m-01 00:00:00') \
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 3 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, Dog.dog_id ASC")
    # Get the detailed expense information for current month -3
    elif type == "expense":
        query4 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name, \
            ROUND(SUM(DISTINCT(Expense.expense_amount)),2) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 3 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 3 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, SUM(DISTINCT(Expense.expense_amount)) DESC")
    # Get the detailed rescue information for current month -3
    elif type == "rescue":
        query4 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, MicrochipId.value, \
            GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name, \
            DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) AS days_in_rescue\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 3 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 3 MONTH), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, days_in_rescue DESC, Dog.dog_id DESC")
    mycursor4 = mydb.cursor(buffered=True)
    mycursor4.reset()
    mycursor4.execute(query4)
    myresult4 = mycursor4.fetchall()
    mycursor4.close()
    mydb.close()
    animalcontrolreportVals4 = convertTupleToJsonFormat(myresult4)
    return animalcontrolreportVals4

# Define function to get the detailed animal control report for current month -4
@app.route('/Report/GetAnimalControlReport5', methods=['GET'])
def api_Get_Animal_Control_Report_5():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.args.get('type')
    query5 = None
    # Get the detailed surrender information for current month -4
    if type == "surrender":
        query5 = ("SELECT MONTH(Dog.surrender_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 4 MONTH, '%Y-%m-01 00:00:00') \
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 4 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, Dog.dog_id ASC")
    # Get the detailed expense information for current month -4
    elif type == "expense":
        query5 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name, \
            ROUND(SUM(DISTINCT(Expense.expense_amount)),2) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 4 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 4 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, SUM(DISTINCT(Expense.expense_amount)) DESC")
    # Get the detailed rescue information for current month -4
    elif type == "rescue":
        query5 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, MicrochipId.value, \
            GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name, \
            DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) AS days_in_rescue\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 4 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 4 MONTH), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, days_in_rescue DESC, Dog.dog_id DESC")
    mycursor5 = mydb.cursor(buffered=True)
    mycursor5.reset()
    mycursor5.execute(query5)
    myresult5 = mycursor5.fetchall()
    mycursor5.close()
    mydb.close()
    animalcontrolreportVals5 = convertTupleToJsonFormat(myresult5)
    return animalcontrolreportVals5

# Define function to get the detailed animal control report for current month -5
@app.route('/Report/GetAnimalControlReport6', methods=['GET'])
def api_Get_Animal_Control_Report_6():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.args.get('type')
    query6 = None
    # Get the detailed surrender information for current month -5
    if type == "surrender":
        query6 = ("SELECT MONTH(Dog.surrender_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 5 MONTH, '%Y-%m-01 00:00:00') \
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 5 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, Dog.dog_id ASC")
    # Get the detailed expense information for current month -5
    elif type == "expense":
        query6 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name, \
            ROUND(SUM(DISTINCT(Expense.expense_amount)),2) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 5 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 5 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, SUM(DISTINCT(Expense.expense_amount)) DESC")
    # Get the detailed rescue information for current month -5
    elif type == "rescue":
        query6 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, MicrochipId.value, \
            GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name, \
            DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) AS days_in_rescue\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 5 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 5 MONTH), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, days_in_rescue DESC, Dog.dog_id DESC")
    mycursor6 = mydb.cursor(buffered=True)
    mycursor6.reset()
    mycursor6.execute(query6)
    myresult6 = mycursor6.fetchall()
    mycursor6.close()
    mydb.close()
    animalcontrolreportVals6 = convertTupleToJsonFormat(myresult6)
    return animalcontrolreportVals6

# Define function to get the detailed animal control report for current month -6
@app.route('/Report/GetAnimalControlReport7', methods=['GET'])
def api_Get_Animal_Control_Report_7():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.args.get('type')
    query7 = None
    # Get the detailed surrender information for current month -6
    if type == "surrender":
        query7 = ("SELECT MONTH(Dog.surrender_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            WHERE Dog.surrendered_by_animal_control=True AND Dog.surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%Y-%m-01 00:00:00') \
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 6 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, Dog.dog_id ASC")
    # Get the detailed expense information for current month -6
    elif type == "expense":
        query7 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, \
            MicrochipId.value, GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name, \
            ROUND(SUM(DISTINCT(Expense.expense_amount)),2) AS total_monthly_expenses_acs_adp\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 6 MONTH), '%Y-%m-%d 23:59:59')\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, SUM(DISTINCT(Expense.expense_amount)) DESC")
    # Get the detailed rescue information for current month -6
    elif type == "rescue":
        query7 = ("SELECT MONTH(ApprovedApplication.adoption_date) month, Dog.dog_id, sex, alteration_status, surrender_date, MicrochipId.value, \
            GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/') As breed_name, \
            DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) AS days_in_rescue\
            FROM Dog\
            LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
            INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
            INNER JOIN ApprovedApplication ON Dog.application_number = ApprovedApplication.application_number\
            WHERE Dog.surrendered_by_animal_control=True AND (Dog.application_number IS NOT NULL) \
            AND ApprovedApplication.adoption_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 6 MONTH, '%Y-%m-01 00:00:00')\
            AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 6 MONTH), '%Y-%m-%d 23:59:59') AND DATEDIFF(ApprovedApplication.adoption_date, Dog.surrender_date) >59\
            GROUP BY Dog.dog_id\
            ORDER BY month DESC, days_in_rescue DESC, Dog.dog_id DESC")
    mycursor7 = mydb.cursor(buffered=True)
    mycursor7.reset()
    mycursor7.execute(query7)
    myresult7 = mycursor7.fetchall()
    mycursor7.close()
    mydb.close()
    animalcontrolreportVals7 = convertTupleToJsonFormat(myresult7)
    return animalcontrolreportVals7


def convertTupleToJsonFormat(data):
    objectArray=[]
    for datapoint in data:
        valuesArray = []
        for i in range(len(datapoint)):
            valuesArray.append(datapoint[i])
        objectArray.append(valuesArray)
    jsonDTFormat = {"data" : objectArray }
    return (json.dumps(jsonDTFormat, default=str))