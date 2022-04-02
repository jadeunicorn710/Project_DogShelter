from flask import render_template, flash, redirect, url_for, request
from MoShelter import app
import mysql.connector as mysql
import json


# Define function to get the detailed monthly adoption report
@app.route('/Report/GetMonthlyAdoptionReport', methods=['GET'])
def api_Get_Monthly_Adoption_Report():
    # Configure DB
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
    mycursor.execute("SELECT s0.breed_name, s0.SurrenderYearMonth, s1.number_of_surrenders, s2.number_of_adoptions, ROUND(s3.expenses,2), ROUND(s2.adoption_fees,2), ROUND(s2.net,2)\
                FROM\
                (SELECT *\
                FROM (SELECT DISTINCT EXTRACT(YEAR_MONTH FROM surrender_date) AS SurrenderYearMonth\
                FROM Dog\
                WHERE (surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 12 MONTH, '%Y-%m-01 00:00:00') AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59'))) tmp1\
                CROSS JOIN\
                (SELECT DISTINCT breed_name\
                FROM AssignedTo) tmp2) s0\
                LEFT JOIN\
                (SELECT breed_name, EXTRACT(YEAR_MONTH FROM surrender_date) AS SurrenderYearMonth, COUNT(Distinct dog_id) AS number_of_surrenders\
                FROM AssignedTo\
                LEFT JOIN Dog USING(dog_id)\
                WHERE\
                (surrender_date BETWEEN DATE_FORMAT(NOW() - INTERVAL 12 MONTH, '%Y-%m-01 00:00:00') AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59'))\
                GROUP BY breed_name, SurrenderYearMonth) s1 ON s1.SurrenderYearMonth = s0.SurrenderYearMonth AND s1.breed_name = s0.breed_name\
                LEFT JOIN\
                (SELECT breed_name,EXTRACT(YEAR_MONTH FROM ApprovedApplication.adoption_date) AS AdoptionYearMonth, \
                    COUNT(Distinct Dog.dog_id) AS number_of_adoptions, SUM(t1.adoption_fees) as adoption_fees, SUM(t1.net) as net\
                FROM Dog\
                LEFT JOIN ApprovedApplication ON ApprovedApplication.application_number = Dog.application_number\
                LEFT JOIN AssignedTo ON AssignedTo.dog_id = Dog.dog_id\
                LEFT JOIN\
                (SELECT Dog.dog_id,\
                (CASE\
                    WHEN NOT ISNULL(Dog.application_number) THEN IF (Dog.surrendered_by_animal_control, (0.15 * SUM(Expense.expense_amount)),(1.15 * SUM(Expense.expense_amount)))\
                END) AS adoption_fees, 0.15 * SUM(Expense.expense_amount) AS net\
                FROM Dog\
                INNER JOIN Expense ON Dog.dog_id = Expense.dog_id\
                GROUP BY Dog.dog_id) t1 ON t1.dog_id = Dog.dog_id\
                WHERE\
                ApprovedApplication.adoption_date  BETWEEN DATE_FORMAT(NOW() - INTERVAL 12 MONTH, '%Y-%m-01 00:00:00') AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59')\
                GROUP BY breed_name, AdoptionYearMonth) s2 ON (s0.breed_name = s2.breed_name AND s0.SurrenderYearMonth = s2.AdoptionYearMonth)\
                LEFT JOIN\
                (SELECT breed_name,EXTRACT(YEAR_MONTH FROM Expense.date_of_expense) AS ExpenseYearMonth, SUM(expense_amount) AS expenses\
                FROM Dog\
                LEFT JOIN Expense ON Dog.dog_id = Expense.dog_id\
                LEFT JOIN AssignedTo ON AssignedTo.dog_id = Dog.dog_id\
                WHERE\
                (Expense.date_of_expense  BETWEEN DATE_FORMAT(NOW() - INTERVAL 12 MONTH, '%Y-%m-01 00:00:00') AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59'))\
                GROUP BY breed_name, ExpenseYearMonth) s3 ON (s3.breed_name = s0.breed_name AND s3.ExpenseYearMonth = s0.SurrenderYearMonth)\
                ORDER BY s0.SurrenderYearMonth, s0.breed_name")

    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    adoptionReportVals = convertTupleToJsonFormat(myresult)

    return (adoptionReportVals)


def convertTupleToJsonFormat(data):
    objectArray = []
    for datapoint in data:
        valuesArray = []
        for i in range(len(datapoint)):
            valuesArray.append(datapoint[i])
        objectArray.append(valuesArray)
    jsonDTFormat = {"data": objectArray}
    return (json.dumps(jsonDTFormat, default=str))
