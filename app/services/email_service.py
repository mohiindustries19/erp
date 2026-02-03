"""Email Service - Automated Email Notifications."""

from flask import current_app, render_template
from flask_mail import Message
from app.models import Order, Distributor, Product, Inventory, Payment
from app import db
from app import mail
from datetime import datetime, timedelta
from sqlalchemy import func
import os

class EmailService:
    
    @staticmethod
    def send_email(to, subject, template, **kwargs):
        """Send email using template"""
        try:
            msg = Message(
                subject=subject,
                recipients=[to] if isinstance(to, str) else to,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            msg.html = render_template(f'emails/{template}.html', **kwargs)
            
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    @staticmethod
    def send_html_email(to, subject, html, attachments=None):
        """Send an HTML email; optionally attach files.

        attachments: list of dicts with keys: filename, content_type, data(bytes)
        """
        try:
            msg = Message(
                subject=subject,
                recipients=[to] if isinstance(to, str) else to,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
            )
            msg.html = html

            for att in attachments or []:
                msg.attach(
                    att['filename'],
                    att.get('content_type', 'application/octet-stream'),
                    att['data'],
                )

            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    @staticmethod
    def send_order_confirmation(order_id):
        """Send order confirmation email to distributor"""
        if not current_app.config.get('SEND_ORDER_CONFIRMATIONS'):
            return False
        
        order = Order.query.get(order_id)
        if not order or not order.distributor.email:
            return False
        
        return EmailService.send_email(
            to=order.distributor.email,
            subject=f'Order Confirmation - {order.order_number}',
            template='order_confirmation',
            order=order,
            company_name=current_app.config['COMPANY_NAME'],
            company_phone=current_app.config['COMPANY_PHONE'],
            company_email=current_app.config['COMPANY_EMAIL']
        )
    
    @staticmethod
    def send_payment_receipt(payment_id):
        """Send payment receipt email"""
        payment = Payment.query.get(payment_id)
        if not payment or not payment.order.distributor.email:
            return False
        
        return EmailService.send_email(
            to=payment.order.distributor.email,
            subject=f'Payment Receipt - {payment.payment_number}',
            template='payment_receipt',
            payment=payment,
            order=payment.order,
            company_name=current_app.config['COMPANY_NAME'],
            company_phone=current_app.config['COMPANY_PHONE'],
            company_email=current_app.config['COMPANY_EMAIL']
        )
    
    @staticmethod
    def send_payment_reminder(order_id):
        """Send payment reminder for overdue orders"""
        if not current_app.config.get('SEND_PAYMENT_REMINDERS'):
            return False
        
        order = Order.query.get(order_id)
        if not order or not order.distributor.email:
            return False
        
        if order.payment_status == 'paid':
            return False
        
        outstanding = order.total_amount - order.paid_amount
        days_overdue = (datetime.now().date() - order.order_date).days
        
        return EmailService.send_email(
            to=order.distributor.email,
            subject=f'Payment Reminder - {order.order_number}',
            template='payment_reminder',
            order=order,
            outstanding=outstanding,
            days_overdue=days_overdue,
            company_name=current_app.config['COMPANY_NAME'],
            company_phone=current_app.config['COMPANY_PHONE'],
            company_email=current_app.config['COMPANY_EMAIL']
        )
    
    @staticmethod
    def send_low_stock_alert(product_id):
        """Send low stock alert to admin"""
        if not current_app.config.get('SEND_LOW_STOCK_ALERTS'):
            return False
        
        product = Product.query.get(product_id)
        inventory = Inventory.query.filter_by(product_id=product_id).first()
        
        if not product or not inventory:
            return False
        
        admin_email = current_app.config['COMPANY_EMAIL']
        
        return EmailService.send_email(
            to=admin_email,
            subject=f'Low Stock Alert - {product.name}',
            template='low_stock_alert',
            product=product,
            inventory=inventory,
            company_name=current_app.config['COMPANY_NAME']
        )
    
    @staticmethod
    def send_monthly_statement(distributor_id, month, year):
        """Send monthly statement to distributor"""
        distributor = Distributor.query.get(distributor_id)
        if not distributor or not distributor.email:
            return False
        
        # Get orders for the month
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()
        
        orders = Order.query.filter(
            Order.distributor_id == distributor_id,
            Order.order_date >= start_date,
            Order.order_date < end_date
        ).all()
        
        if not orders:
            return False
        
        # Calculate totals
        total_orders = len(orders)
        total_amount = sum(o.total_amount for o in orders)
        total_paid = sum(o.paid_amount for o in orders)
        total_outstanding = total_amount - total_paid
        
        month_name = start_date.strftime('%B %Y')
        
        return EmailService.send_email(
            to=distributor.email,
            subject=f'Monthly Statement - {month_name}',
            template='monthly_statement',
            distributor=distributor,
            orders=orders,
            month_name=month_name,
            total_orders=total_orders,
            total_amount=total_amount,
            total_paid=total_paid,
            total_outstanding=total_outstanding,
            company_name=current_app.config['COMPANY_NAME'],
            company_phone=current_app.config['COMPANY_PHONE'],
            company_email=current_app.config['COMPANY_EMAIL']
        )
    
    @staticmethod
    def send_bulk_payment_reminders():
        """Send payment reminders to all overdue orders"""
        reminder_days = current_app.config.get('PAYMENT_REMINDER_DAYS', 7)
        cutoff_date = datetime.now().date() - timedelta(days=reminder_days)
        
        overdue_orders = Order.query.filter(
            Order.payment_status.in_(['pending', 'partial']),
            Order.order_date <= cutoff_date
        ).all()
        
        sent_count = 0
        for order in overdue_orders:
            if EmailService.send_payment_reminder(order.id):
                sent_count += 1
        
        return sent_count
    
    @staticmethod
    def send_bulk_low_stock_alerts():
        """Send low stock alerts for all products below reorder level"""
        low_stock_items = db.session.query(
            Product, Inventory
        ).join(Inventory).filter(
            Inventory.current_stock < Inventory.reorder_level,
            Product.is_active == True
        ).all()
        
        sent_count = 0
        for product, inventory in low_stock_items:
            if EmailService.send_low_stock_alert(product.id):
                sent_count += 1
        
        return sent_count
    
    @staticmethod
    def test_email_configuration():
        """Test email configuration by sending a test email"""
        admin_email = current_app.config['COMPANY_EMAIL']
        
        try:
            msg = Message(
                subject='Test Email - Mohi ERP',
                recipients=[admin_email],
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            msg.html = """
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #2563eb;">Email Configuration Test</h2>
                    <p>This is a test email from Mohi Industries ERP.</p>
                    <p>If you received this email, your email configuration is working correctly!</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        Sent from Mohi Industries ERP<br>
                        {datetime}
                    </p>
                </body>
            </html>
            """.format(datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            mail.send(msg)
            return True, "Test email sent successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"
