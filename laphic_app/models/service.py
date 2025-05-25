from datetime import datetime
from laphic_app.extensions import db

class Service(db.Model):
    __tablename__ = 'services'

    Service_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Category = db.Column(db.String(50), nullable=False)
    Image_URL = db.Column(db.String(255), nullable=True)

    # Relationships
    bookings = db.relationship('Booking', backref='service', lazy=True)
    gallery_images = db.relationship('Gallery', backref='service', lazy=True)

    def __repr__(self):
        return f"<Service {self.Name}>"



# from datetime import datetime
# from laphic_app.extensions import db

# class Service(db.Model):
#     __tablename__ = 'services'
#     Service_ID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Category = db.Column(db.String(50), nullable=False)  # e.g., 'renovation', 'construction'
#     Description = db.Column(db.Text, nullable=True)
#     Cost = db.Column(db.Float, nullable=False)

#     # Relationships
#     feedbacks = db.relationship('Feedback', backref='service', lazy=True)
#     bookings = db.relationship('Booking', backref='service', lazy=True)

#     def __repr__(self):
#         return f"<Service {self.Name}>"



# # from datetime import datetime
# # from laphic_app.extensions import db


# # class Service(db.Model):
# #     __tablename__ = 'services'
# #     Service_ID = db.Column(db.Integer, primary_key=True)
# #     Name = db.Column(db.String(100), nullable=False)
# #     Category = db.Column(db.String(50), nullable=False)  # e.g., 'renovation', 'construction', 'painting'
# #     Description = db.Column(db.Text, nullable=True)
# #     Cost = db.Column(db.Float, nullable=False)
# #     bookings = db.relationship('Booking', backref='service', lazy=True)
# #     feedbacks = db.relationship('Feedback', backref='service', lazy=True)

# #     def __init__(self, Service_ID , Name ,Category ,Description ,Cost , ):
# #         self.SerService_ID =Service_ID
# #         self.Name = Name
# #         self.Category = Category
# #         self.Description = Description
# #         self.Cost = Cost

# #     def __repr__(self):
# #         return f'<Post {self.SerService_ID}>'









