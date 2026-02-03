"""
Daily Product Availability Broadcast
Send to ALL 68 distributors every morning
"""
import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.models import Distributor, Product
from app.services.whatsapp import WhatsAppService

def send_daily_broadcast():
    """Send product availability to all active distributors"""
    app = create_app()
    
    with app.app_context():
        print("="*60)
        print("DAILY PRODUCT AVAILABILITY BROADCAST")
        print(f"Date: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
        print("="*60)
        
        # Get all active distributors
        distributors = Distributor.query.filter_by(status='active').all()
        
        if not distributors:
            print("\n❌ No active distributors found!")
            return False
        
        print(f"\n📱 Total Distributors: {len(distributors)}")
        
        # Group by location
        locations = {}
        for dist in distributors:
            if dist.city not in locations:
                locations[dist.city] = []
            locations[dist.city].append(dist)
        
        print(f"📍 Locations: {len(locations)}")
        for city, dists in sorted(locations.items()):
            print(f"   • {city}: {len(dists)} distributors")
        
        # Get active products
        products = Product.query.filter_by(is_active=True).all()
        
        print(f"\n📦 Products Available: {len(products)}")
        print("\nTop 10 Products:")
        for p in products[:10]:
            print(f"   • {p.name} - ₹{p.base_price}")
        
        # Confirm
        print("\n" + "="*60)
        print("⚠️  This will send WhatsApp to ALL distributors!")
        print("="*60)
        confirm = input(f"Send to all {len(distributors)} distributors? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("\n❌ Cancelled")
            return False
        
        # Send messages
        service = WhatsAppService()
        
        print("\n📤 Sending messages...")
        print("-"*60)
        
        success_count = 0
        failed_count = 0
        results = []
        
        for i, distributor in enumerate(distributors, 1):
            print(f"\r{i}/{len(distributors)} - {distributor.business_name[:30]:<30}", end='', flush=True)
            
            success, msg_id = service.send_product_availability(distributor, products)
            
            results.append({
                'distributor': distributor.business_name,
                'city': distributor.city,
                'phone': distributor.phone,
                'success': success,
                'message_id': msg_id if success else None,
                'error': msg_id if not success else None
            })
            
            if success:
                success_count += 1
            else:
                failed_count += 1
        
        print("\n")
        
        # Summary
        print("\n" + "="*60)
        print("BROADCAST COMPLETE!")
        print("="*60)
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📊 Success Rate: {(success_count/len(distributors)*100):.1f}%")
        print("="*60)
        
        # Show failures if any
        if failed_count > 0:
            print("\n❌ Failed Messages:")
            for r in results:
                if not r['success']:
                    print(f"   • {r['distributor']} ({r['phone']}): {r['error']}")
        
        # Show success by location
        print("\n✅ Success by Location:")
        location_stats = {}
        for r in results:
            city = r['city']
            if city not in location_stats:
                location_stats[city] = {'success': 0, 'total': 0}
            location_stats[city]['total'] += 1
            if r['success']:
                location_stats[city]['success'] += 1
        
        for city, stats in sorted(location_stats.items()):
            rate = (stats['success']/stats['total']*100)
            print(f"   • {city}: {stats['success']}/{stats['total']} ({rate:.0f}%)")
        
        # Next steps
        if success_count > 0:
            print("\n" + "="*60)
            print("🎉 BROADCAST SENT SUCCESSFULLY!")
            print("="*60)
            print("\n📱 What to do now:")
            print("   1. Monitor WhatsApp for responses")
            print("   2. Note which distributors want to order")
            print("   3. Create orders in ERP")
            print("   4. Send order confirmations (automatic)")
            print("   5. Track responses and feedback")
            print("\n💡 Tip: Best time to send is 6:00 AM daily")
            print("   Set up Windows Task Scheduler to automate!")
        
        # Save log
        log_file = f"broadcast_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'w') as f:
            f.write(f"Broadcast Date: {datetime.now()}\n")
            f.write(f"Total Distributors: {len(distributors)}\n")
            f.write(f"Successful: {success_count}\n")
            f.write(f"Failed: {failed_count}\n\n")
            f.write("Results:\n")
            for r in results:
                status = "✅" if r['success'] else "❌"
                f.write(f"{status} {r['distributor']} ({r['city']}) - {r['phone']}\n")
        
        print(f"\n📄 Log saved: {log_file}")
        
        return success_count > 0

if __name__ == '__main__':
    success = send_daily_broadcast()
    sys.exit(0 if success else 1)
