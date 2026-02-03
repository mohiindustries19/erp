"""
First WhatsApp Broadcast - Send to 5 Test Distributors
Run this to send your first real broadcast!
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.models import Distributor, Product
from app.services.whatsapp import WhatsAppService

def send_first_broadcast():
    """Send product availability to first 5 distributors"""
    app = create_app()
    
    with app.app_context():
        print("="*60)
        print("FIRST WHATSAPP BROADCAST")
        print("Mohi Industries - Product Availability")
        print("="*60)
        
        # Get first 5 active distributors
        distributors = Distributor.query.filter_by(status='active').limit(5).all()
        
        if not distributors:
            print("\n❌ No distributors found!")
            return
        
        print(f"\n📱 Found {len(distributors)} distributors:")
        for i, dist in enumerate(distributors, 1):
            print(f"   {i}. {dist.business_name} - {dist.phone} ({dist.city})")
        
        # Get active products
        products = Product.query.filter_by(is_active=True).limit(10).all()
        
        print(f"\n📦 Products to send: {len(products)}")
        for p in products[:5]:
            print(f"   • {p.name} - ₹{p.base_price}")
        
        # Confirm
        print("\n" + "="*60)
        confirm = input("Send WhatsApp to these 5 distributors? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("\n❌ Cancelled")
            return
        
        # Send messages
        service = WhatsAppService()
        
        print("\n📤 Sending messages...")
        print("-"*60)
        
        success_count = 0
        failed_count = 0
        
        for i, distributor in enumerate(distributors, 1):
            print(f"\n{i}. Sending to {distributor.business_name}...")
            
            success, msg_id = service.send_product_availability(distributor, products)
            
            if success:
                print(f"   ✅ Sent! Message ID: {msg_id}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {msg_id}")
                failed_count += 1
        
        # Summary
        print("\n" + "="*60)
        print("BROADCAST COMPLETE!")
        print("="*60)
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📊 Total: {success_count + failed_count}")
        print("="*60)
        
        if success_count > 0:
            print("\n🎉 Great! Your first broadcast is sent!")
            print("\n📱 Next Steps:")
            print("   1. Check WhatsApp responses")
            print("   2. Note which distributors respond")
            print("   3. Take orders from interested distributors")
            print("   4. Tomorrow: Send to all 68 distributors!")
        
        return success_count > 0

if __name__ == '__main__':
    success = send_first_broadcast()
    sys.exit(0 if success else 1)
