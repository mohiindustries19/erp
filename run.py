"""
Mohi Industries ERP - Main Application Entry Point
ॐ श्री गणेशाय नमः
"""
import os
from app import create_app, db
from app.models import User, Company

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Company': Company}

if __name__ == '__main__':
    flask_env = os.getenv('FLASK_ENV', 'development').lower()
    port = int(os.getenv('PORT', '5000'))

    # Avoid creating tables automatically on startup. In Docker/Railway the DB may not be ready yet,
    # and creating tables is better handled by migrations or an explicit init step.
    auto_create_db = os.getenv('AUTO_CREATE_DB', 'false').lower() in ['true', '1', 'on', 'yes']
    if auto_create_db:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully (AUTO_CREATE_DB enabled).")

    debug = flask_env == 'development'
    print("Starting Mohi Industries ERP...")
    print(f"Access at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
