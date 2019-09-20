from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from authentication import *
from models import *

app = Flask("__name__")
app.config.from_pyfile('config.cfg')
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        result = registerByAPI()
        status = result["status"]
        if status:
            sux = result["message"]
            return render_template('signup.html', sux=sux)
        else:
            fail = result["message"]
            return render_template('signup.html', fail=fail)

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        result = loginByAPI()
        # return result
        status = result["status"]
        if status is True:
            current_user = result["user_id"]
            current_mail = result["user_mail"]
            session["user"] = current_user
            return render_template('land-info.html', current_mail=current_mail)
        else:
            fail = result["message"]
            return render_template('signin.html', fail=fail)

    return render_template('signin.html')

@app.route('/land-info')
@token_required
def landInfo(current_user):
    return render_template('land-info.html')

@app.route('/request')
def requestQ():
    return render_template('request.html')

@app.route('/requestsuccessful')
def requestsuccessful():
    return render_template('requestsuccessful.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/building-permit-action')
def buildingPermitAction():
    return render_template('building-permit-action.html')

@app.route('/building-permit')
def buildingPermit():
    return render_template('building-permit.html')

@app.route('/consent')
def consent():
    return render_template('consent.html')

@app.route('/e-charting')
def eCharting():
    return render_template('e-charting.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

#########################################
################ APIs LIST ##############
#########################################
################   USERS   ##############
@app.route('/api/register', methods=['GET','POST'])
def apiRegister():
    if request.method == "POST":
        json_list = register_user()
        return json_list
    else:
        return jsonify({'message' : 'Hello MasterBuilder Developer. Registration is a POST REQUEST'})

@app.route('/api/<token>', methods=['POST'])
def confirm_registration(token):
    try:
        email = s.loads(token, salt='mail-confirm', max_age=60 * 15)
        sux = "Email Confirmed. Please Log In To Continue."
        #update confirm
        return render_template('signin', sux=sux)
    except SignatureExpired:
        fail = "Link Expired. A new Token Would Be Sent Soon. Please check your email address"
        confirm_email(mail, name)
        return render_template('signin', fail=fail)        


@app.route('/api/login', methods=['POST'])
def apiSignIn():
    json_list = sign_in()
    return json_list

@app.route('/api/user/<user_id>', methods=['GET'])
@token_required
def user_info(current_user, user_id):
    output = get_user_details(user_id)
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)