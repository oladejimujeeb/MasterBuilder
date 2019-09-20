from allimports import *
from models import *
import datetime
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import os, warnings, requests, json, base64
from mailings import *

# consume registration api
def registerByAPI():
    try:
        data = {
            "lastname" : request.form.get('lastname'),
            "firstname" : request.form.get('firstname'),
            "phonenumber" : request.form.get('phonenumber'),
            "email" : request.form.get('email'),
            "password" : request.form.get('password')
        }

        url = "http://0.0.0.0:5000/api/register"

        headers = {
            'content-type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return (response.json())

        # result = response.json()
        # status = result["status"]
        # if status:
        #     # send mail
        #     mail = data["email"]
        #     names = data["firstname"] + " " + data["lastname"]
        #     sender = confirm_email(mail, names)
        #     return (sender.json())
        # else:
        #     return (response.json())
    except:
        return jsonify({'status' : False, 'message' : 'An Error Occurred'}), 400

def loginByAPI():
    try:
        email = request.form.get('email')
        passkey = request.form.get('password')
        url = "http://0.0.0.0:5000/api/login"

        conf = email + ":" + passkey
        encodedBytes = base64.b64encode(conf.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        basiC = "Basic " + encodedStr

        headers = {
            'content-type':'application/json',
            'Authorization': basiC
        }

        response = requests.post(url, headers=headers)
        # return str(request.headers["origin"])
        try:
            return response.json()
        except:
            user = User.query.filter_by(user_email=email).first()
            responsel = {
                'status' : True,
                'message' : 'Log In Successful', 
                'user_id' : user.user_id, 
                'user_mail' : user.user_mail
            }
            return json.loads(responsel)
    except:
        user = User.query.filter_by(user_email=email).first()
        response = {
            'status' : True,
            'message' : 'Log In Successful', 
            'user_id' : user.user_id, 
            'user_mail' : user.user_email
        }
        less = json.dumps(response)
        return json.loads(less)
        # return responsel.json()
        # return jsonify({'status' : False, 'message' : 'An Error Occurred'}), 400

def landInfoByAPI(currentUser):
    try:
        data = {
            "siteaddress" : request.form.get('siteaddress'),
            "eastern" : request.form.get('eastern'),
            "western" : request.form.get('western'),
            "email" : request.form.get('email'),
            "select-city" : request.form.get('select-city'),
            current_user : currentUser
        }

        url = "http://0.0.0.0:5000/api/landinfo"

        headers = {
            'content-type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return (response.json())

        # result = response.json()
        # status = result["status"]
        # if status:
        #     # send mail
        #     mail = data["email"]
        #     names = data["firstname"] + " " + data["lastname"]
        #     sender = confirm_email(mail, names)
        #     return (sender.json())
        # else:
        #     return (response.json())
    except:
        return jsonify({'status' : False, 'message' : 'An Error Occurred'}), 400

def permitByAPI(currentUser, currentMail):
    try:
        data = {
            "city" : request.form.get('city'),
            current_user : currentUser,
            current_mail : currentMail
        }

        url = "http://0.0.0.0:5000/api/permit"

        headers = {
            'content-type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return (response.json())
    except:
        return jsonify({'status' : False, 'message' : 'An Error Occurred'}), 400