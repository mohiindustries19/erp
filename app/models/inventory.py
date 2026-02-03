"""
Inventory & Batch Models - FSSAI Compliance with Batch Tracking
"""
from app import db
from datetime import datetime, date

class Batch(db.Model):
    """Batch/Lot tracking for FSSAI compliance"""
    __tablename__ = 'batches'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.String(64), unique=True, nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # FSSAI Mandatory Fields
    manufacturing_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    
    # Production Details
    quantity_produced = db.Column(db.Integer, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    
    # Quality Control
    qc_status = db.Column(db.String(32), default='pending')  # pending, passed, failed
    qc_date = db.Column(db.Date)
    qc_remarks = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_expired(self):
        return date.today() > self.expiry_date
    
    def days_to_expiry(self):
        return (self.expiry_date - date.today()).days
    
    def __repr__(self):
        return f'<Batch {self.batch_number}>'

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(256))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    inventory = db.relationship('Inventory', backref='warehouse', lazy='dynamic')
    batches = db.relationship('Batch', backref='warehouse', lazy='dynamic')
    
    def __repr__(self):
        return f'<Warehouse {self.code} - {self.name}>'

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    
    # Stock Levels
    quantity = db.Column(db.Integer, default=0)
    reserved_quantity = db.Column(db.Integer, default=0)  # For pending orders
    available_quantity = db.Column(db.Integer, default=0)  # quantity - reserved
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one record per product per warehouse
    __table_args__ = (
        db.UniqueConstraint('product_id', 'warehouse_id', name='_product_warehouse_uc'),
    )
    
    def __repr__(self):
        return f'<Inventory P:{self.product_id} W:{self.warehouse_id} Q:{self.quantity}>'
