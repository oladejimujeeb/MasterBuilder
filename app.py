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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)