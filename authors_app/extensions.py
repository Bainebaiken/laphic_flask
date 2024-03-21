from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine

db = SQLAlchemy()
migrate = Migrate()
bcrypt  = Bcrypt()