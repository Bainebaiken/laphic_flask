# import os

# from datetime import datetime
# # class Config:
# #     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/laphic'
# #     SQLALCHEMY_TRACK_MODIFICATIONS = False

# #     # JWT configuration
# #     JWT_SECRET_KEY = 'MY SECRET KEY'
# #     JWT_ACCESS_TOKEN_EXPIRES = 900

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/laphic'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = 'MY SECRET KEY'
    JWT_ACCESS_TOKEN_EXPIRES = 900

    # Set debug mode here
    DEBUG = True  # This will enable debugging globally
