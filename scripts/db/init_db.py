"""
Database Initialization Script
Creates tables and adds sample data for Mohi Industries
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models import (User, Company, Distributor, Product, ProductCategory, 
                        Warehouse, Inventory, Batch)
from datetime import datetime, date, timedelta

def init_database():
    app = create_app()
    
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating database tables...")
        db.create_all()
        
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@mohiindustries.in',
            full_name='Admin User',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        print("Creating company profile...")
        company = Company(
            name='Mohi Industries',
            gstin='10GANPS5418H1ZJ',
            pan='XXXXX1234X',
            fssai_license='10423110000282',
            address_line1='4-1, Plot No G-2, Industrial Area Road',
            city='Hajipur',
            state='Bihar',
            state_code='10',
            pincode='844102',
            phone='+91 9262650010',
            email='info@mohiindustries.in',
            website='https://mohiindustries.in'
        )
        db.session.add(company)
        
        print("Creating product categories...")
        categories = [
            ProductCategory(name='Bakery Products', code='BAK', hsn_code='19059020', gst_rate=5.0),
            ProductCategory(name='Pickles', code='PCK', hsn_code='20019000', gst_rate=12.0),
            ProductCategory(name='Packaged Water', code='WAT', hsn_code='22021000', gst_rate=18.0)
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        
        print("Creating sample products...")
        products = [
            # Bakery
            Product(sku='BAK001', name='White Bread 400g', category_id=1, 
                   hsn_code='19059020', gst_rate=5.0, shelf_life_days=5,
                   pack_size='400g', unit='pcs', mrp=40.0, base_price=32.0, cost_price=25.0),
            Product(sku='BAK002', name='Brown Bread 400g', category_id=1,
                   hsn_code='19059020', gst_rate=5.0, shelf_life_days=5,
                   pack_size='400g', unit='pcs', mrp=50.0, base_price=40.0, cost_price=32.0),
            Product(sku='BAK003', name='Pav Bread 6pcs', category_id=1,
                   hsn_code='19059020', gst_rate=5.0, shelf_life_days=3,
                   pack_size='6pcs', unit='pack', mrp=30.0, base_price=24.0, cost_price=18.0),
            
            # Pickles
            Product(sku='PCK001', name='Mango Pickle 500g', category_id=2,
                   hsn_code='20019000', gst_rate=12.0, shelf_life_days=365,
                   pack_size='500g', unit='jar', mrp=150.0, base_price=120.0, cost_price=90.0),
            Product(sku='PCK002', name='Mixed Pickle 500g', category_id=2,
                   hsn_code='20019000', gst_rate=12.0, shelf_life_days=365,
                   pack_size='500g', unit='jar', mrp=140.0, base_price=112.0, cost_price=85.0),
            
            # Water
            Product(sku='WAT001', name='Mohi Neer 500ml', category_id=3,
                   hsn_code='22021000', gst_rate=18.0, shelf_life_days=180,
                   pack_size='500ml', unit='bottle', mrp=20.0, base_price=16.0, cost_price=10.0),
            Product(sku='WAT002', name='Mohi Neer 1L', category_id=3,
                   hsn_code='22021000', gst_rate=18.0, shelf_life_days=180,
                   pack_size='1L', unit='bottle', mrp=35.0, base_price=28.0, cost_price=18.0),
        ]
        for product in products:
            db.session.add(product)
        db.session.commit()
        
        print("Creating warehouses...")
        warehouses = [
            Warehouse(code='WH01', name='Main Factory Warehouse', city='Mumbai', state='Maharashtra'),
            Warehouse(code='WH02', name='Delhi Distribution Center', city='Delhi', state='Delhi'),
            Warehouse(code='WH03', name='Bangalore Hub', city='Bangalore', state='Karnataka')
        ]
        for wh in warehouses:
            db.session.add(wh)
        db.session.commit()
        
        print("Creating sample batches...")
        today = date.today()
        batches = [
            Batch(batch_number='BAK001-20240126-001', product_id=1, 
                 manufacturing_date=today, expiry_date=today + timedelta(days=5),
                 quantity_produced=1000, quantity_available=1000, warehouse_id=1, qc_status='passed'),
            Batch(batch_number='PCK001-20240101-001', product_id=4,
                 manufacturing_date=date(2024, 1, 1), expiry_date=date(2025, 1, 1),
                 quantity_produced=500, quantity_available=500, warehouse_id=1, qc_status='passed'),
            Batch(batch_number='WAT001-20240115-001', product_id=6,
                 manufacturing_date=date(2024, 1, 15), expiry_date=date(2024, 7, 15),
                 quantity_produced=5000, quantity_available=5000, warehouse_id=1, qc_status='passed'),
        ]
        for batch in batches:
            db.session.add(batch)
        db.session.commit()
        
        print("Creating sample distributors...")
        distributors = [
            Distributor(
                code='DIST0001', business_name='Mumbai Retail Traders',
                contact_person='Rajesh Kumar', phone='+91 9876543210',
                email='rajesh@example.com', gstin='27AAAAA1234A1Z5',
                city='Mumbai', state='Maharashtra', state_code='27',
                territory='Mumbai Central', margin_percentage=15.0,
                credit_limit=100000, payment_terms='credit', status='active'
            ),
            Distributor(
                code='DIST0002', business_name='Delhi Food Distributors',
                contact_person='Amit Sharma', phone='+91 9876543211',
                email='amit@example.com', gstin='07BBBBB5678B1Z5',
                city='Delhi', state='Delhi', state_code='07',
                territory='Delhi NCR', margin_percentage=14.0,
                credit_limit=150000, payment_terms='credit', status='active'
            ),
        ]
        for dist in distributors:
            db.session.add(dist)
        db.session.commit()
        
        print("Database initialized successfully.")
        print("\nLogin Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\nStart the application with: python run.py")

if __name__ == '__main__':
    init_database()
