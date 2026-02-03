"""Main Routes - Dashboard"""

from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required
from app.models import Order, Distributor, Product, Inventory, Payment
from app import db
from sqlalchemy import func

from pathlib import Path
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)


@bp.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return {'status': 'healthy', 'service': 'Mohi Industries ERP'}, 200


@bp.route('/favicon.ico')
def favicon():
    static_dir = Path(__file__).resolve().parents[1] / 'static'
    return send_from_directory(static_dir, 'logo.png', mimetype='image/png')

@bp.route('/')
@login_required
def dashboard():
    # Dashboard stats
    total_distributors = Distributor.query.filter_by(status='active').count()
    total_products = Product.query.filter_by(is_active=True).count()
    pending_orders = Order.query.filter_by(status='confirmed').count()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    # Analytics snapshot (lightweight KPIs)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sales_last_30d = db.session.query(func.sum(Order.total_amount)).filter(
        Order.order_date >= thirty_days_ago,
        Order.status.in_(['confirmed', 'delivered', 'completed']),
    ).scalar() or 0

    total_receivable = db.session.query(
        func.sum(Order.total_amount - Order.paid_amount)
    ).filter(
        Order.payment_status.in_(['pending', 'partial'])
    ).scalar() or 0

    total_collected = db.session.query(
        func.sum(Payment.amount)
    ).filter(
        Payment.status == 'cleared'
    ).scalar() or 0

    avg_satisfaction = db.session.query(
        func.avg(Distributor.customer_satisfaction_score)
    ).filter(
        Distributor.status == 'active'
    ).scalar() or 0
    
    return render_template('dashboard.html',
                         total_distributors=total_distributors,
                         total_products=total_products,
                         pending_orders=pending_orders,
                         recent_orders=recent_orders,
                         sales_last_30d=sales_last_30d,
                         total_receivable=total_receivable,
                         total_collected=total_collected,
                         avg_satisfaction=avg_satisfaction)
