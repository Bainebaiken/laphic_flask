from datetime import datetime
from laphic_app.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    Booking_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Change to lowercase user_id
    Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
    Booking_Date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    Schedule_Date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Booking {self.Booking_ID}>"


# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from laphic_app.extensions import db



# class Booking(db.Model):
#     __tablename__ = 'bookings'

#     Booking_ID = db.Column(db.Integer, primary_key=True)  # Set as primary key
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)  # Foreign key to users
#     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)  # Foreign key to services
#     Booking_Date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Auto default to current timestamp
#     Schedule_Date = db.Column(db.DateTime, nullable=False)

#     # Relationships (optional, depending on your needs)
#     user = db.relationship('User', backref='bookings', lazy=True)
#     service = db.relationship('Service', backref='bookings', lazy=True)

#     def __init__(self, User_ID, Service_ID, Schedule_Date):
#         self.User_ID = User_ID
#         self.Service_ID = Service_ID
#         self.Schedule_Date = Schedule_Date

#     def __repr__(self):
#         return f"<Booking {self.Booking_ID}>"


# class Booking(db.Model):
#     __tablename__ = 'bookings'

   
#     Booking_ID = db.Column(db.Integer, nullable=False)
#     User_ID = db.Column(db.Integer, nullable=False)
#     Service_ID = db.Column(db.Integer, nullable=False)
#     Booking_Date = db.Column(db.DateTime, nullable=False)
#     Schedule_Date = db.Column(db.DateTime, nullable=False)  # Ensure this is defined
#     date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
#     # bookings = db.relationship('Booking', backref='user', lazy=True)
    
    

#     def __init__(self, Booking_ID, User_ID, Service_ID, Booking_Date, Schedule_Date):
#         self.Booking_ID = Booking_ID
#         self.User_ID = User_ID
#         self.Service_ID = Service_ID
#         self.Booking_Date = Booking_Date
#         self.Schedule_Date = Schedule_Date

#         def __repr__(self):
#           return f"<Booking {self.Booking_ID}>"

# class Booking(db.Model):
#     __tablename__ = 'bookings'
#     Booking_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
#     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
#     Booking_Date = db.Column(db.DateTime, default=datetime.utcnow)
#     Scheduled_Date = db.Column(db.DateTime, nullable=False)


#     def __init__(self, Booking_ID , User_ID ,Service_ID ,Booking_Date ,Scheduled_date ):
#         self.Booking_ID  = Booking_ID 
#         self.User_ID = User_ID
#         self.Service_ID  = Service_ID
#         self.Booking_Date = Booking_Date
#         self.Scheduled_Date = Scheduled_date

#     def __repr__(self):
#         return f"<Booking {self.Booking_ID}>"


# # class Booking(db.Model):
# #     __tablename__ = 'bookings'
# #     Booking_ID = db.Column(db.Integer, primary_key=True)
# #     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
# #     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
# #     Booking_Date = db.Column(db.DateTime, default=datetime.utcnow)
# #     Scheduled_Date = db.Column(db.DateTime, nullable=False)
# #     # Status = db.Column(db.String(20), nullable=False)  # e.g., 'pending', 'confirmed', 'completed'
# #     # Payment_Status = db.Column(db.String(20), nullable=False)  # e.g., 'paid', 'unpaid'


# #     def __init__(self, Booking_ID , User_ID ,Service_ID ,Booking_Date ,Scheduled_date ):
# #         self.Booking_ID  = Booking_ID 
#         self.User_ID = User_ID
#         self.Service_ID  = Service_ID
#         self.Booking_Date = Booking_Date
#         self.Scheduled_Date = Scheduled_date

#     def __repr__(self):
#         return f'<Category {self.Booking_ID }>'




