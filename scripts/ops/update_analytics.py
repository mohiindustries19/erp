"""
Update Analytics Data for Existing Distributors
Run this script after migration to populate analytics fields
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models import Distributor, Order
from sqlalchemy import func
from datetime import datetime

app = create_app()

def update_distributor_analytics():
    """Update analytics fields for all distributors"""
    with app.app_context():
        distributors = Distributor.query.all()
        
        print(f"Updating analytics for {len(distributors)} distributors...")
        
        for dist in distributors:
            # Get all completed orders
            orders = Order.query.filter_by(distributor_id=dist.id)\
                .filter(Order.status.in_(['confirmed', 'delivered', 'completed']))\
                .all()
            
            if orders:
                # Calculate total lifetime value
                total_value = sum(order.total_amount for order in orders)
                dist.total_lifetime_value = total_value
                
                # Calculate average order value
                dist.average_order_value = total_value / len(orders)
                
                # Get last order date
                last_order = max(orders, key=lambda x: x.order_date)
                dist.last_order_date = last_order.order_date
                
                # Calculate order frequency
                if len(orders) > 1:
                    first_order = min(orders, key=lambda x: x.order_date)
                    days_diff = (last_order.order_date - first_order.order_date).days
                    avg_days_between_orders = days_diff / (len(orders) - 1)
                    
                    if avg_days_between_orders <= 7:
                        dist.order_frequency = 'weekly'
                    elif avg_days_between_orders <= 30:
                        dist.order_frequency = 'monthly'
                    elif avg_days_between_orders <= 90:
                        dist.order_frequency = 'quarterly'
                    else:
                        dist.order_frequency = 'yearly'
                
                # Calculate loyalty points (1 point per ₹1000 spent)
                dist.loyalty_points = int(total_value / 1000)
                
                print(f"Updated {dist.business_name}: ₹{total_value:.2f} revenue, {len(orders)} orders")
            else:
                print(f"- Skipped {dist.business_name}: No orders")
        
        db.session.commit()
        print(f"\nAnalytics updated successfully for {len(distributors)} distributors.")

if __name__ == '__main__':
    update_distributor_analytics()
