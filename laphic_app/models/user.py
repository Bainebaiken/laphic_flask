

from laphic_app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), default='user')
    profile_image = db.Column(db.String(255), nullable=True)  # Added, optional field

    # Fixed relationships
    messages_sent = db.relationship(
        'Message',
        foreign_keys='Message.sender_id',
        primaryjoin="and_(User.user_id == Message.sender_id, Message.sender_type == 'user')",
        back_populates='sender_user',
        lazy='dynamic'
    )
    messages_received = db.relationship(
        'Message',
        foreign_keys='Message.recipient_id',
        primaryjoin="and_(User.user_id == Message.recipient_id, Message.recipient_type == 'user')",
        back_populates='recipient_user',
        lazy='dynamic'
    )
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'user_type': self.user_type,
            'profile_image': self.profile_image  # Added to return profile image in API responses
        }