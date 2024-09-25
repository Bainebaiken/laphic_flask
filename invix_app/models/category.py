from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from invix_app.extensions import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False)
    # content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=True)
    
    # content = db.relationship('Content', backref='categories')
    articles = db.relationship('Article', back_populates='category')

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug
        # self.content_id = content_id

    def __repr__(self):
        return f'<Category {self.name}>'


# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from invix_app.extensions import db

# class Category(db.Model):
#     __tablename__ = "category"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False, unique=True)
#     slug = db.Column(db.String(100), nullable=False)
#     content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=True)
    
#     content = db.relationship('Content', backref='categories')
#     articles = db.relationship('Article', back_populates='category')

#     def __init__(self, name, slug, content_id=None):
#         self.name = name
#         self.slug = slug
#         self.content_id = content_id

#     def __repr__(self):
#         return f'<Category {self.name}>'



# # from datetime import datetime
# # from flask_sqlalchemy import SQLAlchemy
# # from invix_app.extensions import db

# # from invix_app.extensions import db



# # class Category(db.Model):
# #     __tablename__ = "category"

# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(50), nullable=False, unique=True)
# #     content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=True)
# #     slug = db.Column(db.String(100), nullable=False)

# #     content = db.relationship('Content', backref='categories')
# #     articles = db.relationship('Article', back_populates='category')

# #     def __init__(self, name, slug, content_id=None):
# #         self.name = name
# #         self.slug = slug
# #         self.content_id = content_id

# #     def __repr__(self):
# #         return f'<Sports {self.name}>'


