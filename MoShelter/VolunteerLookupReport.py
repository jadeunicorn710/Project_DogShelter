from flask import render_template, flash, redirect, url_for, request
from MoShelter import app
import mysql.connector as mysql
import json


# Define function to get the volunteer lookup report
@app.route('/Report/GetVolunteerLookupReport', methods=['GET'])
def api_Get_Volunteer_Lookup_Report():
    #Configure DB
    config = {
      'user': 'gatechUser',
      'password': 'GatechUser33!',
      'host': 'localhost',
      'database': 'cs6400_su20_team33',
      'raise_on_warnings': True
    }
    nameGiven = request.args.get('name')
    print('MYNAMEIS' + nameGiven)
    nameString = {'name': '%'+ nameGiven + '%'}
    mydb = mysql.connect(**config)
    mycursor = mydb.cursor(buffered=True)
    mycursor.reset()
    mycursor.execute("SELECT volunteer_first_name, volunteer_last_name, volunteer_email, cell_phone\
                FROM RegularVolunteer WHERE LOWER(volunteer_last_name) LIKE LOWER(%(name)s) OR LOWER(volunteer_first_name) LIKE LOWER(%(name)s) \
                ORDER BY volunteer_last_name, volunteer_first_name", nameString)
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    volunteerReportVals = convertTupleToJsonFormat(myresult)
    return (volunteerReportVals)

def convertTupleToJsonFormat(data):
    objectArray=[]
    for datapoint in data:
        valuesArray = []
        for i in range(len(datapoint)):
            valuesArray.append(datapoint[i])
        objectArray.append(valuesArray)
    jsonDTFormat = {"data" : objectArray }
    return (json.dumps(jsonDTFormat, default=str))