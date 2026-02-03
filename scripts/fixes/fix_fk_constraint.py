import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from sqlalchemy import text

def fix_fk():
    app = create_app()
    with app.app_context():
        # Check row counts
        try:
            res_acc = db.session.execute(text("SELECT count(*) FROM accounts")).scalar()
            print(f"Rows in 'accounts': {res_acc}")
        except Exception as e:
            print(f"Error reading 'accounts': {e}")
            res_acc = 0
            
        try:
            res_chart = db.session.execute(text("SELECT count(*) FROM chart_of_accounts")).scalar()
            print(f"Rows in 'chart_of_accounts': {res_chart}")
        except Exception as e:
            print(f"Error reading 'chart_of_accounts': {e}") # Table might not exist
            res_chart = 0

        # If accounts has data and is the one we want
        if res_acc > 0:
            print("Pointing FK to 'accounts' table...")
            try:
                # Dropping old constraint
                db.session.execute(text("ALTER TABLE expenses DROP CONSTRAINT IF EXISTS expenses_account_id_fkey"))
                
                # Adding new constraint pointing to accounts
                db.session.execute(text("ALTER TABLE expenses ADD CONSTRAINT expenses_account_id_fkey FOREIGN KEY (account_id) REFERENCES accounts (id)"))
                
                db.session.commit()
                print("Successfully updated FK constraint to point to 'accounts'.")
            except Exception as e:
                db.session.rollback()
                print(f"Error updating FK: {e}")
        else:
            print("WARNING: 'accounts' table seems empty. tailored fix aborted.")

if __name__ == "__main__":
    fix_fk()
