from laphic_app.extensions import db

class Provider(db.Model):
    __tablename__ = 'providers'

    Provider_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Contact = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Address = db.Column(db.String(200), nullable=True)
    Password = db.Column(db.String(100), nullable=False)

    messages_sent = db.relationship(
        'Message',
        foreign_keys='Message.sender_id',
        primaryjoin="and_(Provider.Provider_ID == Message.sender_id, Message.sender_type == 'provider')",
        back_populates='sender_provider',
        lazy='dynamic'
    )
    messages_received = db.relationship(
        'Message',
        foreign_keys='Message.recipient_id',
        primaryjoin="and_(Provider.Provider_ID == Message.recipient_id, Message.recipient_type == 'provider')",
        back_populates='recipient_provider',
        lazy='dynamic'
    )

    def __repr__(self):
        return f"<Provider {self.Name}>"




