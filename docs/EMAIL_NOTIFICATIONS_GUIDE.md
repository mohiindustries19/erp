# Email Notifications Guide - Mohi Industries ERP

## 📧 Overview

Automated email notifications keep your customers informed and reduce manual follow-up work. The system sends professional HTML emails for various events.

---

## 🚀 Quick Setup (10 Minutes)

### Step 1: Choose Email Service

**Option A: Gmail (Easiest)**
1. Use your Gmail account
2. Enable 2-Factor Authentication
3. Generate App Password: https://myaccount.google.com/apppasswords
4. Use app password (not your regular password)

**Option B: SendGrid (Recommended for Production)**
1. Sign up at https://sendgrid.com (Free tier: 100 emails/day)
2. Verify your sender email
3. Get API key
4. Use SMTP relay

**Option C: AWS SES (Best for Scale)**
1. Sign up for AWS SES
2. Verify domain
3. Get SMTP credentials
4. Very cheap ($0.10 per 1000 emails)

### Step 2: Configure .env File

```bash
# Gmail Example
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-here
MAIL_DEFAULT_SENDER=noreply@mohiindustries.in

# SendGrid Example
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=noreply@mohiindustries.in

# AWS SES Example
MAIL_SERVER=email-smtp.us-east-1.amazonaws.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-aws-smtp-username
MAIL_PASSWORD=your-aws-smtp-password
MAIL_DEFAULT_SENDER=noreply@mohiindustries.in
```

### Step 3: Enable Notifications

```bash
# Email Notification Settings
SEND_PAYMENT_REMINDERS=true
SEND_LOW_STOCK_ALERTS=true
SEND_ORDER_CONFIRMATIONS=true
PAYMENT_REMINDER_DAYS=7
```

### Step 4: Restart Application

```bash
docker-compose restart
# or
flask run
```

### Step 5: Test Configuration

1. Login to ERP
2. Go to "Emails" menu
3. Click "Test Email Configuration"
4. Check your inbox!

---

## 📨 Email Types

### 1. Order Confirmation
**Sent:** When order is created  
**To:** Customer email  
**Contains:**
- Order number and date
- Total amount
- Payment status
- Delivery address
- Contact information

**Trigger:** Automatic on order creation (if enabled)

### 2. Payment Receipt
**Sent:** When payment is received  
**To:** Customer email  
**Contains:**
- Receipt number
- Payment date and amount
- Payment mode
- Order details
- Balance remaining

**Trigger:** Automatic on payment recording

### 3. Payment Reminder
**Sent:** For overdue payments  
**To:** Customer email  
**Contains:**
- Order details
- Days overdue
- Outstanding amount
- Payment methods
- Contact information

**Trigger:** Manual or bulk send

### 4. Low Stock Alert
**Sent:** When stock below reorder level  
**To:** Admin email  
**Contains:**
- Product details
- Current stock level
- Reorder level
- Recommended actions

**Trigger:** Manual or bulk send

### 5. Monthly Statement (Coming Soon)
**Sent:** End of month  
**To:** Customer email  
**Contains:**
- All orders for the month
- Total amount
- Payments received
- Outstanding balance

**Trigger:** Manual send

---

## 🎯 Usage

### Send Individual Emails

**Order Confirmation:**
```
1. Go to Orders → View Order
2. Click "Send Confirmation Email"
3. Email sent instantly
```

**Payment Receipt:**
```
1. Go to Payments → View Payment
2. Click "Send Receipt"
3. Email sent instantly
```

**Payment Reminder:**
```
1. Go to Orders → View Order
2. Click "Send Payment Reminder"
3. Email sent instantly
```

### Send Bulk Emails

**Bulk Payment Reminders:**
```
1. Go to Emails Dashboard
2. Click "Send Payment Reminders"
3. Confirms count
4. Sends to all overdue orders
```

**Bulk Low Stock Alerts:**
```
1. Go to Emails Dashboard
2. Click "Send Low Stock Alerts"
3. Confirms count
4. Sends alerts for all low stock items
```

---

## 🎨 Email Templates

All emails use professional HTML templates with:
- Company branding
- Responsive design (mobile-friendly)
- Color-coded sections
- Clear call-to-actions
- Contact information

### Customizing Templates

Templates located in: `app/templates/emails/`

**Available templates:**
- `order_confirmation.html`
- `payment_receipt.html`
- `payment_reminder.html`
- `low_stock_alert.html`
- `monthly_statement.html` (coming soon)

**To customize:**
1. Edit HTML template
2. Maintain structure
3. Test with sample data
4. Restart application

---

## ⚙️ Configuration Options

### Email Settings (.env)

```bash
# SMTP Configuration
MAIL_SERVER=smtp.gmail.com          # SMTP server address
MAIL_PORT=587                       # SMTP port (587 for TLS, 465 for SSL)
MAIL_USE_TLS=true                   # Use TLS encryption
MAIL_USERNAME=your-email@gmail.com  # SMTP username
MAIL_PASSWORD=your-password         # SMTP password
MAIL_DEFAULT_SENDER=noreply@...     # From email address

# Notification Toggles
SEND_ORDER_CONFIRMATIONS=true       # Auto-send order confirmations
SEND_PAYMENT_REMINDERS=true         # Enable payment reminders
SEND_LOW_STOCK_ALERTS=true          # Enable low stock alerts

# Timing
PAYMENT_REMINDER_DAYS=7             # Days after due date to send reminder
```

### Disable Specific Notifications

Set to `false` in .env:
```bash
SEND_ORDER_CONFIRMATIONS=false
SEND_PAYMENT_REMINDERS=false
SEND_LOW_STOCK_ALERTS=false
```

---

## 🔒 Security Best Practices

### 1. Use App Passwords (Gmail)
- Never use your main Gmail password
- Generate app-specific password
- Revoke if compromised

### 2. Protect .env File
```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Set proper permissions
chmod 600 .env
```

### 3. Use Dedicated Email
- Create separate email for ERP
- Don't use personal email
- Use professional domain

### 4. Monitor Usage
- Check sent email logs
- Watch for bounces
- Monitor spam reports

---

## 📊 Email Dashboard

Access: `/emails/dashboard`

**Features:**
- View email statistics
- Send bulk emails
- Test configuration
- Check notification settings
- View available templates

**Statistics Shown:**
- Overdue payments count
- Low stock items count
- Pending orders count
- Active customers with email

---

## 🐛 Troubleshooting

### Emails Not Sending?

**Check 1: Configuration**
```bash
# Verify .env settings
cat .env | grep MAIL

# Test configuration
Go to Emails → Test Email Configuration
```

**Check 2: SMTP Credentials**
```bash
# Gmail: Use app password, not regular password
# SendGrid: Use "apikey" as username
# AWS SES: Verify domain first
```

**Check 3: Firewall**
```bash
# Check if port 587 is open
telnet smtp.gmail.com 587

# Should connect successfully
```

**Check 4: Logs**
```bash
# Check application logs
docker-compose logs -f web

# Look for email errors
```

### Common Errors

**"Authentication failed"**
- Solution: Check username/password
- Gmail: Use app password
- SendGrid: Use API key

**"Connection refused"**
- Solution: Check MAIL_SERVER and MAIL_PORT
- Verify firewall settings

**"Sender not verified"**
- Solution: Verify sender email in email service
- AWS SES: Verify domain

**"Rate limit exceeded"**
- Solution: Upgrade email service plan
- Reduce sending frequency

---

## 📈 Best Practices

### 1. Email Timing
- Send order confirmations immediately
- Send payment reminders weekly
- Send low stock alerts daily
- Send monthly statements on 1st

### 2. Email Content
- Keep subject lines clear
- Use professional language
- Include contact information
- Add unsubscribe option (future)

### 3. Monitoring
- Track open rates
- Monitor bounce rates
- Check spam complaints
- Review customer feedback

### 4. Testing
- Test before bulk sending
- Verify email formatting
- Check mobile display
- Test all links

---

## 🔮 Future Enhancements

### Phase 3.1: Advanced Features
- Email scheduling
- Email templates editor
- Delivery tracking
- Open/click analytics
- Unsubscribe management

### Phase 3.2: More Templates
- Invoice attached emails
- Delivery notifications
- Birthday wishes
- Promotional emails
- Newsletter

### Phase 3.3: Automation
- Scheduled bulk sends
- Triggered workflows
- Drip campaigns
- Auto-follow-ups

---

## 💰 Cost Comparison

### Gmail (Free Tier)
- **Cost:** Free
- **Limit:** 500 emails/day
- **Best for:** Small businesses
- **Pros:** Easy setup, reliable
- **Cons:** Daily limit, not professional

### SendGrid (Free Tier)
- **Cost:** Free
- **Limit:** 100 emails/day
- **Best for:** Startups
- **Pros:** Professional, analytics
- **Cons:** Low free tier limit

### SendGrid (Paid)
- **Cost:** $15/month
- **Limit:** 40,000 emails/month
- **Best for:** Growing businesses
- **Pros:** High limit, support
- **Cons:** Monthly cost

### AWS SES
- **Cost:** $0.10 per 1000 emails
- **Limit:** Unlimited (with verification)
- **Best for:** Scale
- **Pros:** Cheapest, scalable
- **Cons:** Complex setup

**Recommendation:** Start with Gmail, move to SendGrid or AWS SES as you grow.

---

## 📞 Support

### Getting Help
1. Check this documentation
2. Test email configuration
3. Review error logs
4. Contact development team

### Reporting Issues
Include:
- Email service used
- Error message
- Configuration (hide passwords!)
- Logs

---

## ✅ Checklist

- [ ] Email service chosen
- [ ] SMTP credentials obtained
- [ ] .env file configured
- [ ] Application restarted
- [ ] Test email sent successfully
- [ ] Order confirmation tested
- [ ] Payment receipt tested
- [ ] Payment reminder tested
- [ ] Low stock alert tested
- [ ] Bulk sends tested
- [ ] Email dashboard accessible
- [ ] Users trained

---

**Ready to automate your communications! 📧**

For questions: Contact development team  
Last Updated: January 2026  
Version: 1.0.0
