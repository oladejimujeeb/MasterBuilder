import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = 'rand0mTEkT4Ma5tERBuil3rGenerated2TestStuffs'
MAIL_SUPPRESS_SEND = False
MAIL_DEBUG = True
TESTING = False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USERNAME = 'masterbuilerupdates@gmail.com'
MAIL_PASSWORD = 'C0d3D3mon60&'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_DEFAULT_SENDER = ('LandQuery From MasterBuilder', 'masterbuilerupdates@gmail.com')