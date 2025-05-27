# 

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

@message_bp.route('/admin/send', methods=['POST'])
@jwt_required()
def admin_send_message():
    """Admin send message to any user"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('user_type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        receiver_id = data.get('receiver_id')
        message_text = data.get('message')
        
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
            message_type='text'
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

@message_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_users_for_admin_chat():
    """Get all users that admin can chat with"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('user_type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get all users except current admin and other admins
        users = User.query.filter(
            User.id != current_user['id'],
            User.user_type != 'admin'
        ).all()
        
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify({
            'success': True,
            'users': users_data
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

@message_bp.route('/admin/chats', methods=['GET'])
@jwt_required()
def get_admin_chats():
    """Get all chats for admin with additional metadata"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('user_type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        chats = FirebaseChatService.get_user_chats(current_user['id'])
        
        # Enhance with user information and chat statistics
        enhanced_chats = []
        for chat in chats:
            if chat['other_user_id']:
                other_user = User.query.get(chat['other_user_id'])
                if other_user:
                    # Get unread count for admin
                    unread_count = FirebaseChatService.get_unread_count(
                        chat['chat_id'], 
                        current_user['id']
                    )
                    
                    enhanced_chats.append({
                        **chat,
                        'other_user': {
                            'id': other_user.id,
                            'username': other_user.username,
                            'email': other_user.email,
                            'user_type': other_user.user_type
                        },
                        'unread_count': unread_count
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

@message_bp.route('/admin/broadcast', methods=['POST'])
@jwt_required()
def admin_broadcast_message():
    """Admin broadcast message to multiple users"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('user_type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        message_text = data.get('message')
        
        if not user_ids or not message_text:
            return jsonify({'error': 'user_ids and message are required'}), 400
        
        sent_messages = []
        failed_messages = []
        
        for user_id in user_ids:
            try:
                # Check if receiver exists
                receiver = User.query.get(user_id)
                if not receiver:
                    failed_messages.append({'user_id': user_id, 'error': 'User not found'})
                    continue
                
                # Send message via Firebase
                message_data = FirebaseChatService.send_message(
                    sender_id=current_user['id'],
                    receiver_id=user_id,
                    message_text=message_text,
                    message_type='text'
                )
                
                sent_messages.append({
                    'user_id': user_id,
                    'message_data': message_data
                })
                
            except Exception as e:
                failed_messages.append({
                    'user_id': user_id,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'message': 'Broadcast completed',
            'sent_count': len(sent_messages),
            'failed_count': len(failed_messages),
            'sent_messages': sent_messages,
            'failed_messages': failed_messages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@message_bp.route('/admin/stats', methods=['GET'])
@jwt_required()
def get_admin_chat_stats():
    """Get chat statistics for admin dashboard"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('user_type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        stats = FirebaseChatService.get_admin_chat_stats(current_user['id'])
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500