"""
Quality Control Models - Batch QC Workflow
"""
from app import db
from datetime import datetime


class QualityCheckTemplate(db.Model):
    __tablename__ = 'qc_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('QualityCheckItem', backref='template', lazy='dynamic', cascade='all, delete-orphan')
    category = db.relationship('ProductCategory')

    def __repr__(self):
        return f'<QCTemplate {self.name}>'


class QualityCheckItem(db.Model):
    __tablename__ = 'qc_items'

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('qc_templates.id'), nullable=False)
    step = db.Column(db.String(256), nullable=False)
    expected = db.Column(db.String(128))
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)

    def __repr__(self):
        return f'<QCItem {self.step}>'


class BatchQualityCheck(db.Model):
    __tablename__ = 'batch_qc_checks'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('qc_templates.id'), nullable=False)

    status = db.Column(db.String(32), default='pending')  # pending, passed, failed
    remarks = db.Column(db.Text)

    checked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    template = db.relationship('QualityCheckTemplate')
    checked_by_user = db.relationship('User', foreign_keys=[checked_by])

    def __repr__(self):
        return f'<BatchQC B:{self.batch_id} {self.status}>'
