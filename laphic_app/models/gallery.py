from datetime import datetime
from laphic_app.extensions import db

class Gallery(db.Model):
    __tablename__ = 'gallery'

    Image_ID = db.Column(db.Integer, primary_key=True)
    Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=True)
    Image_Name = db.Column(db.String(150), nullable=False)
    Image_Description = db.Column(db.Text, nullable=True)
    Image_Path = db.Column(db.String(255), nullable=False)
    Upload_Date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Gallery Image {self.Image_ID}: {self.Image_Name}>"




# from datetime import datetime
# from laphic_app.extensions import db

# class Gallery(db.Model):
#     __tablename__ = 'gallery'
#     Image_ID = db.Column(db.Integer, primary_key=True)  # Primary Key
#     Service_ID = db.Column(db.Integer, db.ForeignKey('services.Service_ID'), nullable=True)  # Optional: Link to a service
#     Image_Name = db.Column(db.String(150), nullable=False)  # Name of the image
#     Image_Description = db.Column(db.Text, nullable=True)  # Description of the image
#     Image_Path = db.Column(db.String(255), nullable=False)  # File path to the image
#     Upload_Date = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for upload

#     # Relationship to associate this gallery image with a service
#     service = db.relationship('Service', backref='gallery_images', lazy=True)

#     def __init__(self, Image_Name, Image_Path, Service_ID=None, Image_Description=None):
#         self.Image_Name = Image_Name
#         self.Image_Path = Image_Path
#         self.Service_ID = Service_ID
#         self.Image_Description = Image_Description

#     def __repr__(self):
#         return f"<Gallery Image {self.Image_ID}: {self.Image_Name}>"
