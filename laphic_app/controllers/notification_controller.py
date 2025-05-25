# controllers.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from laphic_app.models.notification import Notification
from laphic_app.models.user import User
from laphic_app.extensions import db
from functools import wraps

# Create a Blueprint for notifications
notifications_bp = Blueprint('notifications', __name__)

# Custom decorator to check if the current user is an Admin or Super Admin
def admin_or_superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)  # Get the current user from the database
        
        if not user or user.role not in ['Admin', 'Super Admin']:
            return jsonify({"message": "You do not have permission to access this resource"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# Create a notification for a user (only Admin or Super Admin can create/edit)
@notifications_bp.route('/create', methods=['POST'])
@jwt_required()
# @admin_or_superadmin_required
def create_notification():
    data = request.get_json()

    # Ensure the necessary fields are provided
    if not data.get('message'):
        return jsonify({"message": "Notification message is required"}), 400

    # Get the current user's identity (user id)
    current_user_id = get_jwt_identity()

    # Create the new notification
    new_notification = Notification(
        user_id=current_user_id,
        message=data['message'],
    )

    db.session.add(new_notification)
    db.session.commit()

    return jsonify({"message": "Notification created successfully"}), 201

# Get all notifications for a user
@notifications_bp.route('/get', methods=['GET'])
@jwt_required()
def get_notifications():
    # Get the current user's identity (user id)
    current_user_id = get_jwt_identity()

    # Retrieve notifications for the logged-in user
    notifications = Notification.query.filter_by(user_id=current_user_id).all()

    # Prepare the list of notifications to return
    notifications_list = [{
        "id": notification.id,
        "message": notification.message,
        "read": notification.read,
        "created_at": notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for notification in notifications]

    return jsonify(notifications_list), 200

# Mark a notification as read/unread
@notifications_bp.route('/update', methods=['PUT'])
# @jwt_required()
# @admin_or_superadmin_required
def update_notification(notification_id):
    data = request.get_json()

    # Ensure the 'read' field is provided
    if 'read' not in data:
        return jsonify({"message": "'read' status is required"}), 400

    # Get the current user's identity (user id)
    current_user_id = get_jwt_identity()

    # Find the notification by its ID
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user_id).first()

    # If notification not found
    if not notification:
        return jsonify({"message": "Notification not found"}), 404

    # Update the read status of the notification
    notification.read = data['read']
    db.session.commit()

    return jsonify({"message": "Notification status updated successfully"}), 200

