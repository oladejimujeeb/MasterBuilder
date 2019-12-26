from allimports import *
from models import *
from middleware import *
import datetime
import uuid
from flask import Flask, request, render_template, session, logging, flash, redirect, url_for, jsonify, json
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object('settings')
#app.config.from_pyfile('config.cfg')
zmail = Mail(app)

current_date = datetime.datetime.today()

def landNoCall(currentUserId, uMail, uName):
    try:
        siteaddress = request.form.get('siteaddress')
        eastern = request.form.get('eastern')
        western = request.form.get('western')
        email = request.form.get('email')
        selectCity = request.form.get('select-city')
        surveyplan = request.files.get('surveyplan')
        #add to db
        landInfo = Land(siteaddress, eastern, western, 0, selectCity, email)
        db.session.add(landInfo)
        db.session.commit()
        land_str = str(uuid.uuid4())[:6]
        landInfo.land_id = 'land10' + str(landInfo.id) + land_str 
        landInfo.user_id = currentUserId
        db.session.commit()
        streak = landInfo.land_id
        #username and email
        # try:
            #send mail
        subject = 'Land Information Request'
        rec1 = 'm.olabisimurit@gmail.com'
        rec2 = 'hiphyhisaac@gmail.com'
        msg = Message(subject, recipients=[rec1, rec2])
        streak += ", About to send Mail. Subject: " + subject
        msg.html = "Hi, <br><br> A Request Has Been Made For Land Information From <b>" + uName + "</b>, with registered email address <b>" +uMail + "</b>. <br> \
                The details are as given. <br><p style='text-align:left'>City: <b>" + selectCity + "<b><br> Site Address: <b>" + siteaddress + "</b><br> Northern Coordinate: \
                    <b>" + western  + "</b><br> Eastern Coordinate: <b>" + eastern + "</b><br> Provided Email: <b>" + email + "</b></p><br><br> \
                    Kindly, Find Attached The Survey Plan. <br><br>Cheers."
        msg.attach(
            surveyplan.filename,
            'application/octect-stream',
            surveyplan.read())
        streak += ". Attaching attachments. About to send."
        #zmail.send(msg)
        # return "sent"
        return streak
        # except Exception as e:
        #     return e
    except Exception as e:
        return e

# get land info
#GET API
def getLandInfo(): 
    #confirm all is in request
    fields = ["siteaddress", "eastern", "western", "email", "select-city", "current_user"]
    if not all(i in request.json for i in fields):
        return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
    if "surveyplan" not in request.files:
        return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
    data = request.get_json()
    try:
        # add to db
        currentUser = data["current_user"]
        landInfo = Land(data['siteaddress'], data['eastern'], data['western'], 0, data['select-city'], data['email'])
        db.session.add(landInfo)
        db.session.commit()
        landInfo.user_id = currentUser
        db.session.commit()
        #send mail
        try:
            msg = Message('Land Information Request', sender='mysplupdates@gmail.com', recipients=[ 'm.olabisimurit@gmail.com', 'hiphyhisaac@gmail.com'])
            msg.body = "Hi, A Request Has Been Made For Land Information From " + data['email'] + ". Kindly, Find Attached The Survey Plan. Thank you."
            msg.attach(
                attachment.filename,
                'application/octect-stream',
                attachment.read())
            zmail.send(msg)
            return jsonify({'status' : True, 'message' : 'Success. Please Check the Provided Email For Details in an Hour.'})
        except:
            return jsonify({'status' : False, 'message' : 'Operation Failed. Please Retry'}), 400
        # return True, data['email'], request.files['surveyplan'], "sux"
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
