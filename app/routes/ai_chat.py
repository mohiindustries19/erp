"""
AI Chat Routes - Natural Language Query Interface
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.ai_chat import AIChat

bp = Blueprint('ai_chat', __name__, url_prefix='/ai')

@bp.route('/chat')
@login_required
def chat_page():
    """AI Chat interface page"""
    ai = AIChat()
    return render_template('ai/chat.html', ai_enabled=ai.enabled)


@bp.route('/api/query', methods=['POST'])
@login_required
def query():
    """Process natural language query"""
    data = request.get_json()
    user_query = data.get('query', '').strip()
    
    if not user_query:
        return jsonify({
            'success': False,
            'message': 'Please enter a question'
        }), 400
    
    ai = AIChat()
    result = ai.execute_query(user_query)
    
    return jsonify(result)


@bp.route('/api/data/<query_type>')
@login_required
def get_data(query_type):
    """Get specific data for charts/tables"""
    params = request.args.to_dict()
    
    ai = AIChat()
    data = ai.get_specific_data(query_type, params)
    
    if data is not None:
        return jsonify({
            'success': True,
            'data': data
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid query type'
        }), 400


@bp.route('/api/suggestions')
@login_required
def suggestions():
    """Get query suggestions"""
    suggestions = [
        "Show me top 5 customers by revenue",
        "Which products are low in stock?",
        "What's my total pending payments?",
        "Show monthly sales for last 6 months",
        "List top 10 selling products",
        "What's my revenue this month?",
        "Show me customers from Maharashtra",
        "Which orders are pending payment?",
        "What's my profit margin?",
        "Show me overdue invoices"
    ]
    
    return jsonify({
        'success': True,
        'suggestions': suggestions
    })
