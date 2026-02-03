# Quick Start - ML Analytics

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd mohierp/mohi-erp
pip install -r requirements.txt
```

### Step 2: Access ML Analytics
Open your browser and navigate to:
```
http://localhost:5000/advanced-analytics/dashboard
```

### Step 3: Explore Features
Click on any of the 4 analytics modules:
1. **Sales Forecasting** - Predict future sales
2. **Churn Prediction** - Identify at-risk customers
3. **Inventory Optimization** - Get stock recommendations
4. **Profit Analysis** - Analyze profitability

---

## 📊 Quick Feature Guide

### Sales Forecasting
**URL:** `/advanced-analytics/sales-forecast`

**What it does:**
- Predicts sales for next 3-12 months
- Shows trend (increasing/decreasing)
- Displays model accuracy

**How to use:**
1. Select forecast period (3, 6, or 12 months)
2. Click "Generate Forecast"
3. View chart and detailed table

**Requirements:**
- Minimum 3 months of historical sales data

---

### Customer Churn Prediction
**URL:** `/advanced-analytics/churn-prediction`

**What it does:**
- Identifies customers at risk of leaving
- Scores risk from 0-100
- Categorizes as High/Medium/Low risk

**How to use:**
1. Page loads automatically with predictions
2. Filter by risk level (All/High/Medium/Low)
3. Review customer details and take action

**Risk Levels:**
- **High (70-100):** Contact immediately
- **Medium (40-69):** Monitor closely
- **Low (0-39):** Healthy relationship

---

### Inventory Optimization
**URL:** `/advanced-analytics/inventory-optimization`

**What it does:**
- Analyzes current stock levels
- Recommends reorder quantities
- Prioritizes actions

**How to use:**
1. Page loads with all product recommendations
2. Filter by status (Critical/Low/Overstocked/Optimal)
3. Follow recommended actions

**Status Meanings:**
- **Critical:** Order immediately
- **Low:** Order soon
- **Overstocked:** Reduce orders
- **Optimal:** Maintain current level

---

### Profit Analysis
**URL:** `/advanced-analytics/profit-analysis`

**What it does:**
- Shows total revenue and profit
- Ranks top 10 profitable customers
- Displays monthly profit trends

**How to use:**
1. Page loads with complete analysis
2. View summary cards at top
3. Check monthly trend chart
4. Review top customers table

**Insights:**
- Focus on high-profit customers
- Identify profit trends
- Optimize pricing strategies

---

## 🎯 Common Use Cases

### 1. Planning Next Quarter
```
1. Go to Sales Forecast
2. Select 3 months
3. Use predictions for budget planning
4. Share with management
```

### 2. Customer Retention
```
1. Go to Churn Prediction
2. Filter "High Risk"
3. Export list
4. Schedule calls with sales team
```

### 3. Inventory Planning
```
1. Go to Inventory Optimization
2. Filter "Critical"
3. Place orders for recommended quantities
4. Monitor "Low" status items
```

### 4. Customer Prioritization
```
1. Go to Profit Analysis
2. Review top 10 customers
3. Allocate resources accordingly
4. Focus on high-value relationships
```

---

## 💡 Pro Tips

### Get Better Predictions
1. **More data = better accuracy**
   - Keep at least 6 months of history
   - Update orders regularly
   - Maintain clean data

2. **Regular reviews**
   - Check ML analytics weekly
   - Act on recommendations promptly
   - Track prediction accuracy

3. **Data quality**
   - Update order statuses
   - Record accurate dates
   - Keep inventory current
   - Update payment information

### Maximize Value
1. **Sales Forecast**
   - Use for procurement planning
   - Set realistic targets
   - Allocate resources

2. **Churn Prediction**
   - Create retention campaigns
   - Prioritize high-risk customers
   - Track success rate

3. **Inventory Optimization**
   - Prevent stockouts
   - Reduce excess inventory
   - Improve cash flow

4. **Profit Analysis**
   - Focus on profitable customers
   - Optimize pricing
   - Identify trends

---

## 🔧 Troubleshooting

### "Not enough historical data"
**Solution:** Ensure you have:
- At least 3 months of completed orders
- Orders with proper dates
- Correct order statuses

### "No active products found"
**Solution:** 
- Activate products in inventory
- Check product status flags
- Verify inventory records exist

### Charts not loading
**Solution:**
- Check browser console for errors
- Ensure Chart.js is loading
- Refresh the page
- Clear browser cache

### Predictions seem inaccurate
**Solution:**
- Review data quality
- Check for outliers
- Ensure consistent data entry
- Allow more time for data accumulation

---

## 📱 Quick Access Links

### Main Dashboard
```
http://localhost:5000/advanced-analytics/dashboard
```

### Individual Features
```
Sales Forecast:
http://localhost:5000/advanced-analytics/sales-forecast

Churn Prediction:
http://localhost:5000/advanced-analytics/churn-prediction

Inventory Optimization:
http://localhost:5000/advanced-analytics/inventory-optimization

Profit Analysis:
http://localhost:5000/advanced-analytics/profit-analysis
```

### API Endpoints (for developers)
```
GET /advanced-analytics/api/sales-forecast?months=3
GET /advanced-analytics/api/churn-prediction
GET /advanced-analytics/api/inventory-optimization
GET /advanced-analytics/api/profit-analysis
```

---

## 📚 Learn More

For detailed information, see:
- `ADVANCED_ANALYTICS_GUIDE.md` - Complete feature guide
- `PHASE4_COMPLETE.md` - Implementation details
- `IMPLEMENTATION_STATUS.md` - Overall project status

---

## 🎉 You're Ready!

ML Analytics is now part of your daily workflow. Start with:
1. Check Sales Forecast for planning
2. Review Churn Prediction for retention
3. Monitor Inventory Optimization for stock
4. Analyze Profit for customer focus

**Happy Analyzing!** 📊🚀

---

**Quick Start Guide**
**Version:** 1.0.0
**Last Updated:** January 26, 2026
