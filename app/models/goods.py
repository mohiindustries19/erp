"""
Goods Inventory Model
"""
from app import db
from datetime import datetime

class Goods(db.Model):
    __tablename__ = 'goods'
    
    id = db.Column(db.Integer, primary_key=True)
    item_number = db.Column(db.Integer, unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))  # Equipment, Packaging, Furniture, etc.
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(50), default='pcs')
    location = db.Column(db.String(200))
    condition = db.Column(db.String(50), default='good')  # good, fair, poor, damaged
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Float)
    supplier = db.Column(db.String(200))
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Goods {self.item_number}: {self.name}>'
