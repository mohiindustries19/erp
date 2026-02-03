"""
Payment Models - Payment Tracking and Accounting
"""
from app import db
from datetime import datetime

class Payment(db.Model):
    """Payment transactions for orders"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    payment_number = db.Column(db.String(32), unique=True, nullable=False, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    
    # Payment Details
    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(32), nullable=False)  # cash, cheque, bank_transfer, upi, card
    
    # Payment Mode Specific Details
    reference_number = db.Column(db.String(64))  # Cheque no, Transaction ID, UTR
    bank_name = db.Column(db.String(128))
    cheque_date = db.Column(db.Date)  # For cheque payments
    
    # Status
    status = db.Column(db.String(32), default='pending')  # pending, cleared, bounced, cancelled
    clearance_date = db.Column(db.Date)  # When payment cleared
    
    # Notes
    remarks = db.Column(db.Text)
    
    # Accounting
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='payments')
    
    def __repr__(self):
        return f'<Payment {self.payment_number} - ₹{self.amount}>'
