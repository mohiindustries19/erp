"""
Configuration for Mohi Industries ERP
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    # Fix Railway DATABASE_URL (postgres:// -> postgresql://)
    database_url = (
        os.environ.get('DATABASE_URL')
        or os.environ.get('POSTGRES_URL')
        or os.environ.get('POSTGRESQL_URL')
    )
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    if not database_url:
        # Build from Railway/PG* environment variables when DATABASE_URL is missing
        host = (
            os.environ.get('PGHOST')
            or os.environ.get('POSTGRES_HOST')
            or os.environ.get('POSTGRESQL_HOST')
        )
        port = (
            os.environ.get('PGPORT')
            or os.environ.get('POSTGRES_PORT')
            or os.environ.get('POSTGRESQL_PORT')
            or '5432'
        )
        user = (
            os.environ.get('PGUSER')
            or os.environ.get('POSTGRES_USER')
            or os.environ.get('POSTGRESQL_USER')
        )
        password = (
            os.environ.get('PGPASSWORD')
            or os.environ.get('POSTGRES_PASSWORD')
            or os.environ.get('POSTGRESQL_PASSWORD')
        )
        db_name = (
            os.environ.get('PGDATABASE')
            or os.environ.get('POSTGRES_DB')
            or os.environ.get('POSTGRESQL_DB')
        )

        if host and user and db_name:
            if password:
                database_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
            else:
                database_url = f"postgresql://{user}@{host}:{port}/{db_name}"

    SQLALCHEMY_DATABASE_URI = database_url or \
        'postgresql://mohi_admin:mohi_secure_2024@localhost:5435/mohi_erp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Company Details (Indian Compliance)
    COMPANY_NAME = os.environ.get('COMPANY_NAME', 'Mohi Industries')
    COMPANY_GSTIN = os.environ.get('COMPANY_GSTIN', '10GANPS5418H1ZJ')
    COMPANY_PAN = os.environ.get('COMPANY_PAN', 'XXXXX1234X')
    COMPANY_STATE = os.environ.get('COMPANY_STATE', 'Bihar')
    COMPANY_STATE_CODE = os.environ.get('COMPANY_STATE_CODE', '10')
    COMPANY_PHONE = os.environ.get('COMPANY_PHONE', '+91 9262650010')
    COMPANY_EMAIL = os.environ.get('COMPANY_EMAIL', 'info@mohiindustries.in')
    
    # FSSAI
    FSSAI_LICENSE = os.environ.get('FSSAI_LICENSE', '10423110000282')

    # Barcode / EAN-13
    # Set this to your GS1 company prefix (7-9 digits). For internal testing you can keep a dummy.
    BARCODE_COMPANY_PREFIX = os.environ.get('BARCODE_COMPANY_PREFIX', '890123456')
    
    # GST Rates (can be configured)
    GST_RATES = {
        'bakery': 5,      # 5% GST on bakery items
        'pickles': 12,    # 12% GST on pickles
        'water': 18       # 18% GST on packaged water
    }

    # GST API Configuration
    GST_PROVIDER = os.environ.get('GST_PROVIDER', 'cleartax')
    GST_API_KEY = os.environ.get('GST_API_KEY')
    GST_SANDBOX = os.environ.get('GST_SANDBOX', 'true').lower() in ['true', 'on', '1']
    
    # Business Rules
    MIN_ORDER_VALUE = 25000  # Minimum order ₹25,000
    DISTRIBUTOR_MARGIN_MIN = 12
    DISTRIBUTOR_MARGIN_MAX = 18
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@mohiindustries.in')
    
    # Email Settings
    SEND_PAYMENT_REMINDERS = os.environ.get('SEND_PAYMENT_REMINDERS', 'true').lower() in ['true', 'on', '1']
    SEND_LOW_STOCK_ALERTS = os.environ.get('SEND_LOW_STOCK_ALERTS', 'true').lower() in ['true', 'on', '1']
    SEND_ORDER_CONFIRMATIONS = os.environ.get('SEND_ORDER_CONFIRMATIONS', 'true').lower() in ['true', 'on', '1']
    PAYMENT_REMINDER_DAYS = int(os.environ.get('PAYMENT_REMINDER_DAYS', 7))  # Days after due date

    # WhatsApp Configuration
    WHATSAPP_ENABLED = os.environ.get('WHATSAPP_ENABLED', 'false').lower() in ['true', 'on', '1']
    WHATSAPP_PROVIDER = os.environ.get('WHATSAPP_PROVIDER', 'twilio')
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.environ.get('TWILIO_WHATSAPP_NUMBER', '+14155238886')
    
    # Gupshup Configuration
    GUPSHUP_API_KEY = os.environ.get('GUPSHUP_API_KEY')
    GUPSHUP_APP_NAME = os.environ.get('GUPSHUP_APP_NAME', 'MohiIndustries')
    
    # Interakt Configuration
    INTERAKT_API_KEY = os.environ.get('INTERAKT_API_KEY')
    INTERAKT_BASE_URL = os.environ.get('INTERAKT_BASE_URL', 'https://api.interakt.ai/v1')
    
    # Business Information (for WhatsApp messages)
    BUSINESS_NAME = os.environ.get('BUSINESS_NAME', 'Mohi Industries')
    BUSINESS_PHONE = os.environ.get('BUSINESS_PHONE', '9262650010')
    BUSINESS_ADDRESS = os.environ.get('BUSINESS_ADDRESS', 'Hajipur, Bihar')
    
    # Bank Details (for payment reminders)
    BANK_NAME = os.environ.get('BANK_NAME', 'State Bank of India')
    BANK_ACCOUNT = os.environ.get('BANK_ACCOUNT', '1234567890')
    BANK_IFSC = os.environ.get('BANK_IFSC', 'SBIN0001234')
    BANK_BRANCH = os.environ.get('BANK_BRANCH', 'Hajipur')
