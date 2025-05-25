from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from laphic_app.extensions import db, migrate, bcrypt, jwt
from laphic_app.controllers.auth_controller import auth_bp
from laphic_app.controllers.provider_controller import provider_bp
from laphic_app.controllers.Booking_controller import booking_bp
from laphic_app.controllers.service_controller import service_bp
from laphic_app.controllers.feedback_controller import feedback_bp
from laphic_app.controllers.message_controller import message_bp
from laphic_app.controllers.gallery_controller import gallery_bp
from laphic_app.controllers.notification_controller import notifications_bp
from laphic_app.models.user import User
from laphic_app.models.service import Service
from laphic_app.models.provider import Provider
from laphic_app.models.Booking import Booking
from laphic_app.models.feedback import Feedback
from laphic_app.models.message import Message
from laphic_app.models.gallery import Gallery
from laphic_app.models.notification import Notification
from flask_jwt_extended import get_jwt_identity

# Import missing dependencies
try:
    from laphic_app.extensions import socketio  # Add this import
    from laphic_app.firebase_config import initialize_firebase  # Add proper import path
except ImportError as e:
    print(f"Import error: {e}")
    # Handle missing imports gracefully
    socketio = None
    initialize_firebase = None

def create_app():
    app = Flask(__name__)
    
    # Load config from config.py
    try:
        app.config.from_object('config.Config')
    except Exception as e:
        print(f"Config loading error: {e}")
        # Fallback basic config
        app.config['SECRET_KEY'] = 'your-secret-key-here'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Firebase (if available)
    if initialize_firebase:
        try:
            initialize_firebase()
        except Exception as e:
            print(f"Firebase initialization error: {e}")

    # Set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize WebSocket functionality (if available)
    if socketio:
        socketio.init_app(app, cors_allowed_origins="*")

    # Consolidated CORS configuration
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000"],
            "supports_credentials": True
        }
    })

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(notifications_bp)

    # Create database tables (run once or on first start)
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Database creation error: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Run with or without socketio
    if socketio:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)