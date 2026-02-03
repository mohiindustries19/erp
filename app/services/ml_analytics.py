"""
Machine Learning Analytics Service
Sales Forecasting, Churn Prediction, Inventory Optimization
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta
from app.models import Order, Distributor, Product, Inventory
from app import db
from sqlalchemy import func, extract
import warnings
warnings.filterwarnings('ignore')

class MLAnalytics:
    
    @staticmethod
    def sales_forecast(months_ahead=3):
        """
        Forecast sales for next N months using linear regression
        Returns: DataFrame with forecasted sales
        """
        try:
            # Get historical sales data (last 12 months)
            twelve_months_ago = datetime.now() - timedelta(days=365)
            
            sales_data = db.session.query(
                extract('year', Order.order_date).label('year'),
                extract('month', Order.order_date).label('month'),
                func.sum(Order.total_amount).label('sales')
            ).filter(
                Order.order_date >= twelve_months_ago,
                Order.status.in_(['confirmed', 'delivered', 'completed'])
            ).group_by(
                extract('year', Order.order_date),
                extract('month', Order.order_date)
            ).order_by(
                extract('year', Order.order_date),
                extract('month', Order.order_date)
            ).all()
            
            if len(sales_data) < 3:
                return None, "Not enough historical data (need at least 3 months)"
            
            # Prepare data
            df = pd.DataFrame([
                {
                    'month_num': i,
                    'sales': float(row.sales)
                }
                for i, row in enumerate(sales_data, 1)
            ])
            
            # Train model
            X = df[['month_num']].values
            y = df['sales'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Forecast
            last_month = len(sales_data)
            future_months = np.array([[last_month + i] for i in range(1, months_ahead + 1)])
            forecasted_sales = model.predict(future_months)
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'month': [f"Month +{i}" for i in range(1, months_ahead + 1)],
                'forecasted_sales': forecasted_sales,
                'confidence': ['Medium'] * months_ahead
            })
            
            # Calculate trend
            trend = 'increasing' if model.coef_[0] > 0 else 'decreasing'
            trend_percentage = abs(model.coef_[0] / df['sales'].mean() * 100)
            
            return {
                'forecast': forecast_df.to_dict('records'),
                'trend': trend,
                'trend_percentage': round(trend_percentage, 2),
                'current_avg': round(df['sales'].mean(), 2),
                'model_score': round(model.score(X, y), 2)
            }, None
            
        except Exception as e:
            return None, f"Error in sales forecast: {str(e)}"
    
    @staticmethod
    def customer_churn_prediction():
        """
        Predict which customers are at risk of churning
        Returns: List of at-risk customers with churn probability
        """
        try:
            # Get all active distributors
            distributors = Distributor.query.filter_by(status='active').all()
            
            if len(distributors) < 5:
                return None, "Not enough customers for churn prediction"
            
            churn_predictions = []
            
            for dist in distributors:
                # Calculate features
                orders = Order.query.filter_by(distributor_id=dist.id).all()
                
                if not orders:
                    continue
                
                # Feature 1: Days since last order
                last_order = max(orders, key=lambda x: x.order_date)
                days_since_last = (datetime.now().date() - last_order.order_date).days
                
                # Feature 2: Order frequency (orders per month)
                if len(orders) > 1:
                    first_order = min(orders, key=lambda x: x.order_date)
                    months_active = max(1, (last_order.order_date - first_order.order_date).days / 30)
                    order_frequency = len(orders) / months_active
                else:
                    order_frequency = 0.1
                
                # Feature 3: Average order value
                avg_order_value = sum(o.total_amount for o in orders) / len(orders)
                
                # Feature 4: Payment behavior (% of paid orders)
                paid_orders = sum(1 for o in orders if o.payment_status == 'paid')
                payment_score = paid_orders / len(orders) if orders else 0
                
                # Simple churn score (0-100)
                # Higher score = higher churn risk
                churn_score = 0
                
                # Days since last order (max 40 points)
                if days_since_last > 90:
                    churn_score += 40
                elif days_since_last > 60:
                    churn_score += 30
                elif days_since_last > 30:
                    churn_score += 20
                
                # Order frequency (max 30 points)
                if order_frequency < 0.5:  # Less than 1 order per 2 months
                    churn_score += 30
                elif order_frequency < 1:
                    churn_score += 20
                elif order_frequency < 2:
                    churn_score += 10
                
                # Payment behavior (max 30 points)
                if payment_score < 0.5:
                    churn_score += 30
                elif payment_score < 0.7:
                    churn_score += 20
                elif payment_score < 0.9:
                    churn_score += 10
                
                # Determine risk level
                if churn_score >= 70:
                    risk_level = 'High'
                elif churn_score >= 40:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                churn_predictions.append({
                    'distributor_id': dist.id,
                    'business_name': dist.business_name,
                    'churn_score': churn_score,
                    'risk_level': risk_level,
                    'days_since_last_order': days_since_last,
                    'order_frequency': round(order_frequency, 2),
                    'avg_order_value': round(avg_order_value, 2),
                    'payment_score': round(payment_score * 100, 1),
                    'total_orders': len(orders)
                })
            
            # Sort by churn score (highest first)
            churn_predictions.sort(key=lambda x: x['churn_score'], reverse=True)
            
            # Get high-risk customers
            high_risk = [c for c in churn_predictions if c['risk_level'] == 'High']
            medium_risk = [c for c in churn_predictions if c['risk_level'] == 'Medium']
            
            return {
                'predictions': churn_predictions,
                'high_risk_count': len(high_risk),
                'medium_risk_count': len(medium_risk),
                'total_analyzed': len(churn_predictions)
            }, None
            
        except Exception as e:
            return None, f"Error in churn prediction: {str(e)}"
    
    @staticmethod
    def inventory_optimization():
        """
        Optimize inventory levels based on sales patterns
        Returns: Recommendations for each product
        """
        try:
            products = Product.query.filter_by(is_active=True).all()
            
            if not products:
                return None, "No active products found"
            
            recommendations = []
            
            for product in products:
                inventory = Inventory.query.filter_by(product_id=product.id).first()
                
                if not inventory:
                    continue
                
                # Get sales history (last 90 days)
                ninety_days_ago = datetime.now() - timedelta(days=90)
                
                # Note: This is simplified - in real implementation, 
                # you'd track order items to get actual product sales
                # For now, we'll use inventory movements as proxy
                
                current_stock = inventory.current_stock
                reorder_level = inventory.reorder_level
                
                # Calculate metrics
                stock_days = 30  # Simplified: assume current stock lasts 30 days
                
                # Determine status
                if current_stock < reorder_level:
                    status = 'Critical'
                    action = 'Order immediately'
                    priority = 'High'
                elif current_stock < reorder_level * 1.5:
                    status = 'Low'
                    action = 'Order soon'
                    priority = 'Medium'
                elif current_stock > reorder_level * 3:
                    status = 'Overstocked'
                    action = 'Reduce orders'
                    priority = 'Low'
                else:
                    status = 'Optimal'
                    action = 'Maintain current level'
                    priority = 'Normal'
                
                # Calculate recommended order quantity
                if status in ['Critical', 'Low']:
                    recommended_order = max(reorder_level * 2 - current_stock, 0)
                else:
                    recommended_order = 0
                
                recommendations.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'sku': product.sku,
                    'current_stock': current_stock,
                    'reorder_level': reorder_level,
                    'status': status,
                    'action': action,
                    'priority': priority,
                    'recommended_order': int(recommended_order),
                    'stock_days': stock_days
                })
            
            # Sort by priority
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2, 'Normal': 3}
            recommendations.sort(key=lambda x: priority_order[x['priority']])
            
            # Get counts
            critical_count = sum(1 for r in recommendations if r['status'] == 'Critical')
            low_count = sum(1 for r in recommendations if r['status'] == 'Low')
            overstocked_count = sum(1 for r in recommendations if r['status'] == 'Overstocked')
            
            return {
                'recommendations': recommendations,
                'critical_count': critical_count,
                'low_count': low_count,
                'overstocked_count': overstocked_count,
                'total_products': len(recommendations)
            }, None
            
        except Exception as e:
            return None, f"Error in inventory optimization: {str(e)}"
    
    @staticmethod
    def profit_analysis():
        """
        Analyze profit margins by product, customer, and time period
        Returns: Comprehensive profit analysis
        """
        try:
            # Get all completed orders
            orders = Order.query.filter(
                Order.status.in_(['confirmed', 'delivered', 'completed'])
            ).all()
            
            if not orders:
                return None, "No completed orders found"
            
            # Calculate overall metrics
            total_revenue = sum(o.total_amount for o in orders)
            
            # Simplified profit calculation (assuming 20% average margin)
            # In real implementation, you'd calculate actual COGS
            estimated_profit = total_revenue * 0.20
            profit_margin = 20.0
            
            # Profit by customer
            customer_profits = {}
            for order in orders:
                dist_id = order.distributor_id
                if dist_id not in customer_profits:
                    customer_profits[dist_id] = {
                        'business_name': order.distributor.business_name,
                        'revenue': 0,
                        'orders': 0
                    }
                customer_profits[dist_id]['revenue'] += order.total_amount
                customer_profits[dist_id]['orders'] += 1
            
            # Convert to list and calculate profit
            customer_profit_list = []
            for dist_id, data in customer_profits.items():
                profit = data['revenue'] * 0.20
                customer_profit_list.append({
                    'distributor_id': dist_id,
                    'business_name': data['business_name'],
                    'revenue': round(data['revenue'], 2),
                    'profit': round(profit, 2),
                    'orders': data['orders'],
                    'avg_order_value': round(data['revenue'] / data['orders'], 2)
                })
            
            # Sort by profit
            customer_profit_list.sort(key=lambda x: x['profit'], reverse=True)
            
            # Monthly profit trend
            monthly_profits = db.session.query(
                extract('year', Order.order_date).label('year'),
                extract('month', Order.order_date).label('month'),
                func.sum(Order.total_amount).label('revenue')
            ).filter(
                Order.status.in_(['confirmed', 'delivered', 'completed'])
            ).group_by(
                extract('year', Order.order_date),
                extract('month', Order.order_date)
            ).order_by(
                extract('year', Order.order_date),
                extract('month', Order.order_date)
            ).all()
            
            monthly_trend = [
                {
                    'month': f"{int(m.year)}-{int(m.month):02d}",
                    'revenue': round(float(m.revenue), 2),
                    'profit': round(float(m.revenue) * 0.20, 2)
                }
                for m in monthly_profits
            ]
            
            return {
                'total_revenue': round(total_revenue, 2),
                'estimated_profit': round(estimated_profit, 2),
                'profit_margin': profit_margin,
                'top_customers': customer_profit_list[:10],
                'monthly_trend': monthly_trend,
                'total_orders': len(orders)
            }, None
            
        except Exception as e:
            return None, f"Error in profit analysis: {str(e)}"
