"""
Company Model - Indian Compliance
"""
from app import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    
    # Indian Compliance Fields
    gstin = db.Column(db.String(15), unique=True, nullable=False)  # GST Number
    pan = db.Column(db.String(10), nullable=False)
    tan = db.Column(db.String(10))  # TAN for TDS
    fssai_license = db.Column(db.String(14), nullable=False)  # FSSAI License
    
    # Address
    address_line1 = db.Column(db.String(256))
    address_line2 = db.Column(db.String(256))
    city = db.Column(db.String(128))
    state = db.Column(db.String(64))
    state_code = db.Column(db.String(2))  # GST State Code
    pincode = db.Column(db.String(6))
    
    # Contact
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    website = db.Column(db.String(256))
    
    # Bank Details
    bank_name = db.Column(db.String(128))
    bank_account = db.Column(db.String(32))
    bank_ifsc = db.Column(db.String(11))
    bank_branch = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Company {self.name}>'
