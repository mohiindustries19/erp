# WhatsApp Integration - Complete Setup Guide
## Mohi Industries ERP

**Date:** January 28, 2026  
**Status:** Ready to Configure

---

## 📦 Files Created

✅ **Backend Service:**
- `app/services/whatsapp.py` - WhatsApp service with multi-provider support

✅ **Routes:**
- `app/routes/whatsapp.py` - Admin panel routes for sending messages

✅ **Templates:**
- `app/templates/whatsapp/dashboard.html` - WhatsApp dashboard

✅ **Configuration:**
- `docs/snippets/config_whatsapp.py` - Configuration template

✅ **Documentation:**
- `WHATSAPP_INTEGRATION_PLAN.md` - Complete integration plan
- `WHATSAPP_SETUP_GUIDE.md` - This file

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```cmd
cd D:\OtherRepos\mohierp\mohi-erp
.venv\Scripts\activate
pip install twilio requests python-dotenv
```

### Step 2: Configure WhatsApp

**Option A: Use Twilio (Easiest for Testing)**

1. Sign up at https://www.twilio.com/
2. Get your credentials from console
3. Add to `.env` file:

```env
# WhatsApp Configuration
WHATSAPP_ENABLED=True
WHATSAPP_PROVIDER=twilio

# Twilio Credentials
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
```

**Option B: Use Gupshup (Best for India)**

1. Sign up at https://www.gupshup.io/
2. Get API key
3. Add to `.env` file:

```env
# WhatsApp Configuration
WHATSAPP_ENABLED=True
WHATSAPP_PROVIDER=gupshup

# Gupshup Credentials
GUPSHUP_API_KEY=your_api_key_here
GUPSHUP_APP_NAME=MohiIndustries
```

### Step 3: Register Routes

Add to `app/__init__.py`:

```python
# Register WhatsApp routes
from app.routes import whatsapp
app.register_blueprint(whatsapp.bp)
```

---

## 📱 How to Use

### Access WhatsApp Dashboard

```
URL: http://localhost:5000/whatsapp
```

### Send Messages

**1. Product Availability (Morning Broadcast)**
- Go to WhatsApp → Send Product Availability
- Select distributors
- Click Send
- All selected distributors receive product list

**2. Payment Reminders**
- Go to WhatsApp → Send Payment Reminders
- System finds distributors with pending payments
- Click Send
- Reminders sent automatically

**3. Bulk Messages**
- Go to WhatsApp → Send Bulk Message
- Select distributors
- Type custom message
- Click Send

**4. Festival Offers**
- Go to WhatsApp → Send Festival Offer
- Fill offer details
- Select distributors
- Click Send

---

## 🔧 Integration with ERP

### Auto-Send Order Confirmation

Add to `app/routes/orders.py` after order creation:

```python
# After db.session.commit()
try:
    from app.services.whatsapp import send_order_confirmation
    send_order_confirmation(order)
except Exception as e:
    logger.error(f"WhatsApp error: {str(e)}")
```

### Auto-Send Invoice

Add to `app/routes/orders.py` in print_invoice route:

```python
@bp.route('/<int:id>/invoice')
@login_required
def print_invoice(id):
    order = Order.query.get_or_404(id)
    
    # Send via WhatsApp
    try:
        from app.services.whatsapp import send_invoice
        pdf_url = url_for('orders.print_invoice', id=order.id, _external=True)
        send_invoice(order, pdf_url)
    except Exception as e:
        logger.error(f"WhatsApp error: {str(e)}")
    
    return render_template('orders/invoice.html', order=order)
```

### Auto-Send Payment Reminder

Create scheduled task (cron job):

```python
# app/tasks/whatsapp_tasks.py

from app import create_app, db
from app.models import Order, Distributor
from app.services.whatsapp import send_payment_reminder
from datetime import date, timedelta

def send_daily_payment_reminders():
    """Send payment reminders for overdue invoices"""
    app = create_app()
    
    with app.app_context():
        # Find distributors with overdue payments
        today = date.today()
        
        pending_orders = db.session.query(
            Distributor,
            db.func.sum(Order.total_amount - Order.paid_amount).label('outstanding')
        ).join(Order).filter(
            Order.payment_status.in_(['pending', 'partial']),
            Order.order_date < today - timedelta(days=7)  # 7 days overdue
        ).group_by(Distributor.id).all()
        
        for distributor, outstanding in pending_orders:
            invoices = Order.query.filter(
                Order.distributor_id == distributor.id,
                Order.payment_status.in_(['pending', 'partial'])
            ).all()
            
            send_payment_reminder(distributor, outstanding, invoices)
            print(f"Reminder sent to {distributor.business_name}")

if __name__ == '__main__':
    send_daily_payment_reminders()
```

Run daily at 6 PM:
```cmd
python -m app.tasks.whatsapp_tasks
```

---

## 🎯 Message Templates

### Template 1: Order Confirmation
```
✅ Order Confirmed!

Order #: {order_number}
Date: {date}

Items: {item_count} products
Total: ₹{total_amount}

Payment: {payment_terms}
Status: {status}

Thank you! 🙏
📞 9262650010
Mohi Industries
```

### Template 2: Payment Reminder
```
💰 Payment Reminder

Dear {distributor_name},

Outstanding: ₹{outstanding_amount}

Pending Invoices:
• {invoice_1}
• {invoice_2}

Please pay at earliest.

Bank: SBI Hajipur
A/c: 1234567890
IFSC: SBIN0001234

📞 9262650010
```

### Template 3: Product Availability
```
🌅 Good Morning!

Fresh products available:

• Bread 400g - ₹45
• Bun - ₹15
• Cake - ₹50

Reply with your order!

📞 9262650010
Mohi Industries
```

### Template 4: Delivery Update
```
🚚 Out for Delivery!

Order #: {order_number}

Your order is on the way!
Expected: {delivery_time}

Thank you! 🙏
📞 9262650010
```

---

## 💡 Best Practices

### 1. Message Timing
- **Morning (6 AM):** Product availability
- **Afternoon (2 PM):** Delivery updates
- **Evening (6 PM):** Payment reminders
- **Avoid:** Late night messages

### 2. Message Frequency
- Max 5 messages per distributor per day
- Don't spam
- Provide opt-out option

### 3. Message Content
- Keep short and clear
- Use emojis for engagement
- Include call-to-action
- Always add contact number

### 4. Testing
- Test with your own number first
- Verify message delivery
- Check formatting
- Test all templates

---

## 🔍 Troubleshooting

### Error: "WhatsApp is disabled"
**Solution:** Set `WHATSAPP_ENABLED=True` in `.env`

### Error: "Unknown provider"
**Solution:** Check `WHATSAPP_PROVIDER` is set to 'twilio', 'gupshup', or 'interakt'

### Error: "Invalid credentials"
**Solution:** Verify API keys in `.env` file

### Messages not sending
**Solution:**
1. Check internet connection
2. Verify API credits/balance
3. Check phone number format
4. Review provider dashboard for errors

### Phone number format issues
**Solution:** Service auto-formats numbers:
- Removes spaces, dashes
- Adds +91 for India
- Example: 9262650010 → 919262650010

---

## 📊 Cost Estimation

### Twilio (International)
- Setup: Free
- Per message: $0.005 (₹0.40)
- Monthly (68 distributors × 5 msg/day × 30 days): ₹4,080

### Gupshup (India)
- Setup: Free
- Per message: ₹0.25-0.50
- Monthly (68 distributors × 5 msg/day × 30 days): ₹2,550-₹5,100

### Interakt (India)
- Setup: Free
- Monthly subscription: ₹5,000-₹10,000
- Unlimited messages included

**Recommendation:** Start with Twilio for testing, move to Gupshup/Interakt for production.

---

## 🎓 Training Your Team

### For Admin
1. Configure WhatsApp settings
2. Send test messages
3. Monitor delivery status
4. Manage templates

### For Sales Team
1. Send product availability
2. Send order confirmations
3. Track responses
4. Handle queries

### For Accounts Team
1. Send payment reminders
2. Track payments
3. Send receipts
4. Follow up on overdue

---

## 📈 Success Metrics

Track these KPIs:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Delivery Rate | >95% | Provider dashboard |
| Response Rate | >60% | Manual tracking |
| Order Conversion | >40% | Orders/Messages sent |
| Payment Collection | -30% time | Days to payment |
| Customer Satisfaction | +20% | Feedback surveys |

---

## 🔐 Security & Compliance

### Data Privacy
- ✅ Don't share customer data
- ✅ Secure API credentials in `.env`
- ✅ Don't log sensitive information
- ✅ Follow WhatsApp Business Policy

### WhatsApp Policy
- ✅ Only message opted-in customers
- ✅ Provide opt-out option
- ✅ Don't spam
- ✅ Use approved templates only
- ✅ Respond within 24 hours

### Opt-Out Message
Add to all messages:
```
Reply STOP to unsubscribe
```

---

## 🚀 Next Steps

### Week 1: Setup & Testing
- [ ] Install dependencies
- [ ] Configure provider
- [ ] Register routes
- [ ] Send test messages
- [ ] Verify delivery

### Week 2: Integration
- [ ] Add to order creation
- [ ] Add to invoice generation
- [ ] Add to payment recording
- [ ] Test workflows

### Week 3: Automation
- [ ] Set up daily product broadcast
- [ ] Set up payment reminders
- [ ] Create scheduled tasks
- [ ] Monitor performance

### Week 4: Optimization
- [ ] Analyze metrics
- [ ] Optimize message content
- [ ] Improve response handling
- [ ] Scale operations

---

## 📞 Support

**Need Help?**

1. Check provider documentation:
   - Twilio: https://www.twilio.com/docs/whatsapp
   - Gupshup: https://www.gupshup.io/developer/docs
   - Interakt: https://docs.interakt.shop/

2. Review error logs:
   ```cmd
   tail -f logs/app.log
   ```

3. Test with curl:
   ```cmd
   curl -X POST http://localhost:5000/whatsapp/test-message \
     -d "phone=919262650010"
   ```

---

## ✅ Checklist

**Before Going Live:**

- [ ] Dependencies installed
- [ ] Provider configured
- [ ] Routes registered
- [ ] Test messages sent successfully
- [ ] Templates approved (if using API)
- [ ] Team trained
- [ ] Backup plan ready
- [ ] Monitoring set up
- [ ] Compliance checked
- [ ] Budget approved

---

**🎉 You're Ready to Go!**

Your WhatsApp integration is complete and ready to use. Start with test messages, then gradually roll out to all distributors.

**Questions?** Review the integration plan or check provider documentation.

**Good luck with your WhatsApp business communication! 📱**
