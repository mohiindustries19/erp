import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from sqlalchemy import inspect, text

def fix_all_fks():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("Scanning for FKs pointing to 'chart_of_accounts'...")
        
        fks_to_fix = []
        
        for table in tables:
            fks = inspector.get_foreign_keys(table)
            for fk in fks:
                if fk['referred_table'] == 'chart_of_accounts':
                    print(f"FOUND MATCH: Table '{table}' column {fk['constrained_columns']} -> chart_of_accounts")
                    fks_to_fix.append({
                        'table': table,
                        'fk_name': fk['name'],
                        'column': fk['constrained_columns'][0] # Assuming single column FK for now
                    })

        if not fks_to_fix:
            print("No FKs found pointing to chart_of_accounts.")
            return

        print(f"\nFound {len(fks_to_fix)} constraints to fix. Proceeding...")
        
        for item in fks_to_fix:
            table = item['table']
            fk_name = item['fk_name']
            column = item['column']
            
            print(f"Fixing {table}.{column}...")
            
            try:
                # Drop old constraint
                if fk_name:
                    drop_sql = f"ALTER TABLE {table} DROP CONSTRAINT {fk_name}"
                else:
                    # Fallback if name is missing (unlikely for inspection)
                    print(f"Skipping {table} due to missing FK name")
                    continue
                    
                print(f"  Executing: {drop_sql}")
                db.session.execute(text(drop_sql))
                
                # Add new constraint
                # We assume the target column in 'accounts' is 'id'
                new_fk_name = f"{table}_{column}_fkey_fixed"
                add_sql = f"ALTER TABLE {table} ADD CONSTRAINT {new_fk_name} FOREIGN KEY ({column}) REFERENCES accounts (id)"
                print(f"  Executing: {add_sql}")
                db.session.execute(text(add_sql))
                
                db.session.commit()
                print("  Success!")
                
            except Exception as e:
                db.session.rollback()
                print(f"  FAILED: {e}")

if __name__ == "__main__":
    fix_all_fks()
