import os

from datetime import datetime
# from invix_app.extensions import db

# class Config:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/invix'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # JWT configuration
#     JWT_SECRET_KEY = 'MY SECRET KEY'
#     JWT_ACCESS_TOKEN_EXPIRES = 900

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:9y6TWFCsP5mTVcYoiYBd@invixdb.cx2eiq6gm98c.ap-southeast-1.rds.amazonaws.com:3306/invixdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = 'MY SECRET KEY'
    JWT_ACCESS_TOKEN_EXPIRES = 900

