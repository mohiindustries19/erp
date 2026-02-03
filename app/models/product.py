"""
Product Models - FMCG Products with Indian Compliance
"""
from app import db
from datetime import datetime

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)  # Bakery, Pickles, Water
    code = db.Column(db.String(16), unique=True, nullable=False)  # BAK, PCK, WAT
    hsn_code = db.Column(db.String(8))  # HSN Code for GST
    gst_rate = db.Column(db.Float, default=5.0)  # GST percentage
    description = db.Column(db.Text)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(32), unique=True, nullable=False, index=True)
    name = db.Column(db.String(256), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    
    # Product Details
    description = db.Column(db.Text)
    unit = db.Column(db.String(16), default='pcs')  # pcs, kg, ltr, box
    pack_size = db.Column(db.String(64))  # 500ml, 1kg, 200g
    
    # Indian Compliance - FSSAI
    hsn_code = db.Column(db.String(8))
    gst_rate = db.Column(db.Float)
    shelf_life_days = db.Column(db.Integer)  # 3-5 for bakery, 365 for pickles, 180 for water
    requires_batch_tracking = db.Column(db.Boolean, default=True)
    
    # Pricing
    mrp = db.Column(db.Float, nullable=False)
    base_price = db.Column(db.Float, nullable=False)  # Price to distributor
    cost_price = db.Column(db.Float)  # Manufacturing cost
    
    # Barcode - EAN-13 for Retail
    ean_barcode = db.Column(db.String(13), unique=True, index=True)  # 13-digit EAN barcode
    barcode_source = db.Column(db.String(32), default='internal')  # gs1, reseller, internal
    barcode_registered_date = db.Column(db.Date)
    
    # Inventory
    min_stock_level = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    inventory = db.relationship('Inventory', backref='product', lazy='dynamic')
    batches = db.relationship('Batch', backref='product', lazy='dynamic')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.sku} - {self.name}>'
