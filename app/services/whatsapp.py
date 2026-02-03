"""
WhatsApp Business Integration Service
Supports multiple providers: Twilio, Gupshup, Interakt
"""
import requests
import logging
from flask import current_app, url_for
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class WhatsAppService:
    """WhatsApp Business API Service"""
    
    def __init__(self):
        self.provider = current_app.config.get('WHATSAPP_PROVIDER', 'twilio')
        self.enabled = current_app.config.get('WHATSAPP_ENABLED', False)
        
        # Provider-specific configuration
        if self.provider == 'twilio':
            self.account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
            self.auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
            self.from_number = current_app.config.get('TWILIO_WHATSAPP_NUMBER')
        elif self.provider == 'gupshup':
            self.api_key = current_app.config.get('GUPSHUP_API_KEY')
            self.app_name = current_app.config.get('GUPSHUP_APP_NAME')
        elif self.provider == 'interakt':
            self.api_key = current_app.config.get('INTERAKT_API_KEY')
            self.base_url = current_app.config.get('INTERAKT_BASE_URL', 'https://api.interakt.ai/v1')
    
    def _format_phone(self, phone):
        """Format phone number for WhatsApp (remove spaces, add country code)"""
        # Remove spaces, dashes, parentheses
        phone = ''.join(filter(str.isdigit, str(phone or '')))

        if not phone:
            return phone

        # Common India formats:
        # - 10 digits: XXXXXXXXXX  -> add 91
        # - 0XXXXXXXXXX (11 digits) -> strip 0, add 91
        # - 91XXXXXXXXXX (12 digits) -> already includes country code
        if len(phone) == 11 and phone.startswith('0'):
            phone = phone[1:]

        if len(phone) == 10:
            phone = '91' + phone

        return phone
    
    def _send_twilio(self, to, message, media_url=None):
        """Send message via Twilio"""
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            
            params = {
                'from_': f'whatsapp:{self.from_number}',
                'to': f'whatsapp:+{to}',
                'body': message
            }
            
            if media_url:
                params['media_url'] = [media_url]
            
            message = client.messages.create(**params)
            
            logger.info(f"WhatsApp sent via Twilio: {message.sid}")
            return True, message.sid
            
        except Exception as e:
            logger.error(f"Twilio error: {str(e)}")
            return False, str(e)
    
    def _send_gupshup(self, to, message, media_url=None):
        """Send message via Gupshup"""
        try:
            url = "https://api.gupshup.io/sm/api/v1/msg"
            
            headers = {
                'apikey': self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'channel': 'whatsapp',
                'source': self.app_name,
                'destination': to,
                'message': json.dumps({'type': 'text', 'text': message}),
                'src.name': self.app_name
            }
            
            response = requests.post(url, headers=headers, data=data)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"WhatsApp sent via Gupshup: {result}")
                return True, result.get('messageId')
            else:
                logger.error(f"Gupshup error: {response.text}")
                return False, response.text
                
        except Exception as e:
            logger.error(f"Gupshup error: {str(e)}")
            return False, str(e)
    
    def _send_interakt(self, to, message, media_url=None):
        """Send message via Interakt"""
        try:
            url = f"{self.base_url}/public/message/"
            
            headers = {
                'Authorization': f'Basic {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'countryCode': '+91',
                'phoneNumber': to[-10:],  # Last 10 digits
                'type': 'Text',
                'data': {
                    'message': message
                }
            }
            
            if media_url:
                data['type'] = 'Document'
                data['data'] = {
                    'url': media_url,
                    'filename': 'document.pdf'
                }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"WhatsApp sent via Interakt: {result}")
                return True, result.get('result', {}).get('messageId')
            else:
                logger.error(f"Interakt error: {response.text}")
                return False, response.text
                
        except Exception as e:
            logger.error(f"Interakt error: {str(e)}")
            return False, str(e)
    
    def send_message(self, phone, message, media_url=None):
        """Send WhatsApp message (auto-selects provider)"""
        if not self.enabled:
            logger.warning("WhatsApp is disabled in config")
            return False, "WhatsApp disabled"
        
        # Format phone number
        phone = self._format_phone(phone)
        
        # Send via configured provider
        if self.provider == 'twilio':
            return self._send_twilio(phone, message, media_url)
        elif self.provider == 'gupshup':
            return self._send_gupshup(phone, message, media_url)
        elif self.provider == 'interakt':
            return self._send_interakt(phone, message, media_url)
        else:
            logger.error(f"Unknown provider: {self.provider}")
            return False, "Unknown provider"
    
    def send_order_confirmation(self, order):
        """Send order confirmation message"""
        try:
            message = f"""✅ Order Confirmed!

Order #: {order.order_number}
Date: {order.order_date.strftime('%d-%b-%Y')}

Items: {order.items.count()} products
Subtotal: ₹{order.subtotal:,.2f}
GST (5%): ₹{order.tax_amount:,.2f}
Total: ₹{order.total_amount:,.2f}

Payment: {order.payment_terms or 'Credit'}
Status: {order.status.upper()}

Thank you for your order! 🙏

📞 9262650010
Mohi Industries"""
            
            return self.send_message(order.distributor.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending order confirmation: {str(e)}")
            return False, str(e)
    
    def send_invoice(self, order, pdf_url=None):
        """Send invoice PDF via WhatsApp"""
        try:
            message = f"""🧾 Invoice Generated

Invoice #: {order.order_number}
Date: {order.order_date.strftime('%d-%b-%Y')}
Amount: ₹{order.total_amount:,.2f}

Payment Status: {order.payment_status.upper()}
Amount Paid: ₹{order.paid_amount:,.2f}
Balance Due: ₹{order.total_amount - order.paid_amount:,.2f}

Thank you for your business! 🙏

📞 9262650010
Mohi Industries"""
            
            return self.send_message(order.distributor.phone, message, pdf_url)
            
        except Exception as e:
            logger.error(f"Error sending invoice: {str(e)}")
            return False, str(e)
    
    def send_payment_reminder(self, distributor, outstanding_amount, invoices):
        """Send payment reminder"""
        try:
            invoice_list = "\n".join([
                f"• {inv.order_number} - ₹{inv.total_amount - inv.paid_amount:,.2f}"
                for inv in invoices[:5]  # Show max 5 invoices
            ])
            
            message = f"""💰 Payment Reminder

Dear {distributor.business_name},

Outstanding Amount: ₹{outstanding_amount:,.2f}

Pending Invoices:
{invoice_list}

Please clear payment at earliest.

Bank Details:
State Bank of India
A/c: 1234567890
IFSC: SBIN0001234
Branch: Hajipur

📞 9262650010
Mohi Industries"""
            
            return self.send_message(distributor.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending payment reminder: {str(e)}")
            return False, str(e)
    
    def send_delivery_update(self, order, status="Out for Delivery"):
        """Send delivery status update"""
        try:
            message = f"""🚚 Delivery Update

Order #: {order.order_number}
Status: {status}

Distributor: {order.distributor.business_name}
Location: {order.distributor.city}

Expected Delivery: Today

For queries, call:
📞 9262650010

Thank you! 🙏
Mohi Industries"""
            
            return self.send_message(order.distributor.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending delivery update: {str(e)}")
            return False, str(e)
    
    def send_product_availability(self, distributor, products):
        """Send daily product availability"""
        try:
            product_list = "\n".join([
                f"• {p.name} - ₹{p.base_price:,.2f}"
                for p in products[:10]  # Show max 10 products
            ])
            
            message = f"""🌅 Good Morning!

Fresh products available today:

{product_list}

Reply with your order or call:
📞 9262650010

Order format:
Product name, Quantity

Example: Bread 400g, 50 pcs

Thank you! 🙏
Mohi Industries"""
            
            return self.send_message(distributor.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending product availability: {str(e)}")
            return False, str(e)
    
    def send_new_product_launch(self, distributor, product):
        """Send new product launch notification"""
        try:
            message = f"""🆕 New Product Alert!

Introducing:
{product.name}

Price: ₹{product.base_price:,.2f}
MRP: ₹{product.mrp:,.2f}
Pack Size: {product.pack_size}

{product.description or 'Fresh from Mohi Industries!'}

Order now!
📞 9262650010

Thank you! 🙏
Mohi Industries"""
            
            return self.send_message(distributor.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending new product launch: {str(e)}")
            return False, str(e)
    
    def send_credit_limit_warning(self, distributor):
        """Send credit limit warning"""
        try:
            available = distributor.credit_limit - distributor.outstanding_amount
            
            message = f"""⚠️ Credit Limit Alert

Dear {distributor.business_name},

Credit Used: ₹{distributor.outstanding_amount:,.2f}
Credit Limit: ₹{distributor.credit_limit:,.2f}
Available: ₹{available:,.2f}

Please clear pending payments to continue ordering.

📞 9262650010
Mohi Industries"""
            
            return self.send_message(distributor.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending credit limit warning: {str(e)}")
            return False, str(e)
    
    def send_bulk_message(self, distributors, message):
        """Send bulk message to multiple distributors"""
        results = []
        
        for distributor in distributors:
            success, msg_id = self.send_message(distributor.phone, message)
            results.append({
                'distributor': distributor.business_name,
                'phone': distributor.phone,
                'success': success,
                'message_id': msg_id
            })
        
        return results
    
    def send_festival_offer(self, distributor, offer_details):
        """Send festival offer message"""
        try:
            message = f"""🎉 {offer_details.get('title', 'Special Offer')}

{offer_details.get('description', '')}

Offer valid: {offer_details.get('valid_from')} to {offer_details.get('valid_to')}

Terms & Conditions:
{offer_details.get('terms', 'Minimum order quantity applies')}

Order now!
📞 9262650010

Thank you! 🙏
Mohi Industries"""
            
            return self.send_message(distributor.phone, message)
            
        except Exception as e:
            logger.error(f"Error sending festival offer: {str(e)}")
            return False, str(e)


# Convenience functions for easy import
def send_order_confirmation(order):
    """Quick function to send order confirmation"""
    service = WhatsAppService()
    return service.send_order_confirmation(order)


def send_invoice(order, pdf_url=None):
    """Quick function to send invoice"""
    service = WhatsAppService()
    return service.send_invoice(order, pdf_url)


def send_payment_reminder(distributor, outstanding_amount, invoices):
    """Quick function to send payment reminder"""
    service = WhatsAppService()
    return service.send_payment_reminder(distributor, outstanding_amount, invoices)


def send_delivery_update(order, status="Out for Delivery"):
    """Quick function to send delivery update"""
    service = WhatsAppService()
    return service.send_delivery_update(order, status)
