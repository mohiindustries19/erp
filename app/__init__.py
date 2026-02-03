"""
Mohi Industries ERP - Application Factory
"""
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.context_processor
    def _inject_template_helpers():
        from flask_login import current_user
        from app.routes.settings import get_active_theme
        
        # Get theme colors for current user
        theme_colors = {'primary': '#d00000', 'primary_hover': '#a80c06', 'primary_light': '#ff0000'}
        if current_user.is_authenticated:
            theme_colors = get_active_theme(current_user.id)
        
        return {
            'now': datetime.now,
            'theme_colors': theme_colors,
        }
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    from app.routes import auth, main, distributor, inventory, orders, payment, users, accounting, analytics, ai_chat, email_notifications, advanced_analytics, purchasing, gst, qc, whatsapp, documents, settings, barcode
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(distributor.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(payment.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(accounting.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(ai_chat.bp)
    app.register_blueprint(email_notifications.bp)
    app.register_blueprint(advanced_analytics.bp)
    app.register_blueprint(purchasing.bp)
    app.register_blueprint(gst.bp)
    app.register_blueprint(qc.bp)
    app.register_blueprint(whatsapp.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(barcode.bp)
    
    return app

from app import models
