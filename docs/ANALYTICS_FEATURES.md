# Analytics Features - Mohi Industries ERP

## 🎯 New Features Added

### 1. **Analytics Dashboard** (`/analytics/dashboard`)
Professional analytics dashboard with interactive charts and insights.

**Features:**
- Monthly sales trend (line chart)
- State-wise sales distribution (bar chart)
- Top 10 products by revenue (horizontal bar chart)
- Payment collection status (doughnut chart)
- Top 10 customers by revenue (table)
- State-wise sales breakdown (table)

**Summary Cards:**
- Total Receivable (outstanding payments)
- Total Collected (cleared payments)
- Average Customer Satisfaction Score
- Total Loyalty Points

### 2. **CSV/Excel Export**
Export data to Excel format for external analysis.

**Available Exports:**
- `/analytics/export/customers` - All distributor data with analytics
- `/analytics/export/sales` - All orders with payment status
- `/analytics/export/products` - Product catalog with inventory
- `/analytics/export/payments` - Payment history

**Export Includes:**
- Customers: Code, Name, Contact, Location, Revenue, Orders, Loyalty Points, Satisfaction
- Sales: Order details, Customer info, Amounts, Payment status
- Products: SKU, Name, Category, Pricing, Stock levels
- Payments: Payment details, Customer, Order reference

### 3. **Customer Analytics Fields**
New fields added to Distributor model:

```python
loyalty_points              # Earned points (1 point per ₹1000 spent)
customer_satisfaction_score # Rating 1-10 (default: 5)
average_order_value        # Calculated from orders
total_lifetime_value       # Total revenue from customer
last_order_date           # Date of most recent order
order_frequency           # weekly/monthly/quarterly/yearly
```

**Calculated Properties:**
```python
distributor.total_orders      # Count of all orders
distributor.total_revenue     # Sum of completed orders
distributor.outstanding_amount # Pending payments
```

### 4. **Interactive Charts**
Using Chart.js for beautiful, responsive visualizations:
- Line charts for trends
- Bar charts for comparisons
- Doughnut charts for distributions
- Hover tooltips with detailed info
- Responsive design (mobile-friendly)

---

## 📦 Installation

### 1. Install New Dependencies
```bash
cd mohierp/mohi-erp
pip install -r requirements.txt
```

New packages added:
- `pandas` - Data manipulation and CSV export
- `openpyxl` - Excel file generation
- `groq` - AI chat (for future feature)
- `Flask-Mail` - Email notifications (for future feature)

### 2. Run Database Migration
```bash
# Generate migration
flask db migrate -m "Add analytics fields to distributors"

# Apply migration
flask db upgrade
```

### 3. Update Existing Data
```bash
# Populate analytics fields for existing distributors
python scripts/ops/update_analytics.py
```

---

## 🚀 Usage

### Access Analytics Dashboard
1. Login to ERP
2. Click "Analytics" in navigation menu
3. View charts and insights
4. Export data using buttons at top

### Export Data
Click export buttons:
- "Export Customers" - Download customer data
- "Export Sales" - Download sales data
- Or use direct URLs:
  - `/analytics/export/customers`
  - `/analytics/export/sales`
  - `/analytics/export/products`
  - `/analytics/export/payments`

### Update Analytics Data
Run periodically to refresh calculated fields:
```bash
python scripts/ops/update_analytics.py
```

Or add to cron job:
```bash
# Update analytics daily at 2 AM
0 2 * * * cd /path/to/mohi-erp && python scripts/ops/update_analytics.py
```

---

## 📊 Chart Data API

RESTful API endpoints for chart data:

```
GET /analytics/api/chart-data/monthly_sales
GET /analytics/api/chart-data/state_sales
GET /analytics/api/chart-data/top_products
```

Returns JSON:
```json
{
  "labels": ["2024-01", "2024-02", ...],
  "values": [150000, 180000, ...]
}
```

---

## 🎨 Customization

### Add New Charts
Edit `app/templates/analytics/dashboard.html`:

```html
<!-- Add canvas element -->
<canvas id="myNewChart" height="250"></canvas>

<!-- Add Chart.js script -->
<script>
const ctx = document.getElementById('myNewChart').getContext('2d');
new Chart(ctx, {
    type: 'bar', // or 'line', 'pie', 'doughnut'
    data: { ... },
    options: { ... }
});
</script>
```

### Add New Export Types
Edit `app/routes/analytics.py`:

```python
@bp.route('/export/<export_type>')
def export_data(export_type):
    if export_type == 'my_new_export':
        # Query data
        data = []
        # Create DataFrame
        df = pd.DataFrame(data)
        # Return Excel file
```

### Customize Analytics Fields
Edit `app/models/distributor.py` to add more fields:

```python
# Add new field
my_custom_metric = db.Column(db.Float, default=0.0)

# Add calculated property
@property
def my_calculated_value(self):
    return self.some_calculation()
```

---

## 🔮 Future Enhancements (Coming Soon)

### Phase 2: AI Chat Assistant
- Natural language queries
- "Show me top 5 customers this month"
- "Which products are low in stock?"
- Powered by Groq (Llama 3.1)

### Phase 3: Email Notifications
- Payment reminders
- Low stock alerts
- Order confirmations
- Monthly statements

### Phase 4: Advanced Analytics
- Predictive analytics (sales forecasting)
- Customer churn prediction
- Inventory optimization
- Profit margin analysis

---

## 📝 Notes

- Charts use Chart.js 4.4.0 (loaded from CDN)
- Excel files generated in-memory (no temp files)
- All monetary values in INR (₹)
- Date format: YYYY-MM-DD
- Analytics updated on-demand (run update script)

---

## 🐛 Troubleshooting

**Charts not loading?**
- Check browser console for errors
- Ensure Chart.js CDN is accessible
- Verify API endpoints return valid JSON

**Export fails?**
- Check pandas and openpyxl are installed
- Verify database connection
- Check file permissions

**Migration errors?**
- Backup database first
- Run `flask db stamp head` to reset
- Re-run migration commands

---

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review error logs
3. Contact development team

---

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Author:** Mohi Industries Development Team
