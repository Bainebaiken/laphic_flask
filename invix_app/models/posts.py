from datetime import datetime
from invix_app.extensions import db


class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment = db.Column(db.String(100), nullable=False)
    blog = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    # content = db.relationship('Content', backref='posts')
    user = db.relationship('User', backref='posts')

    def __init__(self, title, description, user_id, comment, blog):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.comment = comment
        self.blog = blog

    def __repr__(self):
        return f'<Post {self.title}>'









