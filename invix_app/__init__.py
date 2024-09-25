from flask import Flask
from invix_app.extensions import db, migrate, bcrypt
from invix_app.controllers.auth_controlller import auth_bp
from invix_app.controllers.posts_controller import post_bp
from invix_app.controllers.article_controller import article_bp
# from invix_app.controllers.content_controller import content_bp
from invix_app.controllers.category_controller import category_bp
from invix_app.models.user import User
from invix_app.models.posts import Posts
from invix_app.models.article import Article
# from invix_app.models.content import Content
from invix_app.models.category import Category

from invix_app.extensions import JWTManager

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'MY SECRET KEY'
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(article_bp)
    # app.register_blueprint(content_bp)
    app.register_blueprint(category_bp)
    return app

