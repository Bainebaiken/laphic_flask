from flask import Blueprint, request, jsonify
from laphic_app.extensions import db
from laphic_app.models import Feedback  # Ensure Feedback is imported correctly (uppercase)
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Define a Blueprint for feedbacks-related routes
feedback_bp = Blueprint('feedbacks', __name__, url_prefix='/api/v1/feedbacks')  # Adjusted Blueprint definition

# Create a new feedback
@feedback_bp.route('/register', methods=['POST'])
def create_feedback():
    try:
        data = request.get_json()
        User_ID = data.get('User_ID')
        Rating = data.get('Rating')
        Comment = data.get('Comment')
        Feedback_Date = data.get('Feedback_Date')

        # Create the Feedback instance
        new_feedback = Feedback(
            User_ID=User_ID, 
            Rating=Rating, 
            Comment=Comment,
            Feedback_Date=datetime.fromisoformat(Feedback_Date) if Feedback_Date else None
        )

        db.session.add(new_feedback)
        db.session.commit()

        return jsonify({'feedback': 'Feedback created successfully', 'Feedback_ID': new_feedback.Feedback_ID}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'feedback': 'Failed to create feedback', 'error': str(e)}), 500

# Get all feedbacks
@feedback_bp.route('/', methods=['GET'])
def get_all_feedbacks():
    try:
        feedbacks = Feedback.query.all()  # Corrected to use Feedback model
        feedbacks_list = []
        for feedback in feedbacks:
            feedbacks_list.append({
                'Feedback_ID': feedback.Feedback_ID,
                'User_ID': feedback.User_ID,
                'Rating': feedback.Rating,
                'Comment': feedback.Comment,
                'Feedback_Date': feedback.Feedback_Date.strftime('%Y-%m-%d %H:%M:%S') if feedback.Feedback_Date else None
            })
        return jsonify(feedbacks_list), 200

    except Exception as e:
        return jsonify({'feedback': 'Failed to retrieve feedbacks', 'error': str(e)}), 500

# Get a single feedback by ID
@feedback_bp.route('/<int:id>', methods=['GET'])
def get_feedback(id):
    try:
        feedback = Feedback.query.get(id)  # Corrected to use Feedback model
        if not feedback:
            return jsonify({'feedback': 'Feedback not found'}), 404

        return jsonify({
            'Feedback_ID': feedback.Feedback_ID,
            'User_ID': feedback.User_ID,
            'Rating': feedback.Rating,
            'Comment': feedback.Comment,
            'Feedback_Date': feedback.Feedback_Date.strftime('%Y-%m-%d %H:%M:%S') if feedback.Feedback_Date else None
        }), 200

    except Exception as e:
        return jsonify({'feedback': 'Failed to retrieve feedback', 'error': str(e)}), 500

# Update a feedback by ID
@feedback_bp.route('/<int:id>', methods=['PUT'])
def update_feedback(id):
    try:
        data = request.get_json()
        feedback = Feedback.query.get(id)
        if not feedback:
            return jsonify({'feedback': 'Feedback not found'}), 404

        feedback.User_ID = data.get('User_ID', feedback.User_ID)
        feedback.Rating = data.get('Rating', feedback.Rating)
        feedback.Comment = data.get('Comment', feedback.Comment)
        feedback.Feedback_Date = datetime.fromisoformat(data.get('Feedback_Date')) if data.get('Feedback_Date') else feedback.Feedback_Date
        feedback.updated_at = datetime.now()

        db.session.commit()
        return jsonify({'feedback': 'Feedback updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'feedback': 'Failed to update feedback', 'error': str(e)}), 500

# Delete a feedback by ID
@feedback_bp.route('/<int:id>', methods=['DELETE'])
def delete_feedback(id):
    try:
        feedback = Feedback.query.get(id)
        if not feedback:
            return jsonify({'feedback': 'Feedback not found'}), 404

        db.session.delete(feedback)
        db.session.commit()
        return jsonify({'feedback': 'Feedback deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'feedback': 'Failed to delete feedback', 'error': str(e)}), 500


# from flask import Blueprint, request, jsonify
# from laphic_app.extensions import db
# from laphic_app.models import feedback  
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from datetime import datetime

# # Define a Blueprint for feedbacks-related routes
# feedback_bp = Blueprint('feedbacks', __name__, url_prefix='/api/v1/feedbacks')  # Adjusted Blueprint definition




# # Create a new feedbacks
# @feedback_bp.route('/register', methods=['POST'])  
# def create_feedback():
#     try:
#         data = request.get_json()
#         Feedback_ID = data.get('Feedback_ID')
#         User_ID = data.get('User_ID')
#         Service_ID = data.get('Service_ID')
#         Rating  = data.get('Rating ')
#         Comment = data.get('Comment')
#         Feedback_Date = data.get('Feedback_Date')



#         new_message = feedback(Feedback_ID=Feedback_ID, User_ID=User_ID, Service_ID=Service_ID,
#                         Rating =Rating , Comment=Comment,Feedback_Date=Feedback_Date)

#         db.session.add(new_message)
#         db.session.commit()

#         return jsonify({'feedback': 'feedback created successfully', 'id': new_message.id}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'feedback': 'Failed to create feedbacks', 'error': str(e)}), 500

# # Get all feedbacks
# @feedback_bp.route('/', methods=['GET'])
# def get_all_feedbacks():
#     try:
#         feedbacks = feedback.query.all()
#         feedbacks_list = []
#         for feedbacks in feedbacks:
#             feedbacks_list.append({
#                 'id': feedbacks.id,
#                 'Feedback_ID': feedbacks.Feedback_ID,
#                 'User_ID': feedbacks.User_ID,
#                 'Service_ID': feedbacks.Service_ID,
#                 'created_at': feedbacks.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#                 'updated_at': feedbacks.updated_at.strftime('%Y-%m-%d %H:%M:%S') if feedbacks.updated_at else None
#             })
#         return jsonify(feedbacks_list), 200

#     except Exception as e:
#         return jsonify({'feedback': 'Failed to retrieve feedbacks', 'error': str(e)}), 500

# # Get a single feedbacks by ID
# @feedback_bp.route('/<int:id>', methods=['GET'])
# def get_feedback(id):
#     try:
#         feedbacks = feedback.query.get(id)
#         if not feedbacks:
#             return jsonify({'feedback': 'feedback not found'}), 404

#         return jsonify({
#             'id': feedbacks.id,
#             'Feedback_ID': feedbacks.Feedback_ID,
#             'User_ID': feedbacks.User_ID,
#             'Service_ID': feedbacks.Service_ID,
#             'created_at': feedbacks.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#             'updated_at': feedbacks.updated_at.strftime('%Y-%m-%d %H:%M:%S') if feedbacks.updated_at else None
#         }), 200

#     except Exception as e:
#         return jsonify({'feedback': 'Failed to retrieve feedbacks', 'error': str(e)}), 500

# # Update a feedbacks by ID
# @feedback_bp.route('/<int:id>', methods=['PUT'])
# def update_feedback(id):
#     try:
#         data = request.get_json()
#         feedbacks = feedback.query.get(id)
#         if not feedbacks:
#             return jsonify({'feedback': 'feedback not found'}), 404

#         feedbacks.Feedback_ID = data.get('Feedback_ID', feedbacks.Feedback_ID)
#         feedbacks.User_ID = data.get('User_ID', feedbacks.User_ID)
#         feedbacks.Service_ID = data.get('Service_ID', feedbacks.Service_ID)
#         feedbacks.message_sent = data.get('message_sent', feedbacks.message_sent)
#         feedbacks.updated_at = datetime.now()

#         db.session.commit()
#         return jsonify({'feedback': 'feedback updated successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'feedback': 'Failed to update feedbacks', 'error': str(e)}), 500

# # Delete a feedbacks by ID
# @feedback_bp.route('/<int:id>', methods=['DELETE'])
# def delete_feedback(id):
#     try:
#         feedbacks = feedback.query.get(id)
#         if not feedbacks:
#             return jsonify({'feedback': 'feedback not found'}), 404

#         db.session.delete(feedbacks)
#         db.session.commit()
#         return jsonify({'feedback': 'feedback deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'feedback': 'Failed to delete feedbacks', 'error': str(e)}), 500

