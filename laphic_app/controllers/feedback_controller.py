# from flask import Blueprint, request, jsonify
# from laphic_app.extensions import db
# from laphic_app.models import Feedback
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from functools import wraps
# import re

# # Define a Blueprint for feedback-related routes
# feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/v1/feedback')

# # Admin or Superadmin required decorator
# def admin_or_superadmin_required(fn):
#     @wraps(fn)
#     @jwt_required()
#     def wrapper(*args, **kwargs):
#         user_info = get_jwt_identity()
#         if user_info['role'] not in ['admin', 'superadmin']:
#             return jsonify({'error': 'Admin or Superadmin access required'}), 403
#         return fn(*args, **kwargs)
#     return wrapper

# # Submit feedback (Public access)
# @feedback_bp.route('/submit', methods=['POST'])
# def submit_feedback():
#     try:
#         data = request.get_json()
#         required_fields = ['userId', 'name', 'email', 'comments', 'rating']
#         if not all(key in data for key in required_fields):
#             return jsonify({'error': 'Missing required fields: userId, name, email, comments, rating'}), 400

#         user_id = data['userId']
#         name = data['name']
#         email = data['email']
#         comments = data['comments']
#         rating = data['rating']
#         image_url = data.get('imageUrl')

#         # Validate inputs
#         if not isinstance(rating, int) or rating < 1 or rating > 5:
#             return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
#         if len(comments) > 500:
#             return jsonify({'error': 'Comments must be 500 characters or less'}), 400
#         if len(name) > 100 or len(email) > 100:
#             return jsonify({'error': 'Name and email must be 100 characters or less'}), 400
#         if not re.match(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$', email):
#             return jsonify({'error': 'Invalid email format'}), 400

#         feedback = Feedback(
#             user_id=user_id,
#             name=name,
#             email=email,
#             comment=comments,
#             rating=rating,
#             image_url=image_url
#         )
#         db.session.add(feedback)
#         db.session.commit()

#         return jsonify({'message': 'Feedback submitted successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'Failed to submit feedback', 'details': str(e)}), 500

# # Get feedback history for a user (User or Admin/Superadmin)
# @feedback_bp.route('/history/<user_id>', methods=['GET'])
# @jwt_required()
# def get_feedback_history(user_id):
#     try:
#         current_user = get_jwt_identity()
#         # Allow access if user_id matches JWT identity or user is admin/superadmin
#         if current_user['user_id'] != user_id and current_user['role'] not in ['admin', 'superadmin']:
#             return jsonify({'error': 'Unauthorized access to feedback history'}), 403

#         feedback_list = Feedback.query.filter_by(user_id=user_id).all()
#         return jsonify([
#             {
#                 'id': f.feedback_id,
#                 'name': f.name,
#                 'email': f.email,
#                 'comments': f.comment,
#                 'rating': f.rating,
#                 'imageUrl': f.image_url,
#                 'timestamp': f.feedback_date.isoformat()
#             } for f in feedback_list
#         ]), 200
#     except Exception as e:
#         return jsonify({'error': 'Failed to retrieve feedback history', 'details': str(e)}), 500

# # Get all feedback (Admin/Superadmin only)
# @feedback_bp.route('/all', methods=['GET'])
# @admin_or_superadmin_required
# def get_all_feedback():
#     try:
#         feedback_list = Feedback.query.all()
#         return jsonify([
#             {
#                 'id': f.feedback_id,
#                 'user_id': f.user_id,
#                 'name': f.name,
#                 'email': f.email,
#                 'comments': f.comment,
#                 'rating': f.rating,
#                 'imageUrl': f.image_url,
#                 'timestamp': f.feedback_date.isoformat()
#             } for f in feedback_list
#         ]), 200
#     except Exception as e:
#         return jsonify({'error': 'Failed to retrieve all feedback', 'details': str(e)}), 500



from flask import Blueprint, request, jsonify
from laphic_app.extensions import db
from laphic_app.models import Feedback, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
import re

# Define a Blueprint for feedback-related routes
feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/v1/feedback')

# Admin or Superadmin required decorator
def admin_or_superadmin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Admin or Superadmin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Get user_id by Firebase UID
@feedback_bp.route('/user/<firebase_uid>', methods=['GET'])
def get_user_id(firebase_uid):
    try:
        user = User.query.filter_by(firebase_uid=firebase_uid).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user_id': user.user_id}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve user ID', 'details': str(e)}), 500

# Submit feedback (Public access)
@feedback_bp.route('/submit', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        required_fields = ['userId', 'name', 'email', 'comment', 'rating']
        if not all(key in data for key in required_fields):
            return jsonify({'error': 'Missing required fields: userId, name, email, comment, rating'}), 400

        user_id = data['userId']
        name = data['name']
        email = data['email']
        comment = data['comment']
        rating = data['rating']
        subject = data.get('subject')
        feedback_type = data.get('feedbackType')
        image_url = data.get('imageUrl')

        # Validate inputs
        try:
            user_id = int(user_id)  # Convert userId to integer
        except (ValueError, TypeError):
            return jsonify({'error': 'userId must be a valid integer'}), 400

        if not isinstance(rating, int) or rating < 0 or rating > 5:
            return jsonify({'error': 'Rating must be an integer between 0 and 5'}), 400
        if len(comment) > 500:
            return jsonify({'error': 'Comment must be 500 characters or less'}), 400
        if len(name) > 100 or len(email) > 100:
            return jsonify({'error': 'Name and email must be 100 characters or less'}), 400
        if subject and len(subject) > 100:
            return jsonify({'error': 'Subject must be 100 characters or less'}), 400
        if feedback_type and len(feedback_type) > 50:
            return jsonify({'error': 'Feedback type must be 50 characters or less'}), 400
        # Fixed regex: escaped the hyphen to prevent it from being treated as a range
        if not re.match(r'^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$', email):
            return jsonify({'error': 'Invalid email format'}), 400

        feedback = Feedback(
            user_id=user_id,
            name=name,
            email=email,
            subject=subject,
            comment=comment,
            rating=rating,
            feedback_type=feedback_type,
            image_url=image_url
        )
        db.session.add(feedback)
        db.session.commit()

        return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit feedback', 'details': str(e)}), 500

# Get feedback history for a user (User or Admin/Superadmin)
@feedback_bp.route('/history/<user_id>', methods=['GET'])
@jwt_required()
def get_feedback_history(user_id):
    try:
        current_user = get_jwt_identity()
        try:
            user_id = int(user_id)  # Convert user_id to integer
        except (ValueError, TypeError):
            return jsonify({'error': 'userId must be a valid integer'}), 400

        # Allow access if user_id matches JWT identity or user is admin/superadmin
        if current_user['user_id'] != user_id and current_user['role'] not in ['admin', 'superadmin']:
            return jsonify({'error': 'Unauthorized access to feedback history'}), 403

        feedback_list = Feedback.query.filter_by(user_id=user_id).all()
        return jsonify([
            {
                'id': f.feedback_id,
                'user_id': f.user_id,
                'name': f.name,
                'email': f.email,
                'subject': f.subject,
                'comment': f.comment,
                'rating': f.rating,
                'imageUrl': f.image_url,
                'feedbackType': f.feedback_type,
                'timestamp': f.feedback_date.isoformat()
            } for f in feedback_list
        ]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve feedback history', 'details': str(e)}), 500

# Get all feedback (Admin/Superadmin only)
@feedback_bp.route('/all', methods=['GET'])
@admin_or_superadmin_required
def get_all_feedback():
    try:
        feedback_list = Feedback.query.all()
        return jsonify([
            {
                'id': f.feedback_id,
                'user_id': f.user_id,
                'name': f.name,
                'email': f.email,
                'subject': f.subject,
                'comment': f.comment,
                'rating': f.rating,
                'imageUrl': f.image_url,
                'feedbackType': f.feedback_type,
                'timestamp': f.feedback_date.isoformat()
            } for f in feedback_list
        ]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve all feedback', 'details': str(e)}), 500