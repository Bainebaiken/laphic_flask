# from flask import Flask
# from flask_migrate import Migrate
# from flask_socketio import SocketIO
# from laphic_app.extensions import db, migrate, bcrypt
# from laphic_app.controllers.auth_controlller import auth_bp
# from laphic_app.controllers.Booking_controller import booking_bp
# from laphic_app.controllers.provider_controller import provider_bp
# from laphic_app.controllers.feedback_controller import feedback_bp
# from laphic_app.controllers.message_controller import message_bp
# from laphic_app.controllers.service_controller import service_bp
# from laphic_app.controllers.gallery_controller import gallery_bp
# from laphic_app.models.user import User
# from laphic_app.models.service import Service
# from laphic_app.models.provider import Provider
# from laphic_app.models.Booking import Booking
# from laphic_app.models.feedback import Feedback
# from laphic_app.models.message import Message
# from laphic_app.models.gallery import Gallery
# from laphic_app.extensions import JWTManager
# from flask_cors import CORS

# # Initialize SocketIO
# socketio = SocketIO(cors_allowed_origins="*")  # Enable CORS for WebSocket testing
# migrate = Migrate()  # Move Migrate here to make it globally accessible

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')  # Load config from config.py
    
#     # Set up extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     bcrypt.init_app(app)
#     jwt = JWTManager(app)
#     socketio.init_app(app)  # Initialize WebSocket functionality

#     # Register blueprints
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(provider_bp)
#     app.register_blueprint(booking_bp)
#     app.register_blueprint(service_bp)
#     app.register_blueprint(message_bp)
#     app.register_blueprint(feedback_bp)
#     app.register_blueprint(gallery_bp)

#     # Optionally, you can enable debug mode from the config:
#     app.debug = app.config['DEBUG']

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     socketio.run(app, debug=True)  # Use socketio.run instead of app.run




from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors import CORS
from laphic_app.extensions import db, migrate, bcrypt, jwt
from laphic_app.controllers.auth_controller import auth_bp
from laphic_app.controllers.provider_controller import provider_bp
from laphic_app.controllers.Booking_controller import booking_bp
from laphic_app.controllers.service_controller import service_bp
from laphic_app.controllers.feedback_controller import feedback_bp
from laphic_app.controllers.message_controller import message_bp
from laphic_app.controllers.gallery_controller import gallery_bp
from laphic_app.models.user import User
from laphic_app.models.service import Service
from laphic_app.models.provider import Provider
from laphic_app.models.Booking import Booking
from laphic_app.models.feedback import Feedback
from laphic_app.models.message import Message
from laphic_app.models.gallery import Gallery

# Initialize SocketIO
socketio = SocketIO(cors_allowed_origins="*")  # Enable CORS for WebSocket testing

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load config from config.py
    
    # Set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)  # Initialize WebSocket functionality

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(gallery_bp)

    # Enable CORS for REST API requests
    CORS(app)

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)  # Use socketio.run for both HTTP and WebSocket
