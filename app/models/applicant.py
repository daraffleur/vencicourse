from datetime import datetime
from app import db
from app.models.utils import ModelMixin


class Applicant(db.Model, ModelMixin):

    __tablename__ = "applicants"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} {self.middle_name}: {self.phone} ({self.email})>"
