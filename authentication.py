from allimports import *
from models import *
from middleware import *
import datetime
import uuid 

current_date = datetime.datetime.today()

def pre_register():
    #check if all req fields are given
    data = request.get_json()
    fields = ['lastname', 'firstname', 'phonenumber', 'email', 'password']
    if not all(i in request.json for i in fields):
        return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400

def hash_password(password):
    cpassword = generate_password_hash(password, method='sha256')
    return cpassword

#REGISTER USER API - POST
def register_user():
    # pre_register()
    fields = ['lastname', 'firstname', 'phonenumber', 'email', 'password']
    if not all(i in request.json for i in fields):
        return jsonify({'status' : False, 'message' : 'One or More Missing Field(s)!!!'}), 400
    data = request.get_json()
    password = data['password']
    hashed_password =  hash_password(password)
    try:
        user = User(user_lastname = data['lastname'], user_firstname = data['firstname'], user_phone_number = data['phonenumber'], user_email = data['email'], user_password = hashed_password, user_confirm=0, user_admin=0, user_status=0)
        db.session.add(user)
        db.session.commit()
        user_str = str(uuid.uuid4())[:6]
        user.user_id = 'user00' + str(user.id) + user_str 
        db.session.commit()
        return jsonify({'status': True, 'message': 'Success'}) 
    except exc.IntegrityError:
        return jsonify({'status' : False, 'message' : 'Email Or Phone Number Exists'}), 400

#LOG IN USER API - POST
def signin():
    # when request is coming from body of form
    # data = request.get_json()
    # email = data['email']
    # password = data['password']
    auth = request.authorization

    #No authorization/auth username or password???
    if not auth or not auth.username or not auth.password:
        return jsonify({'status': False, 'message':'Could not verify. Login Required'}), 401

    #login is with email 
    user = User.query.filter_by(user_email=auth.username).first()
    #user not found
    if not user:
        return jsonify({'status': False, 'message':'Could not verify. Login Required'}), 401

    #user exists, check if password is correct
    if check_password_hash(user.user_password, auth.password):
        token = jwt.encode({'user_id': user.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=300)}, app.config['SECRET_KEY'])

        return jsonify({'status': True, 'message' : 'Log In Successful', 'token' : token.decode('UTF-8')})

    return jsonify({'status': False, 'message':'Could not verify. Login Required'}), 401