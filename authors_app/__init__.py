from flask import Flask
from authors_app.extensions import db, migrate, bcrypt
from authors_app.models.user import User
from authors_app.models.company import Company
from authors_app.models.books import Books
from authors_app.controllers.auth_controlller import auth
from flask_sqlalchemy import SQLAlchemy
def create_app():
    app = Flask(__name__)
  
    # Load configuration from a Config class
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #db = SQLAlchemy(app)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Define routes
    @app.route("/")
    def home():
        return "Hello, everyone!"
    
    app.register_blueprint(auth,url_prefix='/api/v1/auth')

    return app












# from flask import Flask
# from authors_app.extensions import db, migrate, bcrypt
# from authors_app.models.user import User
# from authors_app.models.company import Company
# from authors_app.models.books import Books
# from authors_app.controllers.auth_controlller import auth

# def create_app():
#     app = Flask(__name__)
  
#     # Load configuration from a Config class
#     app.config.from_object('config.Config')

#     # Initialize Flask extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     bcrypt.init_app(app)

#     # Importing models should be done after initializing extensions
#     # Importing model classes should start with a capital letter
#     # It's recommended to import each model separately
#     # Adjust imports accordingly based on the actual file structure
#     from authors_app.models import user, company, books

#     # Define routes
#     @app.route("/")
#     def home():
#         return "Hello, everyone!"
    
#     app.register_blueprint(auth)


#     return app


















# from flask import Flask
# from authors_app.extensions import db,migrate,bcrypt


# def create_app():
#     app = Flask(__name__)
  
#     app.config.from_object('config.Config')#helps us to access our config file ad not 

#     db.init_app(app)
#     migrate.init_app(app,db)
#     bcrypt.init_app(app)

#     from authors_app.models.user import user
#     from authors_app.models.company import company
#     from authors_app.models.books import books

#     @app.route("/")
#     def home():
#      return "hello everyone "
    
#     return app
