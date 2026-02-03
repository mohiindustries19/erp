"""
Import Distributors from Bread Distributors List
Run this script to add all 68 distributors to the database
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models import Distributor
from datetime import date

# Distributor data from the list
distributors_data = [
    {"name": "Prem Kumar", "phone": "9955119700", "location": "Patna"},
    {"name": "Akash", "phone": "7992499443", "location": "Patna"},
    {"name": "Sanjay", "phone": "7004264955", "location": "patna"},
    {"name": "Amit", "phone": "9543704682", "location": "Nalanda"},
    {"name": "Babloo", "phone": "7903352850", "location": "Patna"},
    {"name": "Boby", "phone": "7903352850", "location": "Barbigha"},
    {"name": "Dharmendra", "phone": "8863084560", "location": "nawada"},
    {"name": "Din Dayal", "phone": "9334963677", "location": "nawada"},
    {"name": "Firoz", "phone": "9523054442", "location": "Patna"},
    {"name": "Ganesh", "phone": "8084658785", "location": "Darbhanga"},
    {"name": "Gulam", "phone": "9939205367", "location": "Patna"},
    {"name": "Gulam", "phone": "7903902954", "location": "Vaishali"},
    {"name": "Imteaz", "phone": "7324017471", "location": "Patna"},
    {"name": "Jamil", "phone": "7001609102", "location": "Patna"},
    {"name": "Jha ji", "phone": "9386444417", "location": "Dalsingh Sarai"},
    {"name": "Jitendra", "phone": "8210114050", "location": "Darbhanga"},
    {"name": "Jitu", "phone": "9534472488", "location": "lalganj"},
    {"name": "yogindra", "phone": "9631172843", "location": "Betiah"},
    {"name": "Kapil", "phone": "7492919141", "location": "Vaishali"},
    {"name": "Kundan", "phone": "7004793876", "location": "Vaishali"},
    {"name": "Lal babu", "phone": "8987333569", "location": "Madubani"},
    {"name": "Madav", "phone": "7631466462", "location": "Vaishali"},
    {"name": "Miya ji", "phone": "9631638353", "location": "Parsa"},
    {"name": "Nanad lal", "phone": "9801639930", "location": "Patna"},
    {"name": "Niraj", "phone": "7004490110", "location": "Vaishali"},
    {"name": "Olait Miya", "phone": "8757548024", "location": "Patna"},
    {"name": "Pappu", "phone": "9079697035", "location": "Motihari"},
    {"name": "Pawan", "phone": "9631360015", "location": "Vaishali"},
    {"name": "Pawan", "phone": "8083497127", "location": "Naya Gaun"},
    {"name": "Pinku", "phone": "9771590634", "location": "Patna"},
    {"name": "Pramod", "phone": "9934343530", "location": "Parsa"},
    {"name": "Rahul", "phone": "8340125651", "location": "Motihari"},
    {"name": "RajKumar", "phone": "9934125810", "location": "Chapra"},
    {"name": "Rajiv", "phone": "9122832964", "location": "Vaishali"},
    {"name": "Rajiv ji", "phone": "7349028295", "location": "Chapra"},
    {"name": "Rama Shanker", "phone": "9348969145", "location": "Patna"},
    {"name": "Ratan", "phone": "7320833918", "location": "Patna"},
    {"name": "Ravi", "phone": "6201026620", "location": "Vaishali"},
    {"name": "Ritesh", "phone": "8935803818", "location": "Vaishali"},
    {"name": "Samim", "phone": "7352150365", "location": "Vaishali"},
    {"name": "Sanjay", "phone": "9934426349", "location": "Vaishali"},
    {"name": "Sarfaraj", "phone": "8051265872", "location": "Darbhanga"},
    {"name": "Bhushan", "phone": "9939093735", "location": "Patna"},
    {"name": "Satendra", "phone": "9771647834", "location": "Patna"},
    {"name": "Shambhu", "phone": "8292271938", "location": "Vaishali"},
    {"name": "Suman ji", "phone": "8235656922", "location": "Vaishali"},
    {"name": "Sunil", "phone": "9955450317", "location": "Darbhanga"},
    {"name": "Sunil", "phone": "9431445225", "location": "Chapra"},
    {"name": "Surendra", "phone": "8651984975", "location": "Vaishali"},
    {"name": "Taj", "phone": "9162333900", "location": "Gopalganj"},
    {"name": "Binod", "phone": "6204202456", "location": "Vaishali"},
    {"name": "Chhotu", "phone": "8252316244", "location": "Nalanda"},
    {"name": "Santosh", "phone": "8434374611", "location": "Chapra"},
    {"name": "Tribhuan", "phone": "9547650591", "location": "Chapra"},
    {"name": "Babloo", "phone": "7482962790", "location": "Nalanda"},
    {"name": "Shyam", "phone": "9430274028", "location": "Nalanda"},
    {"name": "Babloo", "phone": "8539047035", "location": "Nalanda"},
    {"name": "Dinesh", "phone": "6200861721", "location": "Patna"},
    {"name": "Raushan", "phone": "9693841084", "location": "Patna"},
    {"name": "Vishwajit", "phone": "7493948449", "location": "Vaishali"},
    {"name": "Biddupur", "phone": "8409348802", "location": "Vaishali"},
    {"name": "Maniraj", "phone": "9934831476", "location": "Vaishali"},
    {"name": "Shyam ji", "phone": "7488275824", "location": "Vaishali"},
    {"name": "Dharmendra", "phone": "7470946541", "location": "Vaishali"},
    {"name": "Anil ji", "phone": "9304998935", "location": "Patna"},
    {"name": "Ashok Ji", "phone": "7992312460", "location": "Patna"},
    {"name": "Rahul", "phone": "0000000000", "location": "Vaishali"},
    {"name": "Chitranjan", "phone": "8540896501", "location": "Patna"},
]

def get_state_code(location):
    """Get Bihar state code"""
    return "10"  # Bihar state code

def import_distributors():
    """Import all distributors into the database"""
    app = create_app()
    
    with app.app_context():
        print("Starting distributor import...")
        print(f"Total distributors to import: {len(distributors_data)}")
        
        added = 0
        skipped = 0
        updated = 0
        
        for idx, data in enumerate(distributors_data, 1):
            try:
                # Check if distributor already exists by phone
                existing = Distributor.query.filter_by(phone=data['phone']).first()
                
                if existing and data['phone'] != '0000000000':
                    # Update existing distributor
                    existing.business_name = data['name']
                    existing.contact_person = data['name']
                    existing.city = data['location'].title()
                    existing.state = 'Bihar'
                    existing.territory = data['location'].title()
                    updated += 1
                    print(f"{idx}. Updated: {data['name']} - {data['phone']} ({data['location']})")
                else:
                    # Generate unique code
                    last_dist = Distributor.query.order_by(Distributor.id.desc()).first()
                    next_num = (last_dist.id + 1) if last_dist else 1
                    code = f'DIST{next_num:04d}'
                    
                    # Create new distributor
                    distributor = Distributor(
                        code=code,
                        business_name=data['name'],
                        contact_person=data['name'],
                        phone=data['phone'],
                        email=None,
                        gstin=None,
                        pan=None,
                        address_line1=data['location'].title(),
                        address_line2=None,
                        city=data['location'].title(),
                        state='Bihar',
                        state_code=get_state_code(data['location']),
                        pincode=None,
                        territory=data['location'].title(),
                        margin_percentage=12.0,
                        credit_limit=50000.0,
                        credit_days=30,
                        payment_terms='credit',
                        status='active',
                        onboarding_date=date.today()
                    )
                    
                    db.session.add(distributor)
                    added += 1
                    print(f"{idx}. Added: {code} - {data['name']} - {data['phone']} ({data['location']})")
                
            except Exception as e:
                print(f"{idx}. ERROR: {data['name']} - {str(e)}")
                skipped += 1
                continue
        
        # Commit all changes
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("IMPORT COMPLETED SUCCESSFULLY!")
            print("="*60)
            print(f"✅ Added: {added} distributors")
            print(f"🔄 Updated: {updated} distributors")
            print(f"⚠️  Skipped: {skipped} distributors")
            print(f"📊 Total: {added + updated} distributors in database")
            print("="*60)
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR committing to database: {str(e)}")
            return False
        
        return True

if __name__ == '__main__':
    success = import_distributors()
    sys.exit(0 if success else 1)
