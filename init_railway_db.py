"""
Initialize Database for Railway Deployment
Run this after first deployment to create admin user
"""
from app import create_app, db
from app.models import User, Company
from werkzeug.security import generate_password_hash
import os

app = create_app()

with app.app_context():
    print("🔧 Initializing database...")
    
    # Create all tables
    db.create_all()
    print("✅ Database tables created")
    
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@mohiindustries.in',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")
        print("   Username: admin")
        print("   Password: admin123")
        print("   ⚠️  CHANGE PASSWORD IMMEDIATELY!")
    else:
        print("ℹ️  Admin user already exists")
    
    # Check if company exists
    company = Company.query.first()
    
    if not company:
        # Create company
        company = Company(
            name=os.getenv('COMPANY_NAME', 'Mohi Industries'),
            gstin=os.getenv('COMPANY_GSTIN', '10GANPS5418H1ZJ'),
            pan=os.getenv('COMPANY_PAN', 'XXXXX1234X'),
            state=os.getenv('COMPANY_STATE', 'Bihar'),
            state_code=os.getenv('COMPANY_STATE_CODE', '10'),
            address='B-61, P-1, BIADA, Hajipur, Vaishali, Bihar - 844102',
            phone=os.getenv('COMPANY_PHONE', '+91 9262650010'),
            email=os.getenv('COMPANY_EMAIL', 'info@mohiindustries.in'),
            fssai_license=os.getenv('FSSAI_LICENSE', '10423110000282')
        )
        db.session.add(company)
        db.session.commit()
        print("✅ Company profile created")
    else:
        print("ℹ️  Company profile already exists")
    
    print("\n🎉 Database initialization complete!")
    print(f"🌐 Access your ERP at: {os.getenv('RAILWAY_PUBLIC_DOMAIN', 'your-app-url.railway.app')}")
