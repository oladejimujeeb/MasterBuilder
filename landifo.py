from allimports import *
from models import *
from middleware import *
import datetime
import uuid
from flask import Flask, request, jsonify, json

current_date = datetime.datetime.today()

# get land info
#GET API
def getLandInfo(currentUser):
    #confirm all is in request
    fields = ["siteaddress", "eastern", "western", "email", "select-city"]
    if not all(i in request.json for i in fields):
        return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
    if "surveyplan" not in request.files:
        return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
    data = request.get_json()
    try:
        landInfo = Land(data['siteaddress'], data['eastern'], data['western'], 0, data['select-city'], data['email'])
        db.session.add(landInfo)
        db.session.commit()
        landInfo.user_id = currentUser
        db.session.commit()
        return True, data['email'], request.files['surveyplan']
    except:
        return False, data['email'], request.files['surveyplan']

# update land info