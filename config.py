# import os



# class Config:
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/laphic'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # JWT configuration
#     JWT_SECRET_KEY = 'MY SECRET KEY'
#     JWT_ACCESS_TOKEN_EXPIRES = 900


#     # Set debug mode here
#     DEBUG = True  # This will enable debugging globally



import os

class Config:
    # Remote MySQL database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sql10780827:DdzjfA55mR@sql10.freesqldatabase.com:3306/sql10780827'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = 'MY SECRET KEY'
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes

    # Enable debug mode globally
    DEBUG = True

