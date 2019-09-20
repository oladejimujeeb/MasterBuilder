from allimports import *
from models import *
from middleware import *
import datetime
import uuid
from flask import Flask, request, jsonify, json

current_date = datetime.datetime.today()

# get land info
#GET API
def getLandInfo():
    #confirm all is in request
    fields = ["siteaddress", "eastern", "western", "email", "select-city", "current_user"]
    if not all(i in request.json for i in fields):
        return False, 0, 0, 0
        # return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
    if "surveyplan" not in request.files:
        return False, 0, 0, 0
        # return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
    data = request.get_json()
    try:
        currentUser = data["current_user"]
        landInfo = Land(data['siteaddress'], data['eastern'], data['western'], 0, data['select-city'], data['email'])
        db.session.add(landInfo)
        db.session.commit()
        landInfo.user_id = currentUser
        db.session.commit()
        return True, data['email'], request.files['surveyplan'], "sux"
    except:
        return False, data['email'], request.files['surveyplan'], "fux"

def getBuildPermit():
    #confirm all is in request
    fields = ["city", "current_user", "current_mail"]
    if not all(i in request.json for i in fields):
        return False, 0, 0
    data = request.get_json()
    try:
        permit = BuildingPermit(data["city"], current_date, 0)
        db.session.add(permit)
        db.session.commit()
        permit.user_id = data["current_user"]
        db.session.commit()
        return True, permit.request_time, data["current_mail"]
    except:
        return False, 0, 0


# update land info