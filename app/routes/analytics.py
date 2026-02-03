"""
Analytics Routes - Customer Analytics & Business Intelligence
"""
from flask import Blueprint, render_template, jsonify, send_file, request
from flask_login import login_required
from app.models import Order, Distributor, Product, Inventory, Payment, OrderItem, ProductCategory
from app import db
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import pandas as pd
import io

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Analytics Dashboard with Charts and Insights"""
    
    # Top 10 Customers by Revenue
    top_customers = db.session.query(
        Distributor.id,
        Distributor.business_name,
        Distributor.city,
        Distributor.state,
        func.sum(Order.total_amount).label('total_revenue'),
        func.count(Order.id).label('order_count')
    ).join(Order).filter(
        Order.status.in_(['confirmed', 'delivered', 'completed'])
    ).group_by(
        Distributor.id
    ).order_by(
        func.sum(Order.total_amount).desc()
    ).limit(10).all()
    
    # State-wise Sales Distribution
    state_sales = db.session.query(
        Distributor.state,
        func.sum(Order.total_amount).label('total_sales'),
        func.count(Order.id).label('order_count')
    ).join(Order).filter(
        Order.status.in_(['confirmed', 'delivered', 'completed'])
    ).group_by(
        Distributor.state
    ).order_by(
        func.sum(Order.total_amount).desc()
    ).all()
    
    # Monthly Sales Trend (Last 12 months)
    twelve_months_ago = datetime.now() - timedelta(days=365)
    monthly_sales = db.session.query(
        extract('year', Order.order_date).label('year'),
        extract('month', Order.order_date).label('month'),
        func.sum(Order.total_amount).label('total_sales'),
        func.count(Order.id).label('order_count')
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
    
    # Top 10 Products by Sales
    top_products = db.session.query(
        Product.id,
        Product.name,
        ProductCategory.name.label('category'),
        func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_sales')
    ).join(OrderItem, Product.id == OrderItem.product_id)\
     .join(Order, OrderItem.order_id == Order.id)\
     .join(ProductCategory, Product.category_id == ProductCategory.id)\
     .filter(
        Order.status.in_(['confirmed', 'delivered', 'completed'])
    ).group_by(
        Product.id, ProductCategory.name
    ).order_by(
        func.sum(OrderItem.quantity * OrderItem.unit_price).desc()
    ).limit(10).all()
    
    # Payment Collection Stats
    total_receivable = db.session.query(
        func.sum(Order.total_amount - Order.paid_amount)
    ).filter(
        Order.payment_status.in_(['pending', 'partial'])
    ).scalar() or 0
    
    total_collected = db.session.query(
        func.sum(Payment.amount)
    ).filter(
        Payment.status == 'cleared'
    ).scalar() or 0
    
    # Customer Satisfaction Average
    avg_satisfaction = db.session.query(
        func.avg(Distributor.customer_satisfaction_score)
    ).filter(
        Distributor.status == 'active'
    ).scalar() or 0
    
    # Total Loyalty Points
    total_loyalty_points = db.session.query(
        func.sum(Distributor.loyalty_points)
    ).filter(
        Distributor.status == 'active'
    ).scalar() or 0
    
    return render_template('analytics/dashboard.html',
                         top_customers=top_customers,
                         state_sales=state_sales,
                         monthly_sales=monthly_sales,
                         top_products=top_products,
                         total_receivable=total_receivable,
                         total_collected=total_collected,
                         avg_satisfaction=avg_satisfaction,
                         total_loyalty_points=total_loyalty_points)


@bp.route('/api/chart-data/<chart_type>')
@login_required
def chart_data(chart_type):
    """API endpoint for chart data"""
    
    if chart_type == 'monthly_sales':
        twelve_months_ago = datetime.now() - timedelta(days=365)
        data = db.session.query(
            extract('year', Order.order_date).label('year'),
            extract('month', Order.order_date).label('month'),
            func.sum(Order.total_amount).label('total_sales')
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
        
        labels = [f"{int(d.year)}-{int(d.month):02d}" for d in data]
        values = [float(d.total_sales) for d in data]
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    
    elif chart_type == 'state_sales':
        data = db.session.query(
            Distributor.state,
            func.sum(Order.total_amount).label('total_sales')
        ).join(Order).filter(
            Order.status.in_(['confirmed', 'delivered', 'completed'])
        ).group_by(
            Distributor.state
        ).order_by(
            func.sum(Order.total_amount).desc()
        ).limit(10).all()
        
        labels = [d.state for d in data]
        values = [float(d.total_sales) for d in data]
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    
    elif chart_type == 'top_products':
        data = db.session.query(
            Product.name,
            func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_sales')
        ).join(OrderItem, Product.id == OrderItem.product_id)\
         .join(Order, OrderItem.order_id == Order.id)\
         .filter(
            Order.status.in_(['confirmed', 'delivered', 'completed'])
        ).group_by(
            Product.id
        ).order_by(
            func.sum(OrderItem.quantity * OrderItem.unit_price).desc()
        ).limit(10).all()
        
        labels = [d.name for d in data]
        values = [float(d.total_sales) for d in data]
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    
    return jsonify({'error': 'Invalid chart type'}), 400


@bp.route('/export/<export_type>')
@login_required
def export_data(export_type):
    """Export data to CSV/Excel"""
    
    if export_type == 'customers':
        # Export all distributors
        distributors = Distributor.query.all()
        
        data = []
        for d in distributors:
            data.append({
                'Code': d.code,
                'Business Name': d.business_name,
                'Contact Person': d.contact_person,
                'Phone': d.phone,
                'Email': d.email,
                'City': d.city,
                'State': d.state,
                'GSTIN': d.gstin,
                'Status': d.status,
                'Credit Limit': d.credit_limit,
                'Total Orders': d.total_orders,
                'Total Revenue': d.total_revenue,
                'Outstanding': d.outstanding_amount,
                'Loyalty Points': d.loyalty_points,
                'Satisfaction Score': d.customer_satisfaction_score
            })
        
        df = pd.DataFrame(data)
        
    elif export_type == 'sales':
        # Export all orders
        orders = Order.query.order_by(Order.order_date.desc()).all()
        
        data = []
        for o in orders:
            data.append({
                'Order Number': o.order_number,
                'Date': o.order_date.strftime('%Y-%m-%d'),
                'Customer': o.distributor.business_name,
                'City': o.distributor.city,
                'State': o.distributor.state,
                'Total Amount': o.total_amount,
                'Paid Amount': o.paid_amount,
                'Outstanding': o.total_amount - o.paid_amount,
                'Payment Status': o.payment_status,
                'Order Status': o.status
            })
        
        df = pd.DataFrame(data)
        
    elif export_type == 'products':
        # Export all products
        products = Product.query.filter_by(is_active=True).all()
        
        data = []
        for p in products:
            inventory = Inventory.query.filter_by(product_id=p.id).first()
            data.append({
                'SKU': p.sku,
                'Name': p.name,
                'Category': p.category,
                'HSN Code': p.hsn_code,
                'MRP': p.mrp,
                'Distributor Price': p.distributor_price,
                'GST Rate': p.gst_rate,
                'Current Stock': inventory.current_stock if inventory else 0,
                'Status': 'Active' if p.is_active else 'Inactive'
            })
        
        df = pd.DataFrame(data)
        
    elif export_type == 'payments':
        # Export all payments
        payments = Payment.query.order_by(Payment.payment_date.desc()).all()
        
        data = []
        for p in payments:
            data.append({
                'Payment Number': p.payment_number,
                'Date': p.payment_date.strftime('%Y-%m-%d'),
                'Customer': p.order.distributor.business_name,
                'Order Number': p.order.order_number,
                'Amount': p.amount,
                'Mode': p.payment_mode,
                'Status': p.status,
                'Reference': p.reference_number or ''
            })
        
        df = pd.DataFrame(data)
        
    else:
        return "Invalid export type", 400
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    
    filename = f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )
