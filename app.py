from flask import Flask, render_template, request, redirect, url_for, session

app = Flask("__name__")
app.config.from_pyfile('config.cfg')
#db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/land-info')
def landInfo():
    return render_template('land-info.html')

@app.route('/request')
def request():
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

@app.route('/index-two')
def indexTwo():
    return render_template('index-two.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)