from mailbox import Message
from flask import Blueprint, request, jsonify
from laphic_app.extensions import db
from laphic_app.models import message  
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Define a Blueprint for messages-related routes
message_bp = Blueprint('messages', __name__, url_prefix='/api/v1/messages')  # Adjusted Blueprint definition


# Edit a message
@message_bp.route('/<int:message_id>/edit', methods=['PUT'])
@jwt_required()
def edit_message(message_id):
    try:
        user_info = get_jwt_identity()  # Get the identity of the logged-in user
        data = request.get_json()
        new_content = data.get('content')

        if not new_content:
            return jsonify({'error': 'Message content is required'}), 400

        # Retrieve the message
        message = message.query.get(message_id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404

        # Check if the user is the owner of the message
        if message.sender_id != user_info['id']:
            return jsonify({'error': 'You can only edit your own messages'}), 403

        # Update the message content
        message.content = new_content
        db.session.commit()

        return jsonify({'message': 'Message updated successfully', 'data': {'id': message.id, 'content': message.content}}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a message (Provider only)
@message_bp.route('/<int:message_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    try:
        user_info = get_jwt_identity()  # Get the identity of the logged-in user

        # Ensure the user is a provider
        if user_info['role'] != 'provider':
            return jsonify({'error': 'Only providers can delete messages'}), 403

        # Retrieve the message
        message = Message.query.get(message_id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404

        # Delete the message
        db.session.delete(message)
        db.session.commit()

        return jsonify({'message': 'Message deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# # Create a new messages
# @message_bp.route('/register', methods=['POST'])  
# def create_provider():
#     try:
#         data = request.get_json()
#         Message_ID = data.get('Message_ID')
#         Sender_ID = data.get('Sender_ID')
#         Receiver_ID = data.get('Receiver_ID')
#         Message_Content = data.get('Message_Content')
#         Timestamp = data.get('Timestamp')

#         new_message = message(Message_ID=Message_ID, Sender_ID=Sender_ID, Receiver_ID=Receiver_ID,
#                         Message_Content=Message_Content, Timestamp=Timestamp)

#         db.session.add(new_message)
#         db.session.commit()

#         return jsonify({'message': 'message created successfully', 'id': new_message.id}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to create messages', 'error': str(e)}), 500

# # Get all messages
# @message_bp.route('/', methods=['GET'])
# def get_all_messages():
#     try:
#         messages = message.query.all()
#         messages_list = []
#         for messages in messages:
#             messages_list.append({
#                 'id': messages.id,
#                 'Message_ID': messages.Message_ID,
#                 'Sender_ID': messages.Sender_ID,
#                 'Receiver_ID': messages.Receiver_ID,
#                 'message_sent': messages.message_sent,
#                 'blong': messages.blong,
#                 'created_at': messages.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#                 'updated_at': messages.updated_at.strftime('%Y-%m-%d %H:%M:%S') if messages.updated_at else None
#             })
#         return jsonify(messages_list), 200

#     except Exception as e:
#         return jsonify({'message': 'Failed to retrieve messages', 'error': str(e)}), 500

# # Get a single messages by ID
# @message_bp.route('/<int:id>', methods=['GET'])
# def get_post(id):
#     try:
#         messages = message.query.get(id)
#         if not messages:
#             return jsonify({'message': 'message not found'}), 404

#         return jsonify({
#             'id': messages.id,
#             'Message_ID': messages.Message_ID,
#             'Sender_ID': messages.Sender_ID,
#             'Receiver_ID': messages.Receiver_ID,
#             'message_sent': messages.message_sent,
#             'blong': messages.blong,
#             'created_at': messages.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#             'updated_at': messages.updated_at.strftime('%Y-%m-%d %H:%M:%S') if messages.updated_at else None
#         }), 200

#     except Exception as e:
#         return jsonify({'message': 'Failed to retrieve messages', 'error': str(e)}), 500

# # Update a messages by ID
# @message_bp.route('/<int:id>', methods=['PUT'])
# def update_post(id):
#     try:
#         data = request.get_json()
#         messages = message.query.get(id)
#         if not messages:
#             return jsonify({'message': 'message not found'}), 404

#         messages.Message_ID = data.get('Message_ID', messages.Message_ID)
#         messages.Sender_ID = data.get('Sender_ID', messages.Sender_ID)
#         messages.Receiver_ID = data.get('Receiver_ID', messages.Receiver_ID)
#         messages.message_sent = data.get('message_sent', messages.message_sent)
#         messages.blong = data.get('blong', messages.blong)
#         messages.updated_at = datetime.now()

#         db.session.commit()
#         return jsonify({'message': 'message updated successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to update messages', 'error': str(e)}), 500

# # Delete a messages by ID
# @message_bp.route('/<int:id>', methods=['DELETE'])
# def delete_post(id):
#     try:
#         messages = message.query.get(id)
#         if not messages:
#             return jsonify({'message': 'message not found'}), 404

#         db.session.delete(messages)
#         db.session.commit()
#         return jsonify({'message': 'message deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Failed to delete messages', 'error': str(e)}), 500
