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


