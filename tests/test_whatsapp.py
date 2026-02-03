"""
WhatsApp Integration Test Script
Test your WhatsApp configuration before going live
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.services.whatsapp import WhatsAppService
from app.models import Distributor, Order, Product

def test_configuration():
    """Test WhatsApp configuration"""
    print("="*60)
    print("WhatsApp Configuration Test")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        service = WhatsAppService()
        
        print(f"\n✓ Provider: {service.provider}")
        print(f"✓ Enabled: {service.enabled}")
        
        if not service.enabled:
            print("\n⚠️  WhatsApp is DISABLED")
            print("   Set WHATSAPP_ENABLED=True in .env to enable")
            return False
        
        print("\n✓ Configuration loaded successfully!")
        return True


def test_send_message():
    """Test sending a simple message"""
    print("\n" + "="*60)
    print("Test Message Send")
    print("="*60)
    
    phone = input("\nEnter your phone number (10 digits): ")
    
    if len(phone) != 10 or not phone.isdigit():
        print("❌ Invalid phone number")
        return False
    
    app = create_app()
    
    with app.app_context():
        service = WhatsAppService()
        
        message = """🧪 Test Message from Mohi Industries ERP

This is a test message to verify WhatsApp integration.

If you received this, your configuration is working! ✅

📞 9262650010
Mohi Industries"""
        
        print(f"\nSending test message to +91{phone}...")
        
        success, msg_id = service.send_message(phone, message)
        
        if success:
            print(f"\n✅ Message sent successfully!")
            print(f"   Message ID: {msg_id}")
            return True
        else:
            print(f"\n❌ Failed to send message")
            print(f"   Error: {msg_id}")
            return False


def test_order_confirmation():
    """Test order confirmation message"""
    print("\n" + "="*60)
    print("Test Order Confirmation")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Get first order
        order = Order.query.first()
        
        if not order:
            print("\n⚠️  No orders found in database")
            print("   Create an order first to test this feature")
            return False
        
        print(f"\nUsing order: {order.order_number}")
        print(f"Distributor: {order.distributor.business_name}")
        print(f"Phone: {order.distributor.phone}")
        
        confirm = input("\nSend order confirmation to this distributor? (y/n): ")
        
        if confirm.lower() != 'y':
            print("Cancelled")
            return False
        
        service = WhatsAppService()
        success, msg_id = service.send_order_confirmation(order)
        
        if success:
            print(f"\n✅ Order confirmation sent!")
            print(f"   Message ID: {msg_id}")
            return True
        else:
            print(f"\n❌ Failed to send confirmation")
            print(f"   Error: {msg_id}")
            return False


def test_product_availability():
    """Test product availability message"""
    print("\n" + "="*60)
    print("Test Product Availability")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Get first distributor
        distributor = Distributor.query.filter_by(status='active').first()
        
        if not distributor:
            print("\n⚠️  No active distributors found")
            return False
        
        # Get products
        products = Product.query.filter_by(is_active=True).limit(5).all()
        
        if not products:
            print("\n⚠️  No active products found")
            return False
        
        print(f"\nDistributor: {distributor.business_name}")
        print(f"Phone: {distributor.phone}")
        print(f"\nProducts to send ({len(products)}):")
        for p in products:
            print(f"  • {p.name} - ₹{p.base_price}")
        
        confirm = input("\nSend product availability? (y/n): ")
        
        if confirm.lower() != 'y':
            print("Cancelled")
            return False
        
        service = WhatsAppService()
        success, msg_id = service.send_product_availability(distributor, products)
        
        if success:
            print(f"\n✅ Product availability sent!")
            print(f"   Message ID: {msg_id}")
            return True
        else:
            print(f"\n❌ Failed to send message")
            print(f"   Error: {msg_id}")
            return False


def test_payment_reminder():
    """Test payment reminder message"""
    print("\n" + "="*60)
    print("Test Payment Reminder")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Find distributor with pending payments
        from sqlalchemy import func
        
        result = app.db.session.query(
            Distributor,
            func.sum(Order.total_amount - Order.paid_amount).label('outstanding')
        ).join(Order).filter(
            Order.payment_status.in_(['pending', 'partial'])
        ).group_by(Distributor.id).first()
        
        if not result:
            print("\n⚠️  No distributors with pending payments")
            return False
        
        distributor, outstanding = result
        
        # Get pending invoices
        invoices = Order.query.filter(
            Order.distributor_id == distributor.id,
            Order.payment_status.in_(['pending', 'partial'])
        ).all()
        
        print(f"\nDistributor: {distributor.business_name}")
        print(f"Phone: {distributor.phone}")
        print(f"Outstanding: ₹{outstanding:,.2f}")
        print(f"Pending invoices: {len(invoices)}")
        
        confirm = input("\nSend payment reminder? (y/n): ")
        
        if confirm.lower() != 'y':
            print("Cancelled")
            return False
        
        service = WhatsAppService()
        success, msg_id = service.send_payment_reminder(distributor, outstanding, invoices)
        
        if success:
            print(f"\n✅ Payment reminder sent!")
            print(f"   Message ID: {msg_id}")
            return True
        else:
            print(f"\n❌ Failed to send reminder")
            print(f"   Error: {msg_id}")
            return False


def main():
    """Main test menu"""
    print("\n" + "="*60)
    print("WhatsApp Integration Test Suite")
    print("Mohi Industries ERP")
    print("="*60)
    
    # Test configuration first
    if not test_configuration():
        print("\n❌ Configuration test failed")
        print("   Please configure WhatsApp in .env file")
        sys.exit(1)
    
    while True:
        print("\n" + "="*60)
        print("Select Test:")
        print("="*60)
        print("1. Send test message to your phone")
        print("2. Send order confirmation")
        print("3. Send product availability")
        print("4. Send payment reminder")
        print("5. Exit")
        print("="*60)
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            test_send_message()
        elif choice == '2':
            test_order_confirmation()
        elif choice == '3':
            test_product_availability()
        elif choice == '4':
            test_payment_reminder()
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid choice")
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
