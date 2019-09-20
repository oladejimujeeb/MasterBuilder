from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt 

app = Flask("__name__")
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.String(25), unique=True)
    user_lastname =  db.Column(db.String(500), unique=False)
    user_firstname =  db.Column(db.String(500), unique=False)
    user_phone_number =  db.Column(db.String(15), unique=True)
    user_email =  db.Column(db.String(500), unique=True)
    user_password =  db.Column(db.String(500), unique=False)
    user_confirm = db.Column(db.Boolean, unique=False)
    user_admin = db.Column(db.Boolean, unique=False)
    user_status = db.Column(db.Boolean, unique=False)

    #FK
    job_id = db.Column(db.String(25), db.ForeignKey('job.job_id'), unique=False)
    
    #Foreign relations
    partners = db.relationship('Partner', backref='user', lazy='dynamic')
    permits = db.relationship('BuildingPermit', backref='user', lazy='dynamic')
    land_infos = db.relationship('Land', backref='user', lazy='dynamic')
    
    def __init__(self, user_lastname, user_firstname, user_phone_number, user_email, user_password, user_admin, user_status, user_confirm):
        self.user_lastname = user_lastname
        self.user_firstname = user_firstname
        self.user_phone_number = user_phone_number
        self.user_email = user_email
        self.user_password = user_password
        self.user_confirm = user_confirm
        self.user_admin = user_admin
        self.user_status = user_status

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(25), unique=True)
    job_name =  db.Column(db.String(500), unique=True)
    job_details =  db.Column(db.String(500), unique=False)
    
    #Foreign relation
    user_job = db.relationship('User', backref='job' ,lazy='dynamic')
    partner_job = db.relationship('Partner', backref='job', lazy='dynamic')

    def __init__(self, job_name, job_details):
        self.job_details = job_details
        self.job_name = job_name

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_address =  db.Column(db.String(500), unique=False)
    
    #Foreign keys
    job_id = db.Column(db.String(25), db.ForeignKey('job.job_id'), unique=False)
    user_id = db.Column(db.String(25), db.ForeignKey('user.user_id'), unique=False)

    def __init__(self, job_address):
        self.job_address = job_address

class Land(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    land_id = db.Column(db.String(25), unique=True)
    land_address =  db.Column(db.String(500), unique=False)
    land_cordinate_north =  db.Column(db.String(20), unique=False)
    land_cordinate_south =  db.Column(db.String(20), unique=False)
    land_request_status = db.Column(db.Boolean, unique=False) 
    land_city =  db.Column(db.String(50), unique=False)
    land_email = db.Column(db.String(50), unique=False)

    #Foreign relations
    response = db.relationship('LIResponse', backref='land', lazy='dynamic')

    #Foreign keys
    user_id = db.Column(db.String(25), db.ForeignKey('user.user_id'), unique=False)

    def __init__(self, land_address, land_cordinate_north, land_cordinate_south, land_request_status, land_city, land_email):
        self.land_address = land_address
        self.land_cordinate_north = land_cordinate_north
        self.land_cordinate_south = land_cordinate_south
        self.land_request_status = land_request_status
        self.land_city = land_city
        self.land_email = land_email

class BuildingPermit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_time = db.Column(db.DateTime, unique=False)
    request_status = db.Column(db.Boolean, unique=False)

    #foreign keys
    user_id = db.Column(db.String(25), db.ForeignKey('user.user_id'), unique=False)

    def __init__(self, request_time, request_status):
        self.request_status = request_status
        self.request_time = request_time

class LIResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_e = db.Column(db.String(500), unique=False)
    response_info = db.Column(db.String(500), unique=False)
   
    #foreign keys
    land_id = db.Column(db.String(25), db.ForeignKey('land.land_id'), unique=False)
  
    def __init__(self, response_e, response_info):
        self.response_e = response_e
        self.response_info = response_info

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs): 
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!', 'status': False }), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'status': False, 'message':'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


if __name__ == "__main__":
    db.create_all()