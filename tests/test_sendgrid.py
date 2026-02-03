#!/usr/bin/env python3
"""
Test SendGrid Email Configuration
"""
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

def test_sendgrid():
    """Test SendGrid SMTP connection and send test email"""
    
    # Get configuration from .env
    mail_server = os.getenv('MAIL_SERVER', 'smtp.sendgrid.net')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    mail_sender = os.getenv('MAIL_DEFAULT_SENDER')
    
    print("=" * 60)
    print("SendGrid Email Configuration Test")
    print("=" * 60)
    print(f"Server: {mail_server}")
    print(f"Port: {mail_port}")
    print(f"Username: {mail_username}")
    print(f"Password: {'*' * 20 if mail_password else 'NOT SET'}")
    print(f"Sender: {mail_sender}")
    print("=" * 60)
    
    if not mail_username or not mail_password:
        print("ERROR: MAIL_USERNAME or MAIL_PASSWORD not set in .env file")
        return False
    
    try:
        print("\nConnecting to SendGrid SMTP server...")
        
        # Create SMTP connection
        server = smtplib.SMTP(mail_server, mail_port, timeout=10)
        server.set_debuglevel(1)  # Show detailed debug info
        
        print("\nStarting TLS encryption...")
        server.starttls()
        
        print("\nAuthenticating with SendGrid...")
        server.login(mail_username, mail_password)
        
        print("\nOK: Authentication successful")
        
        # Create test email
        msg = MIMEMultipart()
        msg['From'] = mail_sender
        msg['To'] = mail_sender  # Send to yourself for testing
        msg['Subject'] = 'Mohi Industries ERP - SendGrid Test Email'
        
        body = """
        <html>
        <body>
            <h2>SendGrid Configuration Test</h2>
            <p>This is a test email from Mohi Industries ERP system.</p>
            <p>If you received this email, your SendGrid configuration is working correctly!</p>
            <hr>
            <p><strong>Configuration Details:</strong></p>
            <ul>
                <li>Server: {}</li>
                <li>Port: {}</li>
                <li>Sender: {}</li>
            </ul>
            <p style="color: green;"><strong>SendGrid is configured and working.</strong></p>
        </body>
        </html>
        """.format(mail_server, mail_port, mail_sender)
        
        msg.attach(MIMEText(body, 'html'))
        
        print(f"\nSending test email to {mail_sender}...")
        server.send_message(msg)
        
        print("\nOK: Test email sent successfully")
        print(f"Check your inbox at: {mail_sender}")
        
        server.quit()
        
        print("\n" + "=" * 60)
        print("OK: SendGrid Configuration Test: PASSED")
        print("=" * 60)
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\nERROR: Authentication Error: {e}")
        print("\nPossible issues:")
        print("1. Invalid SendGrid API key")
        print("2. API key doesn't have 'Mail Send' permission")
        print("3. Check your API key at: https://app.sendgrid.com/settings/api_keys")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\nERROR: SMTP Error: {e}")
        return False
        
    except Exception as e:
        print(f"\nERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_sendgrid()
    exit(0 if success else 1)
