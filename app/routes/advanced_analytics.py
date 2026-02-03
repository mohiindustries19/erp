"""
Advanced Analytics Routes - ML-Powered Insights
"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from app.services.ml_analytics import MLAnalytics

bp = Blueprint('advanced_analytics', __name__, url_prefix='/advanced-analytics')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Advanced analytics dashboard"""
    return render_template('advanced_analytics/dashboard.html')


@bp.route('/api/sales-forecast')
@login_required
def sales_forecast():
    """Get sales forecast for next N months"""
    months = request.args.get('months', 3, type=int)
    
    result, error = MLAnalytics.sales_forecast(months_ahead=months)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': result
    })


@bp.route('/api/churn-prediction')
@login_required
def churn_prediction():
    """Get customer churn predictions"""
    result, error = MLAnalytics.customer_churn_prediction()
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': result
    })


@bp.route('/api/inventory-optimization')
@login_required
def inventory_optimization():
    """Get inventory optimization recommendations"""
    result, error = MLAnalytics.inventory_optimization()
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': result
    })


@bp.route('/api/profit-analysis')
@login_required
def profit_analysis():
    """Get comprehensive profit analysis"""
    result, error = MLAnalytics.profit_analysis()
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'data': result
    })


@bp.route('/sales-forecast')
@login_required
def sales_forecast_page():
    """Sales forecast page"""
    return render_template('advanced_analytics/sales_forecast.html')


@bp.route('/churn-prediction')
@login_required
def churn_prediction_page():
    """Customer churn prediction page"""
    return render_template('advanced_analytics/churn_prediction.html')


@bp.route('/inventory-optimization')
@login_required
def inventory_optimization_page():
    """Inventory optimization page"""
    return render_template('advanced_analytics/inventory_optimization.html')


@bp.route('/profit-analysis')
@login_required
def profit_analysis_page():
    """Profit analysis page"""
    return render_template('advanced_analytics/profit_analysis.html')
