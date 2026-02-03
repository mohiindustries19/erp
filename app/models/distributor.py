"""
Distributor Model - For Mohi Industries Distribution Network
"""
from app import db
from datetime import datetime

class Distributor(db.Model):
    __tablename__ = 'distributors'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False, index=True)  # DIST001, DIST002
    
    # Basic Info
    business_name = db.Column(db.String(256), nullable=False)
    contact_person = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120))
    
    # Indian Compliance
    gstin = db.Column(db.String(15), unique=True)
    pan = db.Column(db.String(10))
    fssai_license = db.Column(db.String(14))
    
    # Address
    address_line1 = db.Column(db.String(256))
    address_line2 = db.Column(db.String(256))
    city = db.Column(db.String(128))
    state = db.Column(db.String(64))
    state_code = db.Column(db.String(2))
    pincode = db.Column(db.String(6))
    territory = db.Column(db.String(128))  # Sales territory
    
    # Business Terms
    margin_percentage = db.Column(db.Float, default=12.0)  # 12-18%
    credit_limit = db.Column(db.Float, default=0.0)
    credit_days = db.Column(db.Integer, default=0)  # 0 = advance payment
    payment_terms = db.Column(db.String(64), default='advance')  # advance, credit, cod
    
    # Status
    status = db.Column(db.String(32), default='pending')  # pending, active, inactive
    onboarding_date = db.Column(db.Date)
    
    # Bank Details
    bank_name = db.Column(db.String(128))
    bank_account = db.Column(db.String(32))
    bank_ifsc = db.Column(db.String(11))
    
    # Analytics Fields (New)
    loyalty_points = db.Column(db.Integer, default=0)
    customer_satisfaction_score = db.Column(db.Integer, default=5)  # 1-10 scale
    average_order_value = db.Column(db.Float, default=0.0)
    total_lifetime_value = db.Column(db.Float, default=0.0)
    last_order_date = db.Column(db.Date)
    order_frequency = db.Column(db.String(32), default='monthly')  # weekly, monthly, quarterly
    
    # Relationships
    orders = db.relationship('Order', backref='distributor', lazy='dynamic')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def total_orders(self):
        """Get total number of orders"""
        return self.orders.count()
    
    @property
    def total_revenue(self):
        """Calculate total revenue from this distributor"""
        from app.models import Order
        total = db.session.query(db.func.sum(Order.total_amount))\
            .filter(Order.distributor_id == self.id)\
            .filter(Order.status.in_(['confirmed', 'delivered', 'completed']))\
            .scalar()
        return float(total) if total else 0.0
    
    @property
    def outstanding_amount(self):
        """Calculate outstanding payment amount"""
        from app.models import Order
        total = db.session.query(db.func.sum(Order.total_amount - Order.paid_amount))\
            .filter(Order.distributor_id == self.id)\
            .filter(Order.payment_status.in_(['pending', 'partial']))\
            .scalar()
        return float(total) if total else 0.0
    
    def __repr__(self):
        return f'<Distributor {self.code} - {self.business_name}>'
