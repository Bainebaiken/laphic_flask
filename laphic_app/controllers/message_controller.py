# # from mailbox import Message
# # from flask import Blueprint, request, jsonify
# # from laphic_app.extensions import db
# # from laphic_app.models import message  
# # from flask_jwt_extended import jwt_required, get_jwt_identity
# # from datetime import datetime

# # # Define a Blueprint for messages-related routes
# # message_bp = Blueprint('messages', __name__, url_prefix='/api/v1/messages')  # Adjusted Blueprint definition


# # # Edit a message
# # @message_bp.route('/<int:message_id>/edit', methods=['PUT'])
# # @jwt_required()
# # def edit_message(message_id):
# #     try:
# #         user_info = get_jwt_identity()  # Get the identity of the logged-in user
# #         data = request.get_json()
# #         new_content = data.get('content')

# #         if not new_content:
# #             return jsonify({'error': 'Message content is required'}), 400

# #         # Retrieve the message
# #         message = message.query.get(message_id)
# #         if not message:
# #             return jsonify({'error': 'Message not found'}), 404

# #         # Check if the user is the owner of the message
# #         if message.sender_id != user_info['id']:
# #             return jsonify({'error': 'You can only edit your own messages'}), 403

# #         # Update the message content
# #         message.content = new_content
# #         db.session.commit()

# #         return jsonify({'message': 'Message updated successfully', 'data': {'id': message.id, 'content': message.content}}), 200

# #     except Exception as e:
# #         db.session.rollback()
# #         return jsonify({'error': str(e)}), 500

# # # Delete a message (Provider only)
# # @message_bp.route('/<int:message_id>/delete', methods=['DELETE'])
# # @jwt_required()
# # def delete_message(message_id):
# #     try:
# #         user_info = get_jwt_identity()  # Get the identity of the logged-in user

# #         # Ensure the user is a provider
# #         if user_info['role'] != 'provider':
# #             return jsonify({'error': 'Only providers can delete messages'}), 403

# #         # Retrieve the message
# #         message = Message.query.get(message_id)
# #         if not message:
# #             return jsonify({'error': 'Message not found'}), 404

# #         # Delete the message
# #         db.session.delete(message)
# #         db.session.commit()

# #         return jsonify({'message': 'Message deleted successfully'}), 200

# #     except Exception as e:
# #         db.session.rollback()
# #         return jsonify({'error': str(e)}), 500


# from flask import Blueprint, request, jsonify
# from laphic_app.extensions import db
# from laphic_app.models import Message, User  # Assuming User model exists
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from datetime import datetime
# from flask_socketio import SocketIO, emit

# # Initialize SocketIO (assuming it's set up in your main app)
# socketio = SocketIO()

# # Define a Blueprint for messages-related routes
# message_bp = Blueprint('messages', __name__, url_prefix='/api/v1/messages')

# # Create a new message
# @message_bp.route('/create', methods=['POST'])
# @jwt_required()
# def create_message():
#     try:
#         user_info = get_jwt_identity()  # Get the identity of the logged-in user
#         data = request.get_json()
#         content = data.get('content')
#         recipient_id = data.get('recipient_id')

#         # Validate input
#         if not content or not isinstance(content, str) or len(content.strip()) == 0:
#             return jsonify({'error': 'Message content must be a non-empty string'}), 400
#         if len(content) > 2000:  # Example max length
#             return jsonify({'error': 'Message content exceeds maximum length'}), 400
#         if not recipient_id or not isinstance(recipient_id, int):
#             return jsonify({'error': 'Valid recipient_id is required'}), 400

#         # Check if the recipient exists
#         recipient = User.query.get(recipient_id)
#         if not recipient:
#             return jsonify({'error': 'Recipient not found'}), 404
#         if recipient_id == user_info['id']:
#             return jsonify({'error': 'You cannot send a message to yourself'}), 400

#         # Create new message
#         message = Message(
#             content=content.strip(),
#             sender_id=user_info['id'],
#             recipient_id=recipient_id,
#             created_at=datetime.utcnow()
#         )
#         db.session.add(message)
#         db.session.commit()

#         # Emit WebSocket event to notify the recipient and sender
#         conversation_id = f"chat_{min(user_info['id'], recipient_id)}_{max(user_info['id'], recipient_id)}"
#         socketio.emit('new_message', {
#             'id': message.id,
#             'content': message.content,
#             'sender_id': message.sender_id,
#             'recipient_id': message.recipient_id,
#             'created_at': message.created_at.isoformat()
#         }, room=conversation_id)

#         return jsonify({
#             'message': 'Message created successfully',
#             'data': {
#                 'id': message.id,
#                 'content': message.content,
#                 'sender_id': message.sender_id,
#                 'recipient_id': message.recipient_id,
#                 'created_at': message.created_at.isoformat()
#             }
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An error occurred while creating the message'}), 500

# # Edit a message
# @message_bp.route('/<int:message_id>/edit', methods=['PUT'])
# @jwt_required()
# def edit_message(message_id):
#     try:
#         user_info = get_jwt_identity()
#         data = request.get_json()
#         new_content = data.get('content')

#         # Validate content
#         if not new_content or not isinstance(new_content, str) or len(new_content.strip()) == 0:
#             return jsonify({'error': 'Message content must be a non-empty string'}), 400
#         if len(new_content) > 2000:
#             return jsonify({'error': 'Message content exceeds maximum length'}), 400

#         # Retrieve the message
#         message = Message.query.get(message_id)
#         if not message:
#             return jsonify({'error': 'Message not found'}), 404

#         # Check if the user is the owner of the message
#         if message.sender_id != user_info['id']:
#             return jsonify({'error': 'You can only edit your own messages'}), 403

#         # Update the message content and timestamp
#         message.content = new_content.strip()
#         message.updated_at = datetime.utcnow()
#         db.session.commit()

#         # Emit WebSocket event to notify conversation participants
#         conversation_id = f"chat_{min(message.sender_id, message.recipient_id)}_{max(message.sender_id, message.recipient_id)}"
#         socketio.emit('message_updated', {
#             'id': message.id,
#             'content': message.content,
#             'sender_id': message.sender_id,
#             'recipient_id': message.recipient_id,
#             'updated_at': message.updated_at.isoformat()
#         }, room=conversation_id)

#         return jsonify({
#             'message': 'Message updated successfully',
#             'data': {
#                 'id': message.id,
#                 'content': message.content,
#                 'updated_at': message.updated_at.isoformat()
#             }
#         }), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An error occurred while updating the message'}), 500

# # Delete a message (Provider or message owner)
# @message_bp.route('/<int:message_id>/delete', methods=['DELETE'])
# @jwt_required()
# def delete_message(message_id):
#     try:
#         user_info = get_jwt_identity()

#         # Retrieve the message
#         message = Message.query.get(message_id)
#         if not message:
#             return jsonify({'error': 'Message not found'}), 404

#         # Allow deletion by message owner or provider
#         if message.sender_id != user_info['id'] and user_info['role'] != 'provider':
#             return jsonify({'error': 'You can only delete your own messages or messages as a provider'}), 403

#         # Store conversation_id for WebSocket event
#         conversation_id = f"chat_{min(message.sender_id, message.recipient_id)}_{max(message.sender_id, message.recipient_id)}"
#         db.session.delete(message)
#         db.session.commit()

#         # Emit WebSocket event to notify conversation participants
#         socketio.emit('message_deleted', {
#             'id': message_id,
#             'sender_id': message.sender_id,
#             'recipient_id': message.recipient_id
#         }, room=conversation_id)

#         return jsonify({'message': 'Message deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An error occurred while deleting the message'}), 500
    

# @message_bp.route('/conversation/<int:other_user_id>', methods=['GET'])
# @jwt_required()
# def get_conversation_messages(other_user_id):
#     try:
#         user_info = get_jwt_identity()
#         if other_user_id == user_info['id']:
#             return jsonify({'error': 'You cannot view a conversation with yourself'}), 400

#         # Check if the other user exists
#         other_user = User.query.get(other_user_id)
#         if not other_user:
#             return jsonify({'error': 'User not found'}), 404

#         # Get messages where user is sender or recipient
#         page = request.args.get('page', 1, type=int)
#         per_page = request.args.get('per_page', 20, type=int)
#         messages = Message.query.filter(
#             ((Message.sender_id == user_info['id']) & (Message.recipient_id == other_user_id)) |
#             ((Message.sender_id == other_user_id) & (Message.recipient_id == user_info['id']))
#         ).order_by(Message.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

#         return jsonify({
#             'messages': [{
#                 'id': m.id,
#                 'content': m.content,
#                 'sender_id': m.sender_id,
#                 'recipient_id': m.recipient_id,
#                 'created_at': m.created_at.isoformat(),
#                 'updated_at': m.updated_at.isoformat() if m.updated_at else None
#             } for m in messages.items],
#             'total': messages.total,
#             'pages': messages.pages,
#             'current_page': messages.page
#         }), 200

#     except Exception as e:
#         return jsonify({'error': 'An error occurred while retrieving messages'}), 500    



from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from laphic_app.controllers.firebase_chat_service import FirebaseChatService
from laphic_app.models.user import User

message_bp = Blueprint('message', __name__, url_prefix='/api/messages')

@message_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send a message"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        receiver_id = data.get('receiver_id')
        message_text = data.get('message')
        message_type = data.get('message_type', 'text')
        
        if not receiver_id or not message_text:
            return jsonify({'error': 'receiver_id and message are required'}), 400
        
        # Check if receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            return jsonify({'error': 'Receiver not found'}), 404
        
        # Send message via Firebase
        message_data = FirebaseChatService.send_message(
            sender_id=current_user['id'],
            receiver_id=receiver_id,
            message_text=message_text,
            message_type=message_type
        )
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully',
            'data': message_data
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@message_bp.route('/chat/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_chat_messages(other_user_id):
    """Get messages for a chat with another user"""
    try:
        current_user = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)
        
        # Check if other user exists
        other_user = User.query.get(other_user_id)
        if not other_user:
            return jsonify({'error': 'User not found'}), 404
        
        messages = FirebaseChatService.get_chat_messages(
            user1_id=current_user['id'],
            user2_id=other_user_id,
            limit=limit
        )
        
        # Mark messages as read
        chat_id = FirebaseChatService.generate_chat_id(current_user['id'], other_user_id)
        FirebaseChatService.mark_messages_as_read(chat_id, current_user['id'])
        
        return jsonify({
            'success': True,
            'messages': messages,
            'other_user': {
                'id': other_user.id,
                'username': other_user.username,
                'email': other_user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@message_bp.route('/chats', methods=['GET'])
@jwt_required()
def get_user_chats():
    """Get all chats for current user"""
    try:
        current_user = get_jwt_identity()
        
        chats = FirebaseChatService.get_user_chats(current_user['id'])
        
        # Enhance with user information
        enhanced_chats = []
        for chat in chats:
            if chat['other_user_id']:
                other_user = User.query.get(chat['other_user_id'])
                if other_user:
                    enhanced_chats.append({
                        **chat,
                        'other_user': {
                            'id': other_user.id,
                            'username': other_user.username,
                            'email': other_user.email
                        }
                    })
        
        return jsonify({
            'success': True,
            'chats': enhanced_chats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@message_bp.route('/delete/<string:chat_id>/<string:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(chat_id, message_id):
    """Delete a message"""
    try:
        current_user = get_jwt_identity()
        
        success = FirebaseChatService.delete_message(chat_id, message_id, current_user['id'])
        
        if success:
            return jsonify({'success': True, 'message': 'Message deleted'}), 200
        else:
            return jsonify({'error': 'Cannot delete message'}), 403
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500