import os

from datetime import datetime
# from invix_app.extensions import db

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/invix'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = 'MY SECRET KEY'
    JWT_ACCESS_TOKEN_EXPIRES = 900
