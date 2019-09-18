from flask import Flask, request, render_template, session, logging, flash, redirect, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from landifo import *

app = Flask(__name__)
app.config.from_pyfile('mail.cfg')
zmail = Mail(app)

s = URLSafeTimedSerializer('d3m0n61nM3')


def generate_token(email):
    return (s.dumps(email, salt='mail-confirm'))

def send_email(mail, email):
    token = generate_token(mail)
    msg = Message('Confirm Email', sender='mysplupdates@gmail.com', recipients=[mail, email])
    link = url_for('confirm_update', token=token, _external=True)
    msg.body = "Dear User, /n/n Please click on the link provided to cofirm your business location update./n The link expires in 15 miuntes./n Please ignore if you did not try to update Your business location. /n {}".format(link)
    zmail.send(msg)

def sendLandInfo(currentUser):
    status, mailAdd, attachment = getLandInfo(currentUser)
    if status:
        # succesfully added, send mail
        msg = Message('Land Information Request', sender='mysplupdates@gmail.com', recipients=[ 'm.olabisimurit@gmail.com'])
        msg.body = "Hi, A Request Has Been Made For Land Information From " + mailAdd + ". Kindly, Find Attached The Survey Plan. Thank you."
        msg.attach(
            attachment.filename,
            'application/octect-stream',
            attachment.read())
        zmail.send(msg)
        return jsonify({'status' : True, 'message' : 'Success. Please Check the Provided Email For Details'})
    else:
        # not succesfully added do sothg elsefields
        return jsonify({'status' : False, 'message' : 'Operation Failed. Please Retry'})

def sendECharting(currentUser):
    status, mailAdd, attachment = getLandInfo(currentUser)
    if status:
        # succesfully added, send mail
        msg = Message('Electronic Charting Request', sender='mysplupdates@gmail.com', recipients=['m.olabisimurit@gmail.com'])
        msg.body = "Hi, A Request Has Been Made For e-Charting From " + mailAdd + ". Kindly, Find Attached The Survey Plan. Thank you."
        msg.attach(
            attachment.filename,
            'application/octect-stream',
            attachment.read())
        zmail.send(msg)
        return jsonify({'status' : True, 'message' : 'Success. Please Check the Provided Email For Details'})
    else:
        # not succesfully added do sothg elsefields
        return jsonify({'status' : False, 'message' : 'Operation Failed. Please Retry'})