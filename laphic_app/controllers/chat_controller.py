from flask import Blueprint, request, jsonify
from laphic_app.extensions import db
from laphic_app.models import User, Provider, Message
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Define a Blueprint for chat-related routes
chat_bp = Blueprint('chat', __name__, url_prefix='/api/v1/chat')

# Send a message
@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    try:
        # Get sender info from JWT
        sender = get_jwt_identity()
        sender_id = sender['id']
        sender_type = sender['role']  # 'user' or 'provider'

        # Get message data from the request
        data = request.get_json()
        recipient_id = data.get('recipient_id')
        recipient_type = data.get('recipient_type')  # 'user' or 'provider'
        content = data.get('content')

        if not recipient_id or not recipient_type or not content:
            return jsonify({'error': 'All fields are required: recipient_id, recipient_type, content'}), 400

        # Create a new message
        new_message = Message(
            sender_id=sender_id,
            sender_type=sender_type,
            recipient_id=recipient_id,
            recipient_type=recipient_type,
            content=content
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({'message': 'Message sent successfully', 'message_id': new_message.Message_ID}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send message', 'details': str(e)}), 500

# Retrieve chat history between a user and a provider
@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    try:
        # Get current user info from JWT
        current_user = get_jwt_identity()
        current_user_id = current_user['id']
        current_user_role = current_user['role']  # 'user' or 'provider'

        # Get recipient info from query parameters
        recipient_id = request.args.get('recipient_id')
        recipient_type = request.args.get('recipient_type')  # 'user' or 'provider'

        if not recipient_id or not recipient_type:
            return jsonify({'error': 'Both recipient_id and recipient_type are required'}), 400

        # Retrieve chat history
        messages = Message.query.filter(
            ((Message.sender_id == current_user_id) & (Message.sender_type == current_user_role) &
             (Message.recipient_id == recipient_id) & (Message.recipient_type == recipient_type)) |
            ((Message.sender_id == recipient_id) & (Message.sender_type == recipient_type) &
             (Message.recipient_id == current_user_id) & (Message.recipient_type == current_user_role))
        ).order_by(Message.timestamp).all()

        # Serialize the messages
        chat_history = [
            {
                'Message_ID': msg.Message_ID,
                'sender_id': msg.sender_id,
                'sender_type': msg.sender_type,
                'recipient_id': msg.recipient_id,
                'recipient_type': msg.recipient_type,
                'content': msg.content,
                'timestamp': msg.timestamp
            } for msg in messages
        ]

        return jsonify({'chat_history': chat_history}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve chat history', 'details': str(e)}), 500
