"""
WhatsApp Integration Routes
Admin panel for sending WhatsApp messages
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Distributor, Order, Product
from app.services.whatsapp import WhatsAppService
from datetime import datetime, date, timedelta

bp = Blueprint('whatsapp', __name__, url_prefix='/whatsapp')


@bp.route('/')
@login_required
def dashboard():
    """WhatsApp dashboard"""
    service = WhatsAppService()
    missing_keys = service.missing_env_keys()
    configured = service.is_configured()
    
    # Get statistics
    total_distributors = Distributor.query.filter_by(status='active').count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Get distributors with pending payments
    pending_payments = Order.query.filter(
        Order.payment_status.in_(['pending', 'partial'])
    ).count()
    
    return render_template('whatsapp/dashboard.html',
                         enabled=service.enabled,
                         provider=service.provider,
                         configured=configured,
                         missing_keys=missing_keys,
                         total_distributors=total_distributors,
                         recent_orders=recent_orders,
                         pending_payments=pending_payments)


@bp.route('/send-product-availability', methods=['GET', 'POST'])
@login_required
def send_product_availability():
    """Send daily product availability to distributors"""
    if request.method == 'POST':
        try:
            service = WhatsAppService()
            
            # Get selected distributors
            distributor_ids = request.form.getlist('distributor_ids')
            if not distributor_ids:
                flash('Please select at least one distributor', 'error')
                return redirect(url_for('whatsapp.send_product_availability'))
            
            distributors = Distributor.query.filter(
                Distributor.id.in_(distributor_ids),
                Distributor.status == 'active'
            ).all()
            
            # Get active products
            products = Product.query.filter_by(is_active=True).limit(10).all()
            
            # Send messages
            success_count = 0
            failed_count = 0
            failures = []
            
            for distributor in distributors:
                success, msg_id = service.send_product_availability(distributor, products)
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    failures.append(f"{distributor.business_name}: {msg_id}")
            
            if failed_count:
                preview = "; ".join(failures[:3])
                more = f" (+{len(failures) - 3} more)" if len(failures) > 3 else ""
                flash(f"Messages sent: {success_count} successful, {failed_count} failed. Failed: {preview}{more}", 'error')
            else:
                flash(f'Messages sent: {success_count} successful, {failed_count} failed', 'success')
            return redirect(url_for('whatsapp.dashboard'))
            
        except Exception as e:
            flash(f'Error sending messages: {str(e)}', 'error')
    
    # GET request
    distributors = Distributor.query.filter_by(status='active').all()
    products = Product.query.filter_by(is_active=True).limit(10).all()
    
    return render_template('whatsapp/send_product_availability.html',
                         distributors=distributors,
                         products=products)


@bp.route('/send-payment-reminders', methods=['GET', 'POST'])
@login_required
def send_payment_reminders():
    """Send payment reminders to distributors with pending payments"""
    if request.method == 'POST':
        try:
            service = WhatsAppService()
            
            # Get distributors with pending payments
            pending_orders = db.session.query(
                Distributor,
                db.func.sum(Order.total_amount - Order.paid_amount).label('outstanding')
            ).join(Order).filter(
                Order.payment_status.in_(['pending', 'partial'])
            ).group_by(Distributor.id).all()
            
            success_count = 0
            failed_count = 0
            failures = []
            
            for distributor, outstanding in pending_orders:
                # Get pending invoices
                invoices = Order.query.filter(
                    Order.distributor_id == distributor.id,
                    Order.payment_status.in_(['pending', 'partial'])
                ).all()
                
                success, msg_id = service.send_payment_reminder(
                    distributor,
                    outstanding,
                    invoices
                )
                
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    failures.append(f"{distributor.business_name}: {msg_id}")
            
            if failed_count:
                preview = "; ".join(failures[:3])
                more = f" (+{len(failures) - 3} more)" if len(failures) > 3 else ""
                flash(f"Payment reminders sent: {success_count} successful, {failed_count} failed. Failed: {preview}{more}", 'error')
            else:
                flash(f'Payment reminders sent: {success_count} successful, {failed_count} failed', 'success')
            return redirect(url_for('whatsapp.dashboard'))
            
        except Exception as e:
            flash(f'Error sending reminders: {str(e)}', 'error')
    
    # GET request - show preview
    pending_orders = db.session.query(
        Distributor,
        db.func.sum(Order.total_amount - Order.paid_amount).label('outstanding'),
        db.func.count(Order.id).label('invoice_count')
    ).join(Order).filter(
        Order.payment_status.in_(['pending', 'partial'])
    ).group_by(Distributor.id).all()
    
    return render_template('whatsapp/send_payment_reminders.html',
                         pending_orders=pending_orders)


@bp.route('/send-bulk-message', methods=['GET', 'POST'])
@login_required
def send_bulk_message():
    """Send custom bulk message to selected distributors"""
    if request.method == 'POST':
        try:
            service = WhatsAppService()
            
            # Get form data
            distributor_ids = request.form.getlist('distributor_ids')
            message = request.form.get('message')
            
            if not distributor_ids:
                flash('Please select at least one distributor', 'error')
                return redirect(url_for('whatsapp.send_bulk_message'))
            
            if not message:
                flash('Please enter a message', 'error')
                return redirect(url_for('whatsapp.send_bulk_message'))
            
            # Get distributors
            distributors = Distributor.query.filter(
                Distributor.id.in_(distributor_ids),
                Distributor.status == 'active'
            ).all()
            
            # Send messages
            results = service.send_bulk_message(distributors, message)

            success_count = sum(1 for r in results if r['success'])
            failures = [f"{r['distributor']}: {r.get('message_id')}" for r in results if not r['success']]
            failed_count = len(failures)

            if failed_count:
                preview = "; ".join(failures[:3])
                more = f" (+{len(failures) - 3} more)" if len(failures) > 3 else ""
                flash(f"Messages sent: {success_count} successful, {failed_count} failed. Failed: {preview}{more}", 'error')
            else:
                flash(f'Messages sent: {success_count} successful, {failed_count} failed', 'success')
            return redirect(url_for('whatsapp.dashboard'))
            
        except Exception as e:
            flash(f'Error sending messages: {str(e)}', 'error')
    
    # GET request
    distributors = Distributor.query.filter_by(status='active').all()
    
    # Group by location for easy selection
    locations = {}
    for dist in distributors:
        if dist.city not in locations:
            locations[dist.city] = []
        locations[dist.city].append(dist)
    
    return render_template('whatsapp/send_bulk_message.html',
                         distributors=distributors,
                         locations=locations)


@bp.route('/send-festival-offer', methods=['GET', 'POST'])
@login_required
def send_festival_offer():
    """Send festival offer to distributors"""
    if request.method == 'POST':
        try:
            service = WhatsAppService()
            
            # Get form data
            distributor_ids = request.form.getlist('distributor_ids')
            offer_details = {
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'valid_from': request.form.get('valid_from'),
                'valid_to': request.form.get('valid_to'),
                'terms': request.form.get('terms')
            }
            
            if not distributor_ids:
                flash('Please select at least one distributor', 'error')
                return redirect(url_for('whatsapp.send_festival_offer'))
            
            # Get distributors
            distributors = Distributor.query.filter(
                Distributor.id.in_(distributor_ids),
                Distributor.status == 'active'
            ).all()
            
            # Send messages
            success_count = 0
            failed_count = 0
            failures = []
            
            for distributor in distributors:
                success, msg_id = service.send_festival_offer(distributor, offer_details)
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    failures.append(f"{distributor.business_name}: {msg_id}")
            
            if failed_count:
                preview = "; ".join(failures[:3])
                more = f" (+{len(failures) - 3} more)" if len(failures) > 3 else ""
                flash(f"Offers sent: {success_count} successful, {failed_count} failed. Failed: {preview}{more}", 'error')
            else:
                flash(f'Offers sent: {success_count} successful, {failed_count} failed', 'success')
            return redirect(url_for('whatsapp.dashboard'))
            
        except Exception as e:
            flash(f'Error sending offers: {str(e)}', 'error')
    
    # GET request
    distributors = Distributor.query.filter_by(status='active').all()
    today = date.today().strftime('%Y-%m-%d')
    
    return render_template('whatsapp/send_festival_offer.html',
                         distributors=distributors,
                         today=today)


@bp.route('/test-message', methods=['POST'])
@login_required
def test_message():
    """Send test message to verify WhatsApp configuration"""
    try:
        service = WhatsAppService()

        if not service.enabled:
            return jsonify({'success': False, 'error': 'WhatsApp is disabled. Enable WHATSAPP_ENABLED=true in environment variables.'})

        missing = service.missing_env_keys()
        if missing:
            return jsonify({'success': False, 'error': f"Missing required config: {', '.join(missing)}"})
        
        phone = request.form.get('phone')
        if not phone:
            return jsonify({'success': False, 'error': 'Phone number required'})
        
        message = """🧪 Test Message

This is a test message from Mohi Industries ERP.

If you received this, WhatsApp integration is working! ✅

📞 9262650010
Mohi Industries"""
        
        success, msg_id = service.send_message(phone, message)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Test message sent successfully!',
                'message_id': msg_id
            })
        else:
            return jsonify({
                'success': False,
                'error': msg_id
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """WhatsApp settings page"""
    if request.method == 'POST':
        # Update settings (would need to update config file or database)
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('whatsapp.settings'))
    
    service = WhatsAppService()

    return render_template('whatsapp/settings.html',
                         enabled=service.enabled,
                         provider=service.provider,
                         configured=service.is_configured(),
                         missing_keys=service.missing_env_keys(),
                         required_keys=service.required_env_keys())


# API endpoint for webhook (to receive messages from WhatsApp)
@bp.route('/webhook', methods=['POST'])
def webhook():
    """Webhook to receive incoming WhatsApp messages"""
    try:
        data = request.get_json()
        
        # Log incoming message
        print(f"Received WhatsApp message: {data}")
        
        # TODO: Process incoming message
        # - Parse order from message
        # - Create order in ERP
        # - Send confirmation
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
