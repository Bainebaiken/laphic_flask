from firebase_admin import db
from datetime import datetime
import uuid
from typing import List, Dict, Optional

class FirebaseChatService:
    
    @staticmethod
    def generate_chat_id(user1_id: int, user2_id: int) -> str:
        """Generate consistent chat ID for two users"""
        return f"chat_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"
    
    @staticmethod
    def send_message(sender_id: int, receiver_id: int, message_text: str, message_type: str = 'text') -> Dict:
        """Send a message to Firebase"""
        chat_id = FirebaseChatService.generate_chat_id(sender_id, receiver_id)
        message_id = str(uuid.uuid4())
        
        message_data = {
            'id': message_id,
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message_text,
            'message_type': message_type,  # 'text', 'image', 'file'
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'delivered': True
        }
        
        # Save message to Firebase
        chat_ref = db.reference(f'chats/{chat_id}')
        
        # Update chat metadata
        chat_ref.child('metadata').update({
            'last_message': message_text,
            'last_message_time': message_data['timestamp'],
            'last_sender_id': sender_id,
            'participants': [sender_id, receiver_id]
        })
        
        # Add message
        chat_ref.child('messages').child(message_id).set(message_data)
        
        return message_data
    
    @staticmethod
    def get_chat_messages(user1_id: int, user2_id: int, limit: int = 50) -> List[Dict]:
        """Get messages for a chat between two users"""
        chat_id = FirebaseChatService.generate_chat_id(user1_id, user2_id)
        
        messages_ref = db.reference(f'chats/{chat_id}/messages')
        messages = messages_ref.order_by_child('timestamp').limit_to_last(limit).get()
        
        if not messages:
            return []
        
        # Convert to list and sort by timestamp
        message_list = []
        for msg_id, msg_data in messages.items():
            message_list.append(msg_data)
        
        return sorted(message_list, key=lambda x: x['timestamp'])
    
    @staticmethod
    def mark_messages_as_read(chat_id: str, user_id: int):
        """Mark messages as read for a specific user"""
        messages_ref = db.reference(f'chats/{chat_id}/messages')
        messages = messages_ref.get()
        
        if messages:
            for msg_id, msg_data in messages.items():
                if msg_data.get('receiver_id') == user_id and not msg_data.get('read'):
                    messages_ref.child(msg_id).update({'read': True})
    
    @staticmethod
    def get_user_chats(user_id: int) -> List[Dict]:
        """Get all chats for a user"""
        chats_ref = db.reference('chats')
        all_chats = chats_ref.get()
        
        user_chats = []
        if all_chats:
            for chat_id, chat_data in all_chats.items():
                metadata = chat_data.get('metadata', {})
                participants = metadata.get('participants', [])
                
                if user_id in participants:
                    # Get other participant
                    other_user_id = None
                    for participant in participants:
                        if participant != user_id:
                            other_user_id = participant
                            break
                    
                    user_chats.append({
                        'chat_id': chat_id,
                        'other_user_id': other_user_id,
                        'last_message': metadata.get('last_message', ''),
                        'last_message_time': metadata.get('last_message_time', ''),
                        'last_sender_id': metadata.get('last_sender_id')
                    })
        
        # Sort by last message time
        user_chats.sort(key=lambda x: x['last_message_time'], reverse=True)
        return user_chats
    
    @staticmethod
    def delete_message(chat_id: str, message_id: str, user_id: int) -> bool:
        """Delete a message (only sender can delete)"""
        message_ref = db.reference(f'chats/{chat_id}/messages/{message_id}')
        message = message_ref.get()
        
        if message and message.get('sender_id') == user_id:
            message_ref.delete()
            return True
        return False