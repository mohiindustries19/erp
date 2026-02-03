"""
Purchasing Models - Vendors, Purchase Orders, Vendor Bills
"""
from app import db
from datetime import datetime


class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False, index=True)
    business_name = db.Column(db.String(256), nullable=False)
    contact_person = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(128))
    gstin = db.Column(db.String(15))
    address = db.Column(db.Text)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    payment_terms = db.Column(db.String(64))  # advance, credit, cod
    status = db.Column(db.String(32), default='active')  # active, inactive
    ap_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ap_account = db.relationship('Account')

    def __repr__(self):
        return f'<Vendor {self.code} - {self.business_name}>'


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(32), unique=True, nullable=False, index=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)

    order_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    expected_date = db.Column(db.Date)
    status = db.Column(db.String(32), default='draft')  # draft, ordered, received, cancelled

    subtotal = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)

    remarks = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vendor = db.relationship('Vendor', backref='purchase_orders')
    items = db.relationship('PurchaseOrderItem', backref='purchase_order', lazy='dynamic', cascade='all, delete-orphan')

    def calculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items)
        self.tax_amount = sum((item.line_total * (item.gst_rate or 0)) / 100 for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount

    def __repr__(self):
        return f'<PO {self.order_number}>'


class PurchaseOrderItem(db.Model):
    __tablename__ = 'purchase_order_items'

    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    gst_rate = db.Column(db.Float, default=0.0)
    line_total = db.Column(db.Float, default=0.0)

    product = db.relationship('Product')

    def calculate_line_total(self):
        self.line_total = self.quantity * self.unit_cost

    def __repr__(self):
        return f'<POItem PO:{self.purchase_order_id} P:{self.product_id}>'


class VendorBill(db.Model):
    __tablename__ = 'vendor_bills'

    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(32), unique=True, nullable=False, index=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'))

    bill_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(32), default='pending')  # pending, partial, paid
    approval_status = db.Column(db.String(32), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)

    subtotal = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)

    remarks = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vendor = db.relationship('Vendor', backref='vendor_bills')
    purchase_order = db.relationship('PurchaseOrder', backref='vendor_bills')
    items = db.relationship('VendorBillItem', backref='vendor_bill', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('VendorPayment', backref='vendor_bill', lazy='dynamic', cascade='all, delete-orphan')

    def calculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items)
        self.tax_amount = sum((item.line_total * (item.gst_rate or 0)) / 100 for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount

    def __repr__(self):
        return f'<VendorBill {self.bill_number}>'


class VendorBillItem(db.Model):
    __tablename__ = 'vendor_bill_items'

    id = db.Column(db.Integer, primary_key=True)
    vendor_bill_id = db.Column(db.Integer, db.ForeignKey('vendor_bills.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    gst_rate = db.Column(db.Float, default=0.0)
    line_total = db.Column(db.Float, default=0.0)

    product = db.relationship('Product')

    def calculate_line_total(self):
        self.line_total = self.quantity * self.unit_cost

    def __repr__(self):
        return f'<VendorBillItem B:{self.vendor_bill_id} P:{self.product_id}>'


class VendorPayment(db.Model):
    __tablename__ = 'vendor_payments'

    id = db.Column(db.Integer, primary_key=True)
    vendor_bill_id = db.Column(db.Integer, db.ForeignKey('vendor_bills.id'), nullable=False)

    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(32), nullable=False)  # cash, bank_transfer, upi, cheque
    reference_number = db.Column(db.String(64))
    bank_name = db.Column(db.String(128))
    status = db.Column(db.String(32), default='cleared')  # pending, cleared, bounced

    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<VendorPayment B:{self.vendor_bill_id} ₹{self.amount}>'
