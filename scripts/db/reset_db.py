import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from sqlalchemy import text

def reset_db():
    app = create_app()
    with app.app_context():
        try:
            # Rollback any pending transactions
            db.session.rollback()
            print("Rolled back any pending transactions.")
            
            # Test a simple query
            result = db.session.execute(text("SELECT 1")).scalar()
            print(f"DB Connection Test: {result}")
            
            # Test accounts table
            count = db.session.execute(text("SELECT count(*) FROM accounts")).scalar()
            print(f"Accounts in DB: {count}")
            
            # Test Bank accounts specifically (this was failing)
            bank_count = db.session.execute(text("SELECT count(*) FROM accounts WHERE account_type = 'Bank'")).scalar()
            print(f"Bank Accounts: {bank_count}")
            
            print("\nDatabase is healthy. Please restart the web container.")
            
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    reset_db()
