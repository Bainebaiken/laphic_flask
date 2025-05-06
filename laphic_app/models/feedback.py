# from datetime import datetime
# from laphic_app.extensions import db

# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'

#     Feedback_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     Rating = db.Column(db.Float, nullable=False)
#     Comment = db.Column(db.Text, nullable=True)
#     Feedback_Date = db.Column(db.DateTime, default=datetime.utcnow)


#     def __init__(self, User_ID, Rating, Comment, Feedback_Date=None):
#         self.User_ID = User_ID
#         self.Rating = Rating
#         self.Comment = Comment
#         if Feedback_Date:
#             self.Feedback_Date = Feedback_Date


#     def __repr__(self):
#         return f"<Feedback {self.Feedback_ID}>"



from datetime import datetime
from laphic_app.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    feedback_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship to User model
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

    def __init__(self, user_id, name, email, comment, rating, image_url=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.comment = comment
        self.rating = rating
        self.image_url = image_url

    def __repr__(self):
        return f"<Feedback {self.feedback_id}>"