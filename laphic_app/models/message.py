from datetime import datetime
from laphic_app.extensions import db

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, nullable=False)  # Polymorphic, no direct ForeignKey
    sender_type = db.Column(db.String(10), nullable=False)  # 'user' or 'provider'
    recipient_id = db.Column(db.Integer, nullable=False)  # Polymorphic, no direct ForeignKey
    recipient_type = db.Column(db.String(10), nullable=False)  # 'user' or 'provider'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships with User
    sender_user = db.relationship(
        'User',
        foreign_keys=[sender_id],
        primaryjoin="and_(Message.sender_id == User.user_id, Message.sender_type == 'user')",
        back_populates='messages_sent'
    )
    recipient_user = db.relationship(
        'User',
        foreign_keys=[recipient_id],
        primaryjoin="and_(Message.recipient_id == User.user_id, Message.recipient_type == 'user')",
        back_populates='messages_received'
    )

    # Relationships with Provider
    sender_provider = db.relationship(
        'Provider',
        foreign_keys=[sender_id],
        primaryjoin="and_(Message.sender_id == Provider.Provider_ID, Message.sender_type == 'provider')",
        back_populates='messages_sent'
    )
    recipient_provider = db.relationship(
        'Provider',
        foreign_keys=[recipient_id],
        primaryjoin="and_(Message.recipient_id == Provider.Provider_ID, Message.recipient_type == 'provider')",
        back_populates='messages_received'
    )

    def __init__(self, sender_id, sender_type, recipient_id, recipient_type, content):
        self.sender_id = sender_id
        self.sender_type = sender_type
        self.recipient_id = recipient_id
        self.recipient_type = recipient_type
        self.content = content

    def __repr__(self):
        return f"<Message {self.message_id}>"
