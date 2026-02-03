# Advanced Analytics Guide - ML-Powered Insights

## Overview
Phase 4 implementation adds machine learning capabilities to Mohi ERP for predictive analytics and intelligent decision-making.

## Features

### 1. Sales Forecasting
**URL:** `/advanced-analytics/sales-forecast`

Predict future sales using linear regression based on historical data.

**Features:**
- Forecast 3, 6, or 12 months ahead
- Trend analysis (increasing/decreasing)
- Model accuracy score
- Visual chart representation
- Confidence intervals

**Requirements:**
- Minimum 3 months of historical sales data
- Completed orders (confirmed/delivered/completed status)

**Use Cases:**
- Budget planning
- Inventory procurement planning
- Sales target setting
- Resource allocation

---

### 2. Customer Churn Prediction
**URL:** `/advanced-analytics/churn-prediction`

Identify customers at risk of stopping orders using behavioral analysis.

**Risk Scoring (0-100):**
- **High Risk (70-100):** Immediate action required
- **Medium Risk (40-69):** Monitor closely
- **Low Risk (0-39):** Healthy relationship

**Analysis Factors:**
- Days since last order
- Order frequency (orders per month)
- Average order value
- Payment behavior (% paid on time)

**Use Cases:**
- Customer retention campaigns
- Proactive relationship management
- Sales team prioritization
- Loyalty program targeting

---

### 3. Inventory Optimization
**URL:** `/advanced-analytics/inventory-optimization`

AI-powered recommendations for optimal stock levels.

**Status Categories:**
- **Critical:** Below reorder level - order immediately
- **Low:** Near reorder level - order soon
- **Optimal:** Healthy stock levels
- **Overstocked:** Excess inventory - reduce orders

**Recommendations Include:**
- Current stock vs reorder level
- Recommended order quantity
- Priority level (High/Medium/Low/Normal)
- Action items

**Use Cases:**
- Prevent stockouts
- Reduce excess inventory
- Optimize working capital
- Improve cash flow

---

### 4. Profit Analysis
**URL:** `/advanced-analytics/profit-analysis`

Comprehensive profitability insights by customer and time period.

**Metrics:**
- Total revenue and profit
- Profit margins
- Top 10 profitable customers
- Monthly profit trends
- Average order values

**Analysis:**
- Customer profitability ranking
- Revenue vs profit comparison
- Trend identification
- Performance tracking

**Use Cases:**
- Customer segmentation
- Pricing strategy
- Focus on high-value customers
- Performance monitoring

---

## Technical Details

### ML Libraries Used
- **scikit-learn:** Machine learning models
- **pandas:** Data manipulation
- **numpy:** Numerical computations
- **matplotlib/seaborn:** Visualizations (future)
- **prophet:** Time series forecasting (future)

### Models Implemented
1. **Linear Regression:** Sales forecasting
2. **Rule-Based Scoring:** Churn prediction
3. **Heuristic Analysis:** Inventory optimization
4. **Aggregation Analysis:** Profit analysis

### API Endpoints
```
GET /advanced-analytics/api/sales-forecast?months=3
GET /advanced-analytics/api/churn-prediction
GET /advanced-analytics/api/inventory-optimization
GET /advanced-analytics/api/profit-analysis
```

All endpoints return JSON:
```json
{
  "success": true,
  "data": { ... }
}
```

---

## Data Requirements

### Minimum Data for Accurate Predictions
- **Sales Forecast:** 3+ months of order history
- **Churn Prediction:** 5+ active customers with order history
- **Inventory Optimization:** Active products with inventory records
- **Profit Analysis:** Completed orders

### Data Quality Tips
1. Keep order statuses updated
2. Record accurate order dates
3. Maintain current inventory levels
4. Update payment statuses promptly
5. Regular data cleanup

---

## Best Practices

### 1. Regular Review
- Check ML analytics weekly
- Act on high-priority recommendations
- Track prediction accuracy
- Adjust strategies based on insights

### 2. Data Hygiene
- Clean historical data
- Remove test/dummy orders
- Verify customer information
- Update product details

### 3. Action Items
- Create alerts for critical inventory
- Schedule calls with high-risk customers
- Plan procurement based on forecasts
- Focus on profitable customers

### 4. Continuous Improvement
- More data = better predictions
- Track recommendation outcomes
- Provide feedback on accuracy
- Refine models over time

---

## Future Enhancements

### Planned Features
1. **Advanced Forecasting:** Prophet/ARIMA models
2. **Product Recommendations:** Collaborative filtering
3. **Price Optimization:** Dynamic pricing suggestions
4. **Demand Forecasting:** Product-level predictions
5. **Anomaly Detection:** Unusual pattern alerts
6. **Customer Segmentation:** RFM analysis
7. **Sentiment Analysis:** Customer feedback analysis

### Integration Plans
- Email alerts for critical predictions
- WhatsApp notifications for high-risk customers
- Automated reorder suggestions
- Dashboard widgets for quick insights

---

## Troubleshooting

### "Not enough historical data"
- Ensure you have minimum required data
- Check order date ranges
- Verify order statuses are correct

### "No active products found"
- Activate products in inventory
- Check product status flags
- Verify inventory records exist

### Inaccurate Predictions
- Review data quality
- Check for outliers/anomalies
- Ensure consistent data entry
- Allow more time for data accumulation

---

## Support

For issues or questions:
1. Check data requirements
2. Verify API responses
3. Review error messages
4. Contact system administrator

---

**Phase 4 Complete** ✅
ML-powered analytics now available in Mohi ERP!
