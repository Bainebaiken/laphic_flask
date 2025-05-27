


# controllers.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from laphic_app.models.notification import Notification
from laphic_app.models.user import User
from laphic_app.extensions import db
from functools import wraps

# Create a Blueprint for notifications
notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/v1/notifications')

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
@notifications_bp.route('/all', methods=['GET'])
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
@notifications_bp.route('/update/<int:notification_id>', methods=['PUT'])
@jwt_required()
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

# Delete a notification
@notifications_bp.route('/delete/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    try:
        # Get the current user's identity (user id)
        current_user_id = get_jwt_identity()
        
        # Find the notification by its ID and ensure it belongs to the current user
        notification = Notification.query.filter_by(id=notification_id, user_id=current_user_id).first()
        
        # If notification not found
        if not notification:
            return jsonify({"message": "Notification not found"}), 404
        
        # Delete the notification
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({"message": "Notification deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete notification", "details": str(e)}), 500

# Delete all notifications for a user
@notifications_bp.route('/delete-all', methods=['DELETE'])
@jwt_required()
def delete_all_notifications():
    try:
        # Get the current user's identity (user id)
        current_user_id = get_jwt_identity()
        
        # Find all notifications for the current user
        notifications = Notification.query.filter_by(user_id=current_user_id).all()
        
        if not notifications:
            return jsonify({"message": "No notifications found"}), 404
        
        # Delete all notifications for the user
        deleted_count = Notification.query.filter_by(user_id=current_user_id).delete()
        db.session.commit()
        
        return jsonify({
            "message": f"All notifications deleted successfully",
            "deleted_count": deleted_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete notifications", "details": str(e)}), 500

# Mark all notifications as read for a user
@notifications_bp.route('/mark-all-read', methods=['PUT'])
@jwt_required()
def mark_all_notifications_read():
    try:
        # Get the current user's identity (user id)
        current_user_id = get_jwt_identity()
        
        # Update all unread notifications for the current user
        updated_count = Notification.query.filter_by(
            user_id=current_user_id, 
            read=False
        ).update({Notification.read: True})
        
        db.session.commit()
        
        return jsonify({
            "message": "All notifications marked as read",
            "updated_count": updated_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to mark notifications as read", "details": str(e)}), 500