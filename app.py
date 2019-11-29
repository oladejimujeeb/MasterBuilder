from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from authentication import *
from models import *
from flask_mail import Mail, Message

app = Flask("__name__")
app.config.from_pyfile('config.cfg')
db.init_app(app)
zmail = Mail(app)


@app.route('/')
def home():
    current_mail = session.get('current_mail', None)
    return render_template('index.html', current_mail=current_mail)

@app.route('/about')
def about():
    current_mail = session.get('current_mail', None)
    return render_template('about.html', current_mail=current_mail)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session.pop('current_mail', None)
    session.pop('maiden', None)
    if request.method == "POST":
        result = registerByAPI()
        status = result["status"]
        if status:
            response = loginByAPI()
            session['maiden'] = response["token"]
            current_mail = request.form.get('email')
            session['current_mail'] = current_mail
            return render_template('land-info.html', current_mail=current_mail)
        else:
            fail = result["message"]
            return render_template('signup.html', fail=fail)

    return render_template('signup.html')
 
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    session.pop('current_mail', None)
    session.pop('maiden', None)
    if request.method == "POST":
        result = loginByAPI()
        # return result
        status = result["status"]
        if status is True:
            current_mail = request.form.get('email')
            session['current_mail'] = current_mail
            session['token'] = "maiden4all09567u22manvu899rn"
            session['maiden'] = result["token"]
            return render_template('land-info.html', current_mail=current_mail)
        else:
            fail = result["message"]
            return render_template('signin.html', fail=fail)

    return render_template('signin.html')

@app.route('/land-info', methods=['GET'])
def landInfo():
    current_mail = session.get('current_mail', None)
    if current_mail is None:
        return redirect(url_for('signin'))
    return render_template('land-info.html', current_mail=current_mail)
 
@app.route('/land-info', methods=['POST'])
def landInfoPost():
    if request.method == 'POST':
        #check token
        current_mail = session.get('current_mail', None)
        if current_mail is None:
            return redirect(url_for('signin'))
        currentUser = User.query.filter_by(user_email=current_mail).first()
        currentUserId = currentUser.user_id
        current_name = currentUser.user_firstname + " " + currentUser.user_lastname
        #add to db        
        try:
            result = landNoCall(currentUserId, current_mail, current_name)
            if str(result) == "sent":
                message = "Success. Please Check the Provided Email For Details in an Hour."
                return render_template("requestsuccessful.html",  message=message, current_mail=current_mail)
            else:
                message = "An Error Occured. Please Try Again."
                return render_template('land-info.html', current_mail=current_mail, message=message)
        except Exception as e:
            return e

@app.route('/request')
def requestQ():
    return render_template('request.html')

@app.route('/success')
def requestsuccessful():
    current_mail = session.get('current_mail', None)
    if current_mail is None:
        return redirect(url_for('signin'))
    return render_template('requestsuccessful.html', current_mail=current_mail)

@app.route('/contact')
def contact():
    current_mail = session.get('current_mail', None)
    return render_template('contact.html', current_mail=current_mail)

@app.route('/faq')
def faq():
    current_mail = session.get('current_mail', None)
    return render_template('faq.html', current_mail=current_mail)


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
        #confirm_email(mail, name)
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

####LAND INFO#####
@app.route('/api/landinfo', methods=['POST'])
def apiLandInfo():
    json_list = getLandInfo()
    return json_list

@app.route('/api/permit', methods=['POST'])
def apiPermit():
    json_list = sendBuildPermit()
    return json_list


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)