from datetime import datetime
from laphic_app.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    Feedback_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    Rating = db.Column(db.Float, nullable=False)
    Comment = db.Column(db.Text, nullable=True)
    Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, User_ID, Rating, Comment, Feedback_Date=None):
        self.User_ID = User_ID
        self.Rating = Rating
        self.Comment = Comment
        if Feedback_Date:
            self.Feedback_Date = Feedback_Date


    def __repr__(self):
        return f"<Feedback {self.Feedback_ID}>"



# from datetime import datetime
# from laphic_app.extensions import db

# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'

#     Feedback_ID = db.Column(db.Integer, primary_key=True)
#     # User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     Rating = db.Column(db.Float, nullable=False)
#     Comment = db.Column(db.Text, nullable=True)
#     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationship with User model (changed backref to 'user_feedbacks' to avoid conflict)
#     user = db.relationship('User', backref=db.backref('user_feedbacks', lazy=True))
#     # user = db.relationship('User', backref='bookings')
    
#     def __init__(self, User_ID, Rating, Comment, Feedback_Date=None):
#         self.User_ID = User_ID
#         self.Rating = Rating
#         self.Comment = Comment
#         if Feedback_Date:
#             self.Feedback_Date = Feedback_Date

#     def __repr__(self):
#         return f"<Feedback {self.Feedback_ID}>"


# from datetime import datetime
# from laphic_app.extensions import db

# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'

#     Feedback_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
#     # Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
#     Rating = db.Column(db.Float, nullable=False)
#     Comment = db.Column(db.Text, nullable=True)
#     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationship with User model
#     user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

#     # Relationship with Service model (ensure unique backref name)
#     # service = db.relationship('Service', backref='feedbacks', lazy=True)

#     def __init__(self, User_ID, Rating, Comment, Feedback_Date=None):
#         self.User_ID = User_ID
#         self.Rating = Rating
#         self.Comment = Comment
#         if Feedback_Date:
#             self.Feedback_Date = Feedback_Date

#     def __repr__(self):
#         return f"<Feedback {self.Feedback_ID}>"


 # feedback.py (Feedback model)
# from datetime import datetime
# from laphic_app.extensions import db

# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'

#     Feedback_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
#     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
#     Rating = db.Column(db.Float, nullable=False)
#     Comment = db.Column(db.Text, nullable=True)
#     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationship with User model
#     user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

#     # Relationship with Service model (ensure unique backref name)
#     service = db.relationship('Service', backref=db.backref('related_feedbacks', lazy=True))

#     def __init__(self, User_ID, Service_ID, Rating, Comment, Feedback_Date=None):
#         self.User_ID = User_ID
#         self.Service_ID = Service_ID
#         self.Rating = Rating
#         self.Comment = Comment
#         if Feedback_Date:
#             self.Feedback_Date = Feedback_Date

#     def __repr__(self):
#         return f"<Feedback {self.Feedback_ID}>"


# from datetime import datetime
# from laphic_app.extensions import db


# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'

#     Feedback_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)  # ForeignKey to User model
#     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)  # ForeignKey to Service model
#     Rating = db.Column(db.Float, nullable=False)
#     Comment = db.Column(db.Text, nullable=True)
#     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationship with User model
#     user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

#     # Relationship with Service model (changed backref name to avoid conflict)
#     service = db.relationship('Service', backref=db.backref('service_feedbacks', lazy=True))

#     def __init__(self, User_ID, Service_ID, Rating, Comment, Feedback_Date=None):
#         self.User_ID = User_ID
#         self.Service_ID = Service_ID
#         self.Rating = Rating
#         self.Comment = Comment
#         if Feedback_Date:
#             self.Feedback_Date = Feedback_Date

#     def __repr__(self):
#         return f"<Feedback {self.Feedback_ID}>"




# # class Feedback(db.Model):
# #     __tablename__ = 'feedbacks'

# #     Feedback_ID = db.Column(db.Integer, primary_key=True)
# #     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)  # ForeignKey to User model
# #     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)  # ForeignKey to Service model
# #     Rating = db.Column(db.Float, nullable=False)
# #     Comment = db.Column(db.Text, nullable=True)
# #     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)

# #     # Define the relationship with User model
# #     user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
# #     service = db.relationship('Service', backref=db.backref('feedbacks', lazy=True))

# #     def __init__(self, User_ID, Service_ID, Rating, Comment, Feedback_Date=None):
# #         self.User_ID = User_ID
# #         self.Service_ID = Service_ID
# #         self.Rating = Rating
# #         self.Comment = Comment
# #         if Feedback_Date:
# #             self.Feedback_Date = Feedback_Date

# #     def __repr__(self):
# #         return f"<Feedback {self.Feedback_ID}>"


# # # class Feedback(db.Model):
# # #     __tablename__ = 'feedbacks'

# # #     Feedback_ID = db.Column(db.Integer, primary_key=True)
# # #     User_ID = db.Column(db.Integer, nullable=False)  # ForeignKey if User model exists
# # #     Service_ID = db.Column(db.Integer, nullable=False)  # ForeignKey if Service model exists
# # #     Rating = db.Column(db.Float, nullable=False)
# # #     Comment = db.Column(db.Text, nullable=True)
# # #     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)

# # #     def __init__(self, User_ID, Service_ID, Rating, Comment, Feedback_Date=None):
# # #         self.User_ID = User_ID
# # #         self.Service_ID = Service_ID
# # #         self.Rating = Rating
# # #         self.Comment = Comment
# # #         if Feedback_Date:
# # #             self.Feedback_Date = Feedback_Date

# # #     def __repr__(self):
# # #         return f"<Feedback {self.Feedback_ID}>"




# # # from datetime import datetime
# # # from flask_sqlalchemy import SQLAlchemy
# # # from laphic_app.extensions import db

# # # class Feedback(db.Model):
# # #     __tablename__ = 'feedbacks'
# # #     Feedback_ID = db.Column(db.Integer, primary_key=True)
# # #     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
# # #     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
# # #     Rating = db.Column(db.Integer, nullable=False)
# # #     Comment = db.Column(db.Text, nullable=True)
# # #     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)



# # #     def __init__(self,  Feedback_ID,User_ID, Service_ID, Rating, Comment, Feedback_Date=None):
# # #         self.Feedback_ID = Feedback_ID
# # #         self.User_ID = User_ID
# # #         self.Service_ID = Service_ID
# # #         self.Rating = Rating
# # #         self.Comment = Comment
# # #         if Feedback_Date:
# # #             self.Feedback_Date = Feedback_Date

# # #     def __repr__(self):
# # #         return f"<Feedback {self.Feedback_ID}>"


# # # # class Feedback(db.Model):
# # # #     __tablename__ = 'feedbacks'
# # # #     Feedback_ID = db.Column(db.Integer, primary_key=True)
# # # #     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
# # # #     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=False)
# # # #     Rating = db.Column(db.Integer, nullable=False)
# # # #     Comment = db.Column(db.Text, nullable=True)
# # # #     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)