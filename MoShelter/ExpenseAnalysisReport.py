from flask import render_template, flash, redirect, url_for, request
from MoShelter import app
import mysql.connector as mysql
import json


# Define function to get the detailed expense analysis report
@app.route('/Report/GetExpenseAnalysisReport', methods=['GET'])
def api_Get_Expense_Analysis_Report():
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
    mycursor.execute("SELECT Vendor.vendor_name, ROUND(COALESCE(SUM(expense_amount),0),2) totalExpense FROM Vendor LEFT JOIN Expense ON expense.vendor_name = Vendor.vendor_name\
            GROUP BY vendor_name ORDER BY totalExpense DESC")
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    expenseReportVals = convertTupleToJsonFormat(myresult)
    return (expenseReportVals)

def convertTupleToJsonFormat(data):
    objectArray=[]
    for datapoint in data:
        valuesArray = []
        for i in range(len(datapoint)):
            valuesArray.append(datapoint[i])
        objectArray.append(valuesArray)
    jsonDTFormat = {"data" : objectArray }
    return (json.dumps(jsonDTFormat, default=str))