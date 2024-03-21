from authors_app import db
from datetime import datetime

class Books(db.Model):
    __tablename__ = "books"  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))  
    user = db.relationship('User', backref='books')  # Define the relationship with User model
    company = db.relationship('Company', backref='books')  # Define the relationship with Company model
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Constructor
    def __init__(self, title, description, pages, user_id, company_id, price, image):
        self.title = title
        self.description = description
        self.number_of_pages = pages
        self.user_id = user_id
        self.company_id = company_id
        self.price = price
        self.image = image

    def __repr__(self):
        return f'<Books {self.title}>'















# from authors_app import db
# from datetime import datetime

# class books(db.Model):
#  __table__="books"
#  id =db.Column(db.Integer,primay_key=True)
#  title=db.Column(db.String(50),nullable=False)
#  description=db.Column(db.String(100),nullable=False)
#  image=db.Column(db.String(255),nullable=False)
#  price=db.Column(db.Integer,nullable=False)
#  number_of_pages=db.Column(db.Integer,nullable=False) 
#  user_id =db.Column(db.Integer, db.Foreign_key("users"))
#  company_id=db.Column(db.Integer,db.Foreignkey('companies.id'))
#  #relationships
#  #user=db.relationship('User',backref='books')
#  #company=db.relationship('company',backref='books')
#  created_at=db.Column(db.DateTime,default=datetime.now())
#  updated_at=db.Column(db.DateTime,onupdate=datetime.now())
#  def __init__(self,title,description,pages,user_id,company-id,price,):
#         self.title=title
#         self.description=description
#         self.com
#         self.user_id=user_id
#         self.pages=pages
# def __init__(self):
#         return f'<Book{self.title}'