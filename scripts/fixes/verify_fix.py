import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from sqlalchemy import inspect

def verify():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        fks = inspector.get_foreign_keys('expenses')
        
        found = False
        for fk in fks:
            print(f"FK: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
            if fk['referred_table'] == 'accounts':
                found = True
        
        if found:
            print("SUCCESS: Foreign Key points to 'accounts'.")
        else:
            print("FAILURE: Foreign Key does NOT point to 'accounts'.")

if __name__ == "__main__":
    verify()
