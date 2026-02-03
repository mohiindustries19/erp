"""
Email Notifications Routes - Manage automated emails
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services.email_service import EmailService
from app.models import Order, Distributor
from app import db
from datetime import datetime

bp = Blueprint('email_notifications', __name__, url_prefix='/emails')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Email notifications dashboard"""
    return render_template('emails/dashboard.html')


@bp.route('/test', methods=['POST'])
@login_required
def test_email():
    """Test email configuration"""
    success, message = EmailService.test_email_configuration()
    
    return jsonify({
        'success': success,
        'message': message
    })


@bp.route('/send/order-confirmation/<int:order_id>', methods=['POST'])
@login_required
def send_order_confirmation(order_id):
    """Send order confirmation email"""
    success = EmailService.send_order_confirmation(order_id)
    
    if success:
        flash('Order confirmation email sent successfully!', 'success')
    else:
        flash('Failed to send order confirmation email.', 'error')
    
    return redirect(request.referrer or url_for('orders.view_order', id=order_id))


@bp.route('/send/payment-receipt/<int:payment_id>', methods=['POST'])
@login_required
def send_payment_receipt(payment_id):
    """Send payment receipt email"""
    success = EmailService.send_payment_receipt(payment_id)
    
    if success:
        flash('Payment receipt sent successfully!', 'success')
    else:
        flash('Failed to send payment receipt.', 'error')
    
    return redirect(request.referrer or url_for('payment.list_payments'))


@bp.route('/send/payment-reminder/<int:order_id>', methods=['POST'])
@login_required
def send_payment_reminder(order_id):
    """Send payment reminder email"""
    success = EmailService.send_payment_reminder(order_id)
    
    if success:
        flash('Payment reminder sent successfully!', 'success')
    else:
        flash('Failed to send payment reminder.', 'error')
    
    return redirect(request.referrer or url_for('orders.view_order', id=order_id))


@bp.route('/send/bulk-payment-reminders', methods=['POST'])
@login_required
def send_bulk_payment_reminders():
    """Send payment reminders to all overdue orders"""
    count = EmailService.send_bulk_payment_reminders()
    
    return jsonify({
        'success': True,
        'message': f'Sent {count} payment reminders successfully',
        'count': count
    })


@bp.route('/send/bulk-low-stock-alerts', methods=['POST'])
@login_required
def send_bulk_low_stock_alerts():
    """Send low stock alerts for all products below reorder level"""
    count = EmailService.send_bulk_low_stock_alerts()
    
    return jsonify({
        'success': True,
        'message': f'Sent {count} low stock alerts successfully',
        'count': count
    })


@bp.route('/send/monthly-statement/<int:distributor_id>', methods=['POST'])
@login_required
def send_monthly_statement(distributor_id):
    """Send monthly statement to distributor"""
    data = request.get_json()
    month = data.get('month', datetime.now().month)
    year = data.get('year', datetime.now().year)
    
    success = EmailService.send_monthly_statement(distributor_id, month, year)
    
    return jsonify({
        'success': success,
        'message': 'Monthly statement sent successfully' if success else 'Failed to send monthly statement'
    })


@bp.route('/api/stats')
@login_required
def email_stats():
    """Get email statistics"""
    from datetime import timedelta
    
    # Get overdue orders count
    reminder_days = 7
    cutoff_date = datetime.now().date() - timedelta(days=reminder_days)
    overdue_count = Order.query.filter(
        Order.payment_status.in_(['pending', 'partial']),
        Order.order_date <= cutoff_date
    ).count()
    
    # Get low stock products count
    from app.models import Product, Inventory
    low_stock_count = db.session.query(Product).join(Inventory).filter(
        Inventory.quantity < Product.reorder_level,
        Product.is_active == True
    ).count()
    
    # Get pending orders count
    pending_orders = Order.query.filter_by(status='confirmed').count()
    
    # Get active distributors with email
    active_distributors = Distributor.query.filter(
        Distributor.status == 'active',
        Distributor.email.isnot(None),
        Distributor.email != ''
    ).count()
    
    return jsonify({
        'overdue_orders': overdue_count,
        'low_stock_products': low_stock_count,
        'pending_orders': pending_orders,
        'active_distributors': active_distributors
    })
