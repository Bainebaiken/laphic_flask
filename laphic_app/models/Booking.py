# from datetime import datetime
# from laphic_app.extensions import db

# class Booking(db.Model):
#     __tablename__ = 'bookings'

#     Booking_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Change to lowercase user_id
#     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
#     Booking_Date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     Schedule_Date = db.Column(db.DateTime, nullable=False)

#     def __repr__(self):
#         return f"<Booking {self.Booking_ID}>"


from datetime import datetime

from laphic_app.extensions import db



class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
    selected_date = db.Column(db.String(20), nullable=False)
    selected_time = db.Column(db.String(10), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.id} for {self.name}>'