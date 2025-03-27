from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bcrypt  = Bcrypt()
jwt = JWTManager()