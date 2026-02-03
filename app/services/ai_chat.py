"""
AI Chat Service - Natural Language Query Interface
Uses Groq (Llama 3.1) for fast, free AI responses
"""
import os
from groq import Groq
from app.models import Distributor, Order, Product, Inventory, Payment
from app import db
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import json

class AIChat:
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key or api_key == 'your-groq-api-key-here':
            self.client = None
            self.enabled = False
        else:
            self.client = Groq(api_key=api_key)
            self.enabled = True
        
        # Updated to current model (llama-3.1-70b-versatile is decommissioned)
        self.model = "llama-3.3-70b-versatile"  # Latest Llama 3.3 model
    
    def get_context_data(self):
        """Get current ERP data for context"""
        try:
            # Get summary statistics
            total_distributors = Distributor.query.filter_by(status='active').count()
            total_products = Product.query.filter_by(is_active=True).count()
            total_orders = Order.query.count()
            
            # Get top 5 customers
            top_customers = db.session.query(
                Distributor.business_name,
                func.sum(Order.total_amount).label('revenue')
            ).join(Order).filter(
                Order.status.in_(['confirmed', 'delivered', 'completed'])
            ).group_by(Distributor.id).order_by(
                func.sum(Order.total_amount).desc()
            ).limit(5).all()
            
            # Get low stock products
            low_stock = db.session.query(
                Product.name,
                Inventory.quantity
            ).join(Inventory).filter(
                Inventory.quantity < Product.reorder_level
            ).limit(5).all()
            
            # Get pending payments
            pending_amount = db.session.query(
                func.sum(Order.total_amount - Order.paid_amount)
            ).filter(
                Order.payment_status.in_(['pending', 'partial'])
            ).scalar() or 0
            
            # Get this month's sales
            first_day = datetime.now().replace(day=1)
            monthly_sales = db.session.query(
                func.sum(Order.total_amount)
            ).filter(
                Order.order_date >= first_day,
                Order.status.in_(['confirmed', 'delivered', 'completed'])
            ).scalar() or 0
            
            context = {
                'total_distributors': total_distributors,
                'total_products': total_products,
                'total_orders': total_orders,
                'top_customers': [{'name': c.business_name, 'revenue': float(c.revenue)} for c in top_customers],
                'low_stock_products': [{'name': p.name, 'stock': p.quantity} for p in low_stock],
                'pending_payments': float(pending_amount),
                'monthly_sales': float(monthly_sales)
            }
            
            return context
        except Exception as e:
            print(f"Error getting context: {e}")
            return {}
    
    def execute_query(self, user_query):
        """Execute natural language query and return results"""
        
        if not self.enabled:
            return {
                'success': False,
                'message': 'AI Chat is not configured. Please add GROQ_API_KEY to .env file.',
                'data': None
            }
        
        try:
            # Get current context
            context = self.get_context_data()
            
            # Check if query needs specific data
            query_lower = user_query.lower()
            additional_data = {}
            
            # Get all customers if asked
            if any(word in query_lower for word in ['all customer', 'list customer', 'name customer', 'show customer', 'customer list', 'customer name', 'which customer', 'what customer', 'contact']):
                all_customers = Distributor.query.filter_by(status='active').all()
                additional_data['all_customers'] = [
                    {
                        'name': d.business_name,
                        'contact_person': d.contact_person,
                        'phone': d.phone,
                        'email': d.email,
                        'city': d.city,
                        'state': d.state,
                        'address': d.address,
                        'gstin': d.gstin
                    }
                    for d in all_customers
                ]
            
            # Get all products if asked
            if any(word in query_lower for word in ['all product', 'list product', 'show product', 'product list', 'product name', 'which product', 'what product']):
                all_products = Product.query.filter_by(is_active=True).all()
                additional_data['all_products'] = [
                    {
                        'name': p.name,
                        'sku': p.sku,
                        'category': p.category,
                        'price': float(p.price)
                    }
                    for p in all_products
                ]
            
            # Get all orders if asked
            if any(word in query_lower for word in ['all order', 'list order', 'show order', 'order list', 'which order', 'what order']):
                recent_orders = Order.query.order_by(Order.order_date.desc()).limit(20).all()
                additional_data['recent_orders'] = [
                    {
                        'order_number': o.order_number,
                        'customer': o.distributor.business_name,
                        'amount': float(o.total_amount),
                        'status': o.status,
                        'date': o.order_date.strftime('%Y-%m-%d')
                    }
                    for o in recent_orders
                ]
            
            # Create system prompt with ERP context
            system_prompt = f"""You are an AI assistant for Mohi Industries ERP system. 
You help users query their business data using natural language.

Current ERP Data:
- Total Active Distributors: {context.get('total_distributors', 0)}
- Total Products: {context.get('total_products', 0)}
- Total Orders: {context.get('total_orders', 0)}
- This Month's Sales: ₹{context.get('monthly_sales', 0):,.2f}
- Pending Payments: ₹{context.get('pending_payments', 0):,.2f}

Top 5 Customers by Revenue:
{json.dumps(context.get('top_customers', []), indent=2)}

Low Stock Products:
{json.dumps(context.get('low_stock_products', []), indent=2)}"""

            # Add additional data if available
            if additional_data:
                system_prompt += f"\n\nAdditional Data:\n{json.dumps(additional_data, indent=2)}"

            system_prompt += """

When answering:
1. Be concise and specific
2. Use Indian Rupees (₹) for amounts
3. Format numbers with commas (e.g., ₹1,50,000)
4. When user asks for a list or contacts, provide ALL details in a formatted list
5. Don't just say "we have X items" - actually list them with full details
6. Provide actionable insights when possible
7. Use bullet points for lists with complete information
8. Be professional but friendly
9. If asked for contacts, show: name, contact person, phone, email, location

Answer the user's question based on the data provided above."""

            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            
            return {
                'success': True,
                'message': answer,
                'data': {**context, **additional_data}
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error processing query: {str(e)}',
                'data': None
            }
    
    def get_specific_data(self, query_type, params=None):
        """Get specific data based on query type"""
        
        try:
            if query_type == 'top_customers':
                limit = params.get('limit', 10) if params else 10
                customers = db.session.query(
                    Distributor.business_name,
                    Distributor.city,
                    Distributor.state,
                    func.sum(Order.total_amount).label('revenue'),
                    func.count(Order.id).label('orders')
                ).join(Order).filter(
                    Order.status.in_(['confirmed', 'delivered', 'completed'])
                ).group_by(Distributor.id).order_by(
                    func.sum(Order.total_amount).desc()
                ).limit(limit).all()
                
                return [
                    {
                        'name': c.business_name,
                        'location': f"{c.city}, {c.state}",
                        'revenue': float(c.revenue),
                        'orders': c.orders
                    }
                    for c in customers
                ]
            
            elif query_type == 'low_stock':
                products = db.session.query(
                    Product.name,
                    Product.sku,
                    Inventory.quantity,
                    Product.reorder_level
                ).join(Inventory).filter(
                    Inventory.quantity < Product.reorder_level
                ).all()
                
                return [
                    {
                        'name': p.name,
                        'sku': p.sku,
                        'current_stock': p.quantity,
                        'reorder_level': p.reorder_level
                    }
                    for p in products
                ]
            
            elif query_type == 'pending_payments':
                orders = Order.query.filter(
                    Order.payment_status.in_(['pending', 'partial'])
                ).order_by(Order.order_date.desc()).limit(20).all()
                
                return [
                    {
                        'order_number': o.order_number,
                        'customer': o.distributor.business_name,
                        'total': float(o.total_amount),
                        'paid': float(o.paid_amount),
                        'outstanding': float(o.total_amount - o.paid_amount),
                        'date': o.order_date.strftime('%Y-%m-%d')
                    }
                    for o in orders
                ]
            
            elif query_type == 'monthly_sales':
                months = params.get('months', 6) if params else 6
                start_date = datetime.now() - timedelta(days=months*30)
                
                sales = db.session.query(
                    extract('year', Order.order_date).label('year'),
                    extract('month', Order.order_date).label('month'),
                    func.sum(Order.total_amount).label('total')
                ).filter(
                    Order.order_date >= start_date,
                    Order.status.in_(['confirmed', 'delivered', 'completed'])
                ).group_by(
                    extract('year', Order.order_date),
                    extract('month', Order.order_date)
                ).order_by(
                    extract('year', Order.order_date),
                    extract('month', Order.order_date)
                ).all()
                
                return [
                    {
                        'month': f"{int(s.year)}-{int(s.month):02d}",
                        'sales': float(s.total)
                    }
                    for s in sales
                ]
            
            elif query_type == 'top_products':
                limit = params.get('limit', 10) if params else 10
                products = db.session.query(
                    Product.name,
                    Product.category,
                    func.sum(Order.total_amount).label('sales')
                ).join(Order).filter(
                    Order.status.in_(['confirmed', 'delivered', 'completed'])
                ).group_by(Product.id).order_by(
                    func.sum(Order.total_amount).desc()
                ).limit(limit).all()
                
                return [
                    {
                        'name': p.name,
                        'category': p.category,
                        'sales': float(p.sales)
                    }
                    for p in products
                ]
            
            else:
                return None
                
        except Exception as e:
            print(f"Error getting specific data: {e}")
            return None
