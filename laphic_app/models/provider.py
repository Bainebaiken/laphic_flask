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




# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from laphic_app.extensions import db


# class Provider(db.Model):
#     __tablename__ = 'providers'

#     Provider_ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Contact = db.Column(db.String(20), nullable=False)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Address = db.Column(db.String(200), nullable=True)
#     Password = db.Column(db.String(100), nullable=False)

#     # Relationships
#     messages_sent = db.relationship(
#         'Message',
#         foreign_keys='Message.sender_id',
#         primaryjoin="and_(Provider.Provider_ID == Message.sender_id, Message.sender_type == 'provider')",
#         backref='sender_provider',
#         lazy='dynamic'
#     )
#     messages_received = db.relationship(
#         'Message',
#         foreign_keys='Message.recipient_id',
#         primaryjoin="and_(Provider.Provider_ID == Message.recipient_id, Message.recipient_type == 'provider')",
#         backref='recipient_provider',
#         lazy='dynamic'
#     )

#     def __repr__(self):
#         return f"<Provider {self.Name}>"



# class Provider(db.Model):
#     __tablename__ = 'providers'
#     Provider_ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Contact = db.Column(db.String(20), nullable=False)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Address = db.Column(db.String(200), nullable=True)
#     Password = db.Column(db.String(100), nullable=False)

#     # Relationships
#     messages_sent = db.relationship(
#         'Message',
#         foreign_keys='Message.Sender_ID',
#         backref='sent_by_provider',  # Unique backref for Provider
#         lazy='dynamic',
#         primaryjoin='Provider.Provider_ID == Message.Sender_ID'
#     )
#     messages_received = db.relationship(
#         'Message',
#         foreign_keys='Message.Receiver_ID',
#         backref='received_by_provider',  # Unique backref for Provider
#         lazy='dynamic',
#         primaryjoin='Provider.Provider_ID == Message.Receiver_ID'
#     )

#     def __repr__(self):
#         return f"<Provider {self.Name}>"


# class Provider(db.Model):
#     __tablename__ = 'providers'
#     Provider_ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Contact = db.Column(db.String(20), nullable=False)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Address = db.Column(db.String(200), nullable=True)
#     Password = db.Column(db.String(100), nullable=False)

#     # Relationships
#     messages_sent = db.relationship(
#         'Message',
#         foreign_keys='Message.Sender_ID',
#         backref='sent_by_provider',  # Unique backref for Provider
#         lazy=True,
#         primaryjoin='Message.Sender_ID == Provider.Provider_ID'
#     )
#     messages_received = db.relationship(
#         'Message',
#         foreign_keys='Message.Receiver_ID',
#         backref='received_by_provider',  # Unique backref for Provider
#         lazy=True,
#         primaryjoin='Message.Receiver_ID == Provider.Provider_ID'
#     )

#     def __repr__(self):
#         return f"<Provider {self.Name}>"



# # class Provider(db.Model):
# #     __tablename__ = 'providers'
# #     Provider_ID = db.Column(db.Integer, primary_key=True)
# #     Name = db.Column(db.String(100), nullable=False)
# #     Contact = db.Column(db.String(20), nullable=False)
# #     Email = db.Column(db.String(100), unique=True, nullable=False)
# #     Address = db.Column(db.String(200), nullable=True)
# #     Password = db.Column(db.String(100), nullable=False)

#     # Relationships
#     # Use primaryjoin to explicitly define the relationship condition
#     messages_sent = db.relationship(
#         'Message',
#         foreign_keys='Message.Sender_ID',  # Link to Sender_ID in the Message model
#         backref='provider_sender',  # Backref to refer to the provider
#         lazy=True,
#         primaryjoin='Message.Sender_ID == Provider.Provider_ID'  # Explicit join condition
#     )
#     messages_received = db.relationship(
#         'Message',
#         foreign_keys='Message.Receiver_ID',  # Link to Receiver_ID in the Message model
#         backref='provider_receiver',  # Backref to refer to the provider
#         lazy=True,
#         primaryjoin='Message.Receiver_ID == Provider.Provider_ID'  # Explicit join condition
#     )

#     def __repr__(self):
#         return f"<Provider {self.Name}>"


# class Provider(db.Model):
#     __tablename__ = 'providers'
#     Provider_ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Contact = db.Column(db.String(20), nullable=False)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Address = db.Column(db.String(200), nullable=True)
#     Password = db.Column(db.String(100), nullable=False)

#     # Relationships
#     # Add ForeignKey constraint to link Message.Sender_ID to Provider.Provider_ID
#     messages_sent = db.relationship('Message', foreign_keys='Message.Sender_ID', backref='provider_sender', lazy=True)
#     messages_received = db.relationship('Message', foreign_keys='Message.Receiver_ID', backref='provider_receiver', lazy=True)

#     def __repr__(self):
#         return f"<Provider {self.Name}>"


# class Provider(db.Model):
#     __tablename__ = 'providers'
#     Provider_ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Contact = db.Column(db.String(20), nullable=False)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Address = db.Column(db.String(200), nullable=True)
#     Password = db.Column(db.String(100), nullable=False)

#     # Relationships
#     messages_sent = db.relationship('Message', foreign_keys='Message.Sender_ID', backref='provider_sender', lazy=True)
#     messages_received = db.relationship('Message', foreign_keys='Message.Receiver_ID', backref='provider_receiver', lazy=True)

#     def __repr__(self):
#         return f"<Provider {self.Name}>"


# # Provider Model
# class Provider(db.Model):
#     __tablename__ = 'providers'
#     Provider_ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Contact = db.Column(db.String(20), nullable=False)
#     messages_sent = db.relationship('Message', foreign_keys='Message.Sender_ID', backref='provider_sender', lazy=True)
#     messages_received = db.relationship('Message', foreign_keys='Message.Receiver_ID', backref='provider_receiver', lazy=True)

#     def __init__(self, Provider_ID, Name, Contact ,messages_sent,messages_received):
#         self.messages_sent = messages_sent
#         self.Provider_ID = Provider_ID
#         self.Name = Name
#         self.messages_received = messages_received

#     def __repr__(self):
#         return f'<Article {self.Provider_ID}>'

