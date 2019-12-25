from allimports import *
from models import *
from middleware import *
import datetime
import uuid
from flask import Flask, request, jsonify, json
from sqlalchemy import exc, text

current_date = datetime.datetime.today()
app.config.from_object('settings')
#app.config.from_pyfile('config.cfg')


def pre_register():
    #check if all req fields are given
    data = request.get_json()
    fields = ['lastname', 'firstname', 'phonenumber', 'email', 'password']
    if not all(i in request.json for i in fields):
        return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400

def hash_password(password):
    cpassword = generate_password_hash(password, method='sha256')
    return cpassword

###
def reg_man():
    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    phonenumber = request.form.get('phonenumber')
    email = request.form.get('email')
    password = request.form.get('password')
    surveylist = request.form.getlist('tags')
    hashed_password =  hash_password(password)
    # try:
    streak = ""
    user = User(user_lastname = lastname, user_firstname = firstname, user_phone_number = phonenumber, user_email = email, user_password = hashed_password, user_confirm=0, user_admin=0, user_status=0)
    db.session.add(user)
    db.session.commit()
    user_str = str(uuid.uuid4())[:6]
    user.user_id = 'user00' + str(user.id) + user_str 
    db.session.commit()
    streak += str(user.user_id)
    out = 0
    for item in surveylist:
        oneSurvey = Survey.query.filter_by(survey_name=item).first()
        if oneSurvey:
            if oneSurvey.survey_frequency == None:
                oneSurvey.survey_frequency = 2
            else:
                oneSurvey.survey_frequency += 1
            out += str(oneSurvey.survey_frequency)
            # db.session.commit()
        else:
            survey = Survey(item, int(1))
            db.session.add(survey)
            out += str(oneSurvey.survey_frequency)
    db.session.commit()
    streak += str(out)
    return streak
    # except exc.IntegrityError:
    #     return "error"

# #REGISTER USER API - POST
# def register_user():
#     fields = ['lastname', 'firstname', 'phonenumber', 'email', 'password', 'surveylist']
#     if not all(i in request.json for i in fields):
#         return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
#     data = request.get_json()
#     password = data['password']
#     hashed_password =  hash_password(password)
#     name = data['lastname'] + ', ' + 'firstname'
#     choice = data['surveylist']
#     return jsonify({'name': name, 'Choice List': choice})
#     # try:
#     #     user = User(user_lastname = data['lastname'], user_firstname = data['firstname'], user_phone_number = data['phonenumber'], user_email = data['email'], user_password = hashed_password, user_confirm=0, user_admin=0, user_status=0)
    #     db.session.add(user)
    #     db.session.commit()
    #     user_str = str(uuid.uuid4())[:6]
    #     user.user_id = 'user00' + str(user.id) + user_str 
    #     db.session.commit()
    #     for item in data['surveylist']:
    #         oneSurvey = Survey.query.filter_by(survey_name=item).first()
    #         if oneSurvey:
    #             oneSurvey.survey_frequency += 1
    #             # db.session.commit()
    #         else:
    #             survey = Survey(item, int(1))
    #             db.session.add(survey)
    #     db.session.commit()
    #     return jsonify({'status': True, 'message': 'Registration Successful'})
    # except exc.IntegrityError:
    #     return jsonify({'status' : False, 'message' : 'Email Or Phone Number Exists'}), 400

#LOG IN USER API - POST 

def sign_in():
    auth = request.authorization

    #No authorization/auth username or password???
    if not auth or not auth.username or not auth.password:
        return jsonify({'status': False, 'message':'Login Required'}), 401

    #login is with email 
    user = User.query.filter_by(user_email=auth.username).first()
    #user not found
    if not user:
        return jsonify({'status': False, 'message':'Could not verify. User Not Found'}), 401

    #user exists, check if password is correct
    if check_password_hash(user.user_password, auth.password):
        token = jwt.encode({'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=4320)}, app.config['SECRET_KEY'])

        # return jsonify({'status': False, 'message':'Could not verify. Password Incorrect'}), 401 
        return jsonify({'status': True, 'message' : 'Log In Successful', 'token' : token.decode('UTF-8')}), 200

    else:
        return jsonify({'status': False, 'message':'Could not verify. Password Incorrect'}), 401

def get_user_details(userid):
    try:
        user = User.query.filter_by(user_id=userid).first()
        if not user:
            return jsonify({'status' : False, 'message' : 'User Not Found'}), 404

        data = {}
        data['user_id'] = user.user_id
        data['user_lastname'] = user.user_lastname
        data['user_firstname'] = user.user_firstname
        data['user_phone_number'] = user.user_phone_number
        data['user_email'] = user.user_email
        data['user_admin'] = user.user_admin

        return jsonify({'user' : data, 'status' : True, 'message' : 'Success'})
    except:
        return jsonify({'status' : False, 'message' : 'Failed'})