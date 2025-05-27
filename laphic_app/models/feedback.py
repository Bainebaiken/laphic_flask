



# from datetime import datetime
# from laphic_app.extensions import db

# class Feedback(db.Model):
#     __tablename__ = 'feedbacks'

#     feedback_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     comment = db.Column(db.Text, nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     image_url = db.Column(db.String(500), nullable=True)
#     feedback_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     # Relationship to User model
#     user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

#     def __init__(self, user_id, name, email, comment, rating, image_url=None):
#         self.user_id = user_id
#         self.name = name
#         self.email = email
#         self.comment = comment
#         self.rating = rating
#         self.image_url = image_url

#     def __repr__(self):
#         return f"<Feedback {self.feedback_id}>"




from datetime import datetime
from laphic_app.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=True)  # Added subject field
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    feedback_type = db.Column(db.String(50), nullable=True)  # Added feedback_type field
    feedback_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship to User model
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

    def __init__(self, user_id, name, email, comment, rating, subject=None, feedback_type=None, image_url=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.subject = subject
        self.comment = comment
        self.rating = rating
        self.feedback_type = feedback_type
        self.image_url = image_url

    def __repr__(self):
        return f"<Feedback {self.feedback_id}>"