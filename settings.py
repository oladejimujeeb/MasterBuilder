import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = 'rand0mTEkT4Ma5tERBuil3rGenerated2TestStuffs'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USERNAME = 'masterbuilerupdates@gmail.com'
MAIL_PASSWORD = 'C0d3D3mon60&'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_DEBUG = True
MAIL_SUPPRESS_SEND = False
TESTING = False
MAIL_DEFAULT_SENDER = ('LandQuery From MasterBuilder', 'masterbuilerupdates@gmail.com')