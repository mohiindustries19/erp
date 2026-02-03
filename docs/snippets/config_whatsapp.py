"""
WhatsApp Configuration
Add these settings to your .env file or config.py
"""

# ============================================
# WhatsApp Configuration
# ============================================

# Enable/Disable WhatsApp
WHATSAPP_ENABLED = False  # Set to True when ready to use

# Choose Provider: 'twilio', 'gupshup', or 'interakt'
WHATSAPP_PROVIDER = 'twilio'

# ============================================
# Twilio Configuration
# ============================================
# Sign up at: https://www.twilio.com/
# Cost: ~$0.005 per message

TWILIO_ACCOUNT_SID = 'your_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_auth_token_here'
TWILIO_WHATSAPP_NUMBER = '+14155238886'  # Twilio Sandbox number (for testing)
# For production, get your own WhatsApp Business number

# ============================================
# Gupshup Configuration
# ============================================
# Sign up at: https://www.gupshup.io/
# Cost: ~₹0.25-0.50 per message

GUPSHUP_API_KEY = 'your_gupshup_api_key_here'
GUPSHUP_APP_NAME = 'MohiIndustries'

# ============================================
# Interakt Configuration
# ============================================
# Sign up at: https://www.interakt.shop/
# Cost: Plans start at ₹5,000/month

INTERAKT_API_KEY = 'your_interakt_api_key_here'
INTERAKT_BASE_URL = 'https://api.interakt.ai/v1'

# ============================================
# Message Settings
# ============================================

# Business Information (used in messages)
BUSINESS_NAME = 'Mohi Industries'
BUSINESS_PHONE = '9262650010'
BUSINESS_ADDRESS = 'Hajipur Industrial Area, Hajipur, Bihar 844102'

# Bank Details (for payment reminders)
BANK_NAME = 'State Bank of India'
BANK_ACCOUNT = '1234567890'
BANK_IFSC = 'SBIN0001234'
BANK_BRANCH = 'Hajipur'

# Message Timing
MORNING_MESSAGE_TIME = '06:00'  # Daily product availability
EVENING_MESSAGE_TIME = '18:00'  # Payment reminders
PAYMENT_REMINDER_DAYS = [1, 3, 7]  # Days before due date to send reminders

# Message Limits (to avoid spam)
MAX_MESSAGES_PER_DAY = 10  # Per distributor
MAX_BULK_MESSAGES = 100  # Per batch

# ============================================
# Template IDs (for approved templates)
# ============================================
# After getting templates approved by WhatsApp, add their IDs here

TEMPLATE_ORDER_CONFIRMATION = 'order_confirmation_v1'
TEMPLATE_PAYMENT_REMINDER = 'payment_reminder_v1'
TEMPLATE_DELIVERY_UPDATE = 'delivery_update_v1'
TEMPLATE_PRODUCT_AVAILABILITY = 'product_availability_v1'
TEMPLATE_NEW_PRODUCT = 'new_product_launch_v1'
TEMPLATE_FESTIVAL_OFFER = 'festival_offer_v1'
