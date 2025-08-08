"""
Billing API endpoints
"""
from flask import request, jsonify
from app.core.config import Config
import stripe
from . import api_bp

# Configure Stripe
stripe.api_key = Config.STRIPE_SECRET_KEY

@api_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session"""
    try:
        data = request.json
        tier = data['tier']
        
        if tier not in Config.PRICING_TIERS:
            return jsonify({'error': 'Invalid tier'}), 400
        
        tier_info = Config.PRICING_TIERS[tier]
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'OpenRouter AI Agents - {tier_info["name"]}',
                        'description': f'Monthly subscription to {tier_info["name"]} plan',
                    },
                    'unit_amount': tier_info['price'] * 100,
                    'recurring': {
                        'interval': 'month',
                    },
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.host_url + 'dashboard',
        )
        
        return jsonify({'id': checkout_session.id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400