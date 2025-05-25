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

    # New fields for cost and square meter ranges
    Min_Cost = db.Column(db.Float, nullable=True)
    Max_Cost = db.Column(db.Float, nullable=True)
    Min_Square_Meters = db.Column(db.Float, nullable=True)
    Max_Square_Meters = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Gallery Image {self.Image_ID}: {self.Image_Name}>"

    def to_dict(self):
        return {
            "Image_ID": self.Image_ID,
            "Service_ID": self.Service_ID,
            "Image_Name": self.Image_Name,
            "Image_Description": self.Image_Description,
            "Image_Path": self.Image_Path,
            "Upload_Date": self.Upload_Date.isoformat(),
            "Min_Cost": self.Min_Cost,
            "Max_Cost": self.Max_Cost,
            "Min_Square_Meters": self.Min_Square_Meters,
            "Max_Square_Meters": self.Max_Square_Meters
        }
