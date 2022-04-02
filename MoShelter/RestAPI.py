from flask import render_template, flash, redirect, url_for, request
from MoShelter import app
import mysql.connector as mysql
import json


@app.route('/restApi/Dog/GetDashboard', methods=['GET'])
def api_Get_Dashboard():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    mycursor.execute("SELECT Dog.dog_id, dog_name, sex, alteration_status, MicrochipId.value,\
        GROUP_CONCAT(DISTINCT breed_name Order by breed_name ASC SEPARATOR '/')  As breed_name,\
        Round(((DATEDIFF(CURDATE(), Dog.dob)) / 365.25 *12) + 0E0,0) AS age_in_months,\
        if(Dog.alteration_status = false OR value IS NULL, False , True) AS adoptabilityStatus\
        FROM Dog\
        LEFT JOIN MicrochipId ON Dog.dog_id = MicrochipId.dog_id\
        INNER JOIN AssignedTo ON Dog.dog_id = AssignedTo.dog_id\
        WHERE Dog.application_number IS NULL\
        Group by Dog.dog_id\
        ORDER BY Dog.surrender_date ASC")
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    dashboardVals = convertTupleToJsonFormat(myresult)
    return (dashboardVals)

@app.route('/restApi/Dog/GetExpenses', methods=['GET'])
def api_Get_GetExpenses():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }
    dogId = request.args.get('dogId')
    mydb = mysql.connect(**config)
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    mycursor.execute("SELECT date_of_expense, vendor_name, expense_amount, optional_description FROM expense WHERE dog_id = %s ORDER BY date_of_expense DESC", (dogId,))
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    dashboardVals = convertTupleToJsonFormat(myresult)
    return (dashboardVals)

@app.route('/restApi/Dog/CompareDogName', methods=['GET'])
def api_Get_DogNameComparison():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    dogName = request.args.get('name')
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    query = ("SELECT LOWER(dog_name) \
        FROM Dog WHERE LOWER(Dog.dog_name) =  LOWER(%s)")
    mycursor.execute(query, (dogName,))
    myresult = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if myresult != None:
        jsonPythonStruct = {
          "Name": myresult[0]
        }
        return(json.dumps(jsonPythonStruct))
    return json.dumps(None)

@app.route('/restApi/Dog/CompareMicroChip', methods=['GET'])
def api_Get_MicroChipComparison():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    microchipid = request.args.get('name')
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    query = ("SELECT LOWER(value) \
        FROM Microchipid WHERE LOWER(Microchipid.value) =  LOWER(%s)")
    mycursor.execute(query, (microchipid,))
    myresult = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if myresult != None:
        jsonPythonStruct = {
          "Name": myresult[0]
        }
        return(json.dumps(jsonPythonStruct))
    return json.dumps(None)

@app.route('/restApi/Application/GetApplicantInfoForAdoption', methods=['GET'])
def api_Get_Applicant_For_Adoption():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    nameGiven = request.args.get('name')
    nameString = {'name': '%'+nameGiven+'%'}
    mydb = mysql.connect(**config)
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    query = ("SELECT AdoptionApplication.application_date, ParentApproved.application_number, Applicant.applicant_first_name, Applicant.applicant_last_name, "
            "AdoptionApplication.co_applicant_first_name, AdoptionApplication.co_applicant_last_name, Applicant.applicant_email, Applicant.phone_number,"
            "Applicant.street, Applicant.city, Applicant.state, Applicant.zip_code "
            "FROM ApprovedApplication ParentApproved " 
            "INNER JOIN Applicant ON Applicant.applicant_email = ParentApproved.applicant_email "
            "INNER JOIN AdoptionApplication ON AdoptionApplication.application_number = ParentApproved.application_number "
            "WHERE (LOWER(Applicant.applicant_last_name) LIKE LOWER(%(name)s) "
            "OR LOWER(AdoptionApplication.co_applicant_last_name) LIKE LOWER(%(name)s)) AND ParentApproved.adoption_date IS NULL "
            "AND not exists(select 1 from ApprovedApplication ChildApproved where ChildApproved.applicant_email = ParentApproved.applicant_email and ChildApproved.application_number > ParentApproved.application_number ORDER BY application_date ASC)")
    mycursor.execute(query, nameString)
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    dashboardVals = convertTupleToJsonFormat(myresult)
    return (dashboardVals)
  


@app.route('/restApi/Application/GetApplicantInfo', methods=['GET'])
def api_Get_Email_Validation():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    applicantEmail = request.args.get('email')
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    query = ("SELECT applicant_first_name, applicant_last_name, street, city, state, zip_code, phone_number, LOWER(applicant_email) \
        FROM Applicant WHERE LOWER(Applicant.applicant_email) =  LOWER(%s)")
    mycursor.execute(query, (applicantEmail,))
    myresult = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if myresult != None:
        jsonPythonStruct = {
          "FirstName": myresult[0],
          "LastName": myresult[1],
          "Street": myresult[2],
          "City": myresult[3],
          "State": myresult[4],
          "ZipCode": myresult[5],
          "Phone": myresult[6],
          "Email": myresult[7]
        }
        return(json.dumps(jsonPythonStruct))
    return json.dumps(None)

@app.route('/restApi/Application/GetApplications', methods=['GET'])
def api_Get_All_Applications():
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
    query = None
    if type == "approved":
        query = ("SELECT App.application_date, App.application_number, person.applicant_first_name, person.applicant_last_name, person.applicant_email, person.phone_number, \
            person.street, person.city, person.state, person.zip_code, App.co_applicant_first_name, App.co_applicant_last_name FROM Applicant Person \
            NATURAL JOIN AdoptionApplication App \
            INNER JOIN ApprovedApplication ApprvApp ON App.application_number = ApprvApp.application_number WHERE ApprvApp.adoption_date IS NULL")
    elif type == "rejected":
        query = ("SELECT App.application_date, App.application_number, person.applicant_first_name, person.applicant_last_name, person.applicant_email, person.phone_number, \
            person.street, person.city, person.state, person.zip_code, App.co_applicant_first_name, App.co_applicant_last_name FROM Applicant Person \
            NATURAL JOIN AdoptionApplication App \
            INNER JOIN RejectedApplication RejApp ON App.application_number = RejApp.application_number")
    else:
        query = ("SELECT App.application_date, app.application_number, person.applicant_first_name, person.applicant_last_name, person.applicant_email, person.phone_number, \
            person.street, person.city, person.state, person.zip_code, App.co_applicant_first_name, App.co_applicant_last_name FROM Applicant Person NATURAL JOIN AdoptionApplication App \
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
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    dashboardVals = convertTupleToJsonFormat(myresult)
    return dashboardVals


@app.route('/restApi/Application/AddApplication', methods=['POST'])
def api_Post_Add_Application():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    dateList = list(request.form['date'])
    dateList[2] = ','
    dateList[5] = ','
    dateString = "".join(dateList)
    applicantInfo = {
        'appEmail': request.form['email'],
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'phone': request.form['phone'],
        'zipcode': request.form['zipcode'],
        'street': request.form['street'],
        'city': request.form['city'],
        'state': request.form['state'],
        'coFName': request.form['co_first_name'],
        'coLName': request.form['co_last_name'],
        'hasBeenRetrieved': request.form['hasBeenRetrieved'],
        'appDate': dateString,
    }
    mycursor = mydb.cursor()
    mycursor.reset()
    queryAddApplicant = ("INSERT INTO Applicant (applicant_email, applicant_first_name, applicant_last_name, phone_number, zip_code, street, city, state) \
        VALUES ( %(appEmail)s, %(fname)s, %(lname)s, %(phone)s, %(zipcode)s, %(street)s, %(city)s, %(state)s )")
    queryAddApplication = ("INSERT INTO AdoptionApplication(applicant_email, application_date, co_applicant_first_name, co_applicant_last_name) \
        VALUES ( %(appEmail)s, STR_TO_DATE(%(appDate)s,'%m,%d,%Y'), %(coFName)s, %(coLName)s )")
    if applicantInfo['hasBeenRetrieved'] != 'true':
        mycursor.execute(queryAddApplicant, applicantInfo)
        mydb.commit()
    mycursor.execute(queryAddApplication, applicantInfo)
    mydb.commit()
    appNumber = mycursor.lastrowid
    mycursor.close()
    mydb.close()
    return json.dumps(appNumber)


@app.route('/restApi/Dog/AddDog', methods=['POST'])
def api_Post_Add_Dog():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    surrenderdateList = list(request.form['surrender_date'])
    surrenderdateList[2] = ','
    surrenderdateList[5] = ','
    surrenderdateString = "".join(surrenderdateList)
    dobList = list(request.form['dob'])
    dobList[2] = ','
    dobList[5] = ','
    dobString = "".join(dobList)
    dogInfo = {
        'name': request.form['name'],
        'sex': request.form['sex'],
        'alterationStatus': True if request.form['alteration_status'] == 'true' else False,
        'dob': dobString,
        'description': request.form['description'],
        'microchipid': request.form['microchip'],
        'surrenderDate': surrenderdateString,
        'surrenderReason': request.form['reason'],
        'animalControl': True if request.form['animal_control'] == 'true' else False,
        'unknownBreed': request.form['unknownBreed'],
        'email': request.form['username']
    }
    mycursor = mydb.cursor()
    mycursor.reset()
    queryAddDog = ("INSERT INTO Dog(dog_name, sex, description, alteration_status, dob, surrender_date, surrender_reason, surrendered_by_animal_control, volunteer_email) \
        VALUES ( %(name)s, %(sex)s, %(description)s, %(alterationStatus)s, STR_TO_DATE(%(dob)s,'%m,%d,%Y'), STR_TO_DATE(%(surrenderDate)s,'%m,%d,%Y') , %(surrenderReason)s, \
        %(animalControl)s,  %(email)s )")
    mycursor.execute(queryAddDog, dogInfo)
    mydb.commit()
    dogId = mycursor.lastrowid
    #Insert Breeds
    if dogInfo['unknownBreed'] == 'off':
        breedList = request.form.getlist('breed')
        for breed in breedList:
            queryAddBreed = ("INSERT INTO AssignedTo(breed_name, dog_id) \
                VALUES ( %s, %s )")
            mycursor.execute(queryAddBreed, (breed, dogId,))
            mydb.commit()
    else:
        queryAddBreed = ("INSERT INTO AssignedTo(breed_name, dog_id) \
                VALUES ( %s, %s )")
        mycursor.execute(queryAddBreed, (dogInfo['unknownBreed'], dogId,))
        mydb.commit()
    #Insert MicroChipId
    if dogInfo['microchipid'] != "":
        queryAddMicroChipId = ("INSERT INTO MicrochipId(value, dog_id) \
            VALUES ( %s, %s )")
        mycursor.execute(queryAddMicroChipId, (dogInfo['microchipid'],dogId,))
        mydb.commit()
    mycursor.close()
    mydb.close()
    return json.dumps(dogId)

@app.route('/restApi/Dog/EditDog', methods=['POST'])
def api_Post_Edit_Dog():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }
    dogInfo = {
        'dogId': request.form['dogId'],
        'sex': request.form['sex'],
        'alterationStatus': True if request.form['alteration_status'] == 'true' else False,
        'microchipid': request.form['microchip'],
        'unknownBreed': request.form['unknownBreed'],
        'email': request.form['username']
    }
    mydb = mysql.connect(**config)
    mycursor = mydb.cursor()
    mycursor.reset()
    queryEditDog = ("UPDATE Dog SET sex = %(sex)s, alteration_status = %(alterationStatus)s WHERE dog_id = %(dogId)s")
    mycursor.execute(queryEditDog, dogInfo)
    mydb.commit()
    #Insert Breeds
    if dogInfo['unknownBreed'] == 'off':
        breedList = request.form.getlist('breed')
        queryDeleteUnknownOrMixedBreed = ("DELETE FROM  AssignedTo WHERE dog_id = %s")
        mycursor.execute(queryDeleteUnknownOrMixedBreed, (dogInfo['dogId'],))
        mydb.commit()
        for breed in breedList:
            queryAddBreed = ("INSERT INTO AssignedTo(breed_name, dog_id) \
                VALUES ( %s, %s )")
            mycursor.execute(queryAddBreed, (breed, dogInfo['dogId'],))
            mydb.commit()
    #Insert MicroChipId
    if dogInfo['microchipid'] != "":
        queryAddMicroChipId = ("INSERT INTO MicrochipId(value, dog_id) \
            VALUES ( %s, %s )")
        mycursor.execute(queryAddMicroChipId, (dogInfo['microchipid'],dogInfo['dogId'],))
        mydb.commit()
    mycursor.close()
    mydb.close()
    return json.dumps('Succesful Update of Dog Details')

@app.route('/restApi/Dog/AddExpense', methods=['POST'])
def api_Get_Add_Expenses():
    # Configure DB
    config = {
        'user': 'gatechUser',
        'password': 'GatechUser33!',
        'host': 'localhost',
        'database': 'cs6400_su20_team33',
        'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    dateList = list(request.form['date'])
    dateList[2] = ','
    dateList[5] = ','
    dateString = "".join(dateList)
    vendorName = ''
    expenseInfo = {
        'dogId': int(request.form['dogId']),
        'expenseDate': dateString,
        'expenseAmount': float(request.form['expense_amount']),
        'optDescription': request.form['description'],
        'checkForName': request.form['checkForName']
    }
    if expenseInfo['checkForName'] == 'off':
        vendorName = request.form['vendor']
        expenseInfo.update({'vendorName' : vendorName})
    else:
        vendorName = request.form['vname']
        expenseInfo.update({'vendorName' : vendorName})
    mycursor = mydb.cursor()
    mycursor.reset()
    queryAddVendor = ("INSERT IGNORE INTO Vendor (vendor_name)\
                       VALUES (%(vendorName)s)")
    queryAddExpense = ("INSERT INTO Expense (dog_id, date_of_expense, expense_amount, optional_description, vendor_name) \
        VALUES (  %(dogId)s, STR_TO_DATE(%(expenseDate)s,'%m,%d,%Y'), %(expenseAmount)s, %(optDescription)s, %(vendorName)s)")

    if expenseInfo['checkForName'] == 'on':
        mycursor.execute(queryAddVendor, expenseInfo)
        mydb.commit()

    mycursor.execute(queryAddExpense, expenseInfo)
    mydb.commit()

    mycursor.close()
    mydb.close()
    return json.dumps(int(request.form['dogId']))

@app.route('/restApi/Dog/AddAdoption', methods=['POST'])
def api_Get_Add_Adoption():
    # Configure DB
    config = {
        'user': 'gatechUser',
        'password': 'GatechUser33!',
        'host': 'localhost',
        'database': 'cs6400_su20_team33',
        'raise_on_warnings': True
    }

    dateList = list(request.form['date'])
    dateList[2] = ','
    dateList[5] = ','
    dateString = "".join(dateList)

    adoptionPaperwork = {
        'dogId': int(request.form['dogId']),
        'adoptionDate': dateString,
        'dogName': request.form['dogName'],
        'applicantName': request.form['applicantName'],
        'applicantEmail': request.form['applicantEmail'],
        'appNum': int(request.form['appNum'])
    }
    mydb = mysql.connect(**config)
    mycursor = mydb.cursor()
    mycursor.reset()

    #Update Approved Application 
    queryUpdateApprovedApplication = ("UPDATE ApprovedApplication SET adoption_date = STR_TO_DATE(%(adoptionDate)s,'%m,%d,%Y') WHERE application_number =  %(appNum)s and applicant_email =  %(applicantEmail)s ")
    mycursor.execute(queryUpdateApprovedApplication, adoptionPaperwork)
    mydb.commit()

    #Update Dog to Adopted
    queryUpdateDog = ("UPDATE Dog SET application_number = %(appNum)s WHERE dog_id =  %(dogId)s")
    mycursor.execute(queryUpdateDog, adoptionPaperwork)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return json.dumps(adoptionPaperwork['dogName'] + ' has been successfully adopted to a new home by ' + adoptionPaperwork['applicantName'] + '(' + adoptionPaperwork['applicantEmail'] + ')')

@app.route('/restApi/Application/ReviewApplication', methods=['POST'])
def api_Get_Review_Application():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }

    mydb = mysql.connect(**config)
    type = request.form['type']
    appId = request.form['appNo']
    appEmail = request.form['email']
    data_application = {
        'appId': int(appId),
        'appEmail': appEmail,
    }
    query = None
    if type == "Approve":
        query = ("INSERT INTO ApprovedApplication (application_number, applicant_email) \
            VALUES (%(appId)s, %(appEmail)s)")
    elif type == "Reject":
        query = ("INSERT INTO RejectedApplication (application_number, applicant_email) \
            VALUES (%(appId)s, %(appEmail)s)")
    else:
        return json.dumps(None)
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    mycursor.execute(query, data_application)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return json.dumps(None)

def convertTupleToJsonFormat(data):
    objectArray=[]
    for datapoint in data:
        valuesArray = []
        for i in range(len(datapoint)):
            valuesArray.append(datapoint[i])
        objectArray.append(valuesArray)
    jsonDTFormat = {"data" : objectArray }
    return (json.dumps(jsonDTFormat, default=str))