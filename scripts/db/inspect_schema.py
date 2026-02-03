import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from sqlalchemy import inspect

def inspect_db():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Tables in database:", tables)
        
        print("\n--- FK Constraints for 'expenses' ---")
        fks = inspector.get_foreign_keys('expenses')
        for fk in fks:
            print(f"Column: {fk['constrained_columns']} -> RefTable: {fk['referred_table']} -> RefColumn: {fk['referred_columns']}")

        print("\n--- Columns in 'accounts' ---")
        if 'accounts' in tables:
            cols = inspector.get_columns('accounts')
            print([c['name'] for c in cols])
            
        print("\n--- Columns in 'chart_of_accounts' ---")
        if 'chart_of_accounts' in tables:
            cols = inspector.get_columns('chart_of_accounts')
            print([c['name'] for c in cols])
            
        # Check ID 18
        if 'chart_of_accounts' in tables:
            res = db.session.execute(db.text("SELECT * FROM chart_of_accounts WHERE id=18")).fetchone()
            print(f"\nID 18 in chart_of_accounts: {res}")
            
        if 'accounts' in tables:
            res = db.session.execute(db.text("SELECT * FROM accounts WHERE id=18")).fetchone()
            print(f"\nID 18 in accounts: {res}")

if __name__ == "__main__":
    inspect_db()
