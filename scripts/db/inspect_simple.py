import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from sqlalchemy import inspect

def list_tables():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        print("TABLES:", inspector.get_table_names())

if __name__ == "__main__":
    list_tables()
