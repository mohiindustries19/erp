"""
Order Models - Sales Orders with GST Compliance
"""
from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(32), unique=True, nullable=False, index=True)
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributors.id'), nullable=False)
    
    # Order Details
    order_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    delivery_date = db.Column(db.Date)
    order_type = db.Column(db.String(32), default='regular')  # regular, daily_bakery, bulk
    
    # Amounts (Before Tax)
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    taxable_amount = db.Column(db.Float, default=0.0)
    
    # GST Breakdown
    cgst_amount = db.Column(db.Float, default=0.0)
    sgst_amount = db.Column(db.Float, default=0.0)
    igst_amount = db.Column(db.Float, default=0.0)
    
    # Total
    total_amount = db.Column(db.Float, default=0.0)
    
    # Payment
    payment_terms = db.Column(db.String(64))  # advance, credit, cod
    payment_status = db.Column(db.String(32), default='pending')  # pending, partial, paid
    paid_amount = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(32), default='draft')  # draft, confirmed, processing, dispatched, delivered, cancelled
    
    # Delivery
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    delivery_address = db.Column(db.Text)
    
    # Notes
    remarks = db.Column(db.Text)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_totals(self):
        """Calculate order totals with GST"""
        self.subtotal = sum(item.line_total for item in self.items)
        self.taxable_amount = self.subtotal - self.discount_amount
        
        # Check if inter-state or intra-state
        # For now, assuming intra-state (CGST + SGST)
        self.cgst_amount = 0
        self.sgst_amount = 0
        self.igst_amount = 0
        
        for item in self.items:
            gst_rate = item.gst_rate
            item_taxable = item.line_total
            
            # Intra-state: CGST + SGST
            self.cgst_amount += item_taxable * (gst_rate / 2) / 100
            self.sgst_amount += item_taxable * (gst_rate / 2) / 100
        
        self.total_amount = self.taxable_amount + self.cgst_amount + self.sgst_amount + self.igst_amount
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item Details
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, default=0.0)
    
    # GST
    hsn_code = db.Column(db.String(8))
    gst_rate = db.Column(db.Float)
    
    # Calculated
    line_total = db.Column(db.Float)  # quantity * unit_price * (1 - discount/100)
    
    # Batch Allocation (for FSSAI compliance)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'))
    
    # Relationships
    product = db.relationship('Product')
    batch = db.relationship('Batch')
    
    def calculate_line_total(self):
        """Calculate line total after discount"""
        discount_multiplier = 1 - (self.discount_percent / 100)
        self.line_total = self.quantity * self.unit_price * discount_multiplier
    
    def __repr__(self):
        return f'<OrderItem O:{self.order_id} P:{self.product_id}>'
