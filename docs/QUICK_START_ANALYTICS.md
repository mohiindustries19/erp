# Quick Start Guide - Analytics Features

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (1 minute)
```bash
cd mohierp/mohi-erp
pip install pandas openpyxl groq Flask-Mail
```

### Step 2: Run Database Migration (1 minute)
```bash
flask db migrate -m "Add analytics fields"
flask db upgrade
```

### Step 3: Update Analytics Data (1 minute)
```bash
python scripts/ops/update_analytics.py
```

### Step 4: Restart Application (1 minute)
```bash
# Docker
docker-compose restart

# Or direct
flask run
```

### Step 5: Access Analytics (1 minute)
1. Login to ERP
2. Click "Analytics" in menu
3. Explore dashboard!

---

## 📊 What You Get

### Analytics Dashboard
- 4 interactive charts
- Top 10 customers table
- State-wise sales breakdown
- Key metrics summary

### Export Features
- Export Customers (Excel)
- Export Sales (Excel)
- Export Products (Excel)
- Export Payments (Excel)

### Customer Insights
- Loyalty points
- Satisfaction scores
- Lifetime value
- Order frequency

---

## 🎯 Quick Actions

### View Top Customers
```
Navigate to: /analytics/dashboard
Scroll to: "Top 10 Customers by Revenue"
```

### Export Customer Data
```
Click: "Export Customers" button
File downloads: customers_YYYYMMDD_HHMMSS.xlsx
```

### Check Sales Trends
```
View: "Monthly Sales Trend" chart
Hover: See exact values
```

### Analyze State Performance
```
View: "Top States by Sales" chart
Check: State-wise sales table below
```

---

## 💡 Pro Tips

1. **Update Analytics Weekly**
   ```bash
   python scripts/ops/update_analytics.py
   ```

2. **Export Before Month-End**
   - Export sales data
   - Share with accounts team
   - Archive for records

3. **Monitor Top Customers**
   - Check weekly
   - Identify growth opportunities
   - Plan promotions

4. **Track Payment Collection**
   - View doughnut chart
   - Follow up on outstanding
   - Improve cash flow

---

## 🐛 Troubleshooting

**Charts not showing?**
```bash
# Check browser console
# Refresh page (Ctrl+F5)
# Clear browser cache
```

**Export fails?**
```bash
# Verify pandas installed
pip list | grep pandas

# Check database connection
flask shell
>>> from app import db
>>> db.engine.execute('SELECT 1').scalar()
```

**Migration errors?**
```bash
# Reset migrations
flask db stamp head
flask db migrate -m "Add analytics fields"
flask db upgrade
```

---

## 📞 Need Help?

1. Check `ANALYTICS_FEATURES.md` for detailed docs
2. Review `IMPLEMENTATION_SUMMARY.md` for overview
3. Contact development team

---

## ✅ Checklist

- [ ] Dependencies installed
- [ ] Migration completed
- [ ] Analytics data updated
- [ ] Application restarted
- [ ] Dashboard accessible
- [ ] Charts loading
- [ ] Exports working
- [ ] Data accurate

---

**Ready to go! Enjoy your new analytics features! 🎉**
