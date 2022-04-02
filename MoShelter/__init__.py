"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import MoShelter.views, MoShelter.RestAPI, MoShelter.AnimalControlReport, MoShelter.ExpenseAnalysisReport, MoShelter.VolunteerLookupReport, MoShelter.MonthlyAdoptionReport
