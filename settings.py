import os

SQLALCHEMY_DATABASE_URI = os.environment.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.environment.get('SECRET_KEY')