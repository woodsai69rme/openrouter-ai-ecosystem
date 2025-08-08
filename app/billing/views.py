"""
Billing and upgrade views
"""
from flask import render_template_string, session, redirect, url_for
from app.core.config import Config
from . import billing_bp

@billing_bp.route('/upgrade/<tier>')
def upgrade(tier):
    """Upgrade page with Stripe integration"""
    if tier not in Config.PRICING_TIERS:
        return redirect('/')
    
    tier_info = Config.PRICING_TIERS[tier]
    
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Upgrade to {{ tier_info.name }}</title>
    <script src="https://js.stripe.com/v3/"></script>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .plan-card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); text-align: center; }
        .price { font-size: 3rem; color: #667eea; margin: 20px 0; }
        .features { text-align: left; max-width: 400px; margin: 20px auto; }
        .btn { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 1.1rem; }
        .btn:hover { background: #5a6fd8; }
    </style>
</head>
<body>
    <div class="plan-card">
        <h1>Upgrade to {{ tier_info.name }}</h1>
        <div class="price">${{ tier_info.price }}<span style="font-size: 1rem;">/month</span></div>
        
        <div class="features">
            <h3>What you get:</h3>
            <ul>
            {% for feature in tier_info.features %}
                <li>{{ feature }}</li>
            {% endfor %}
            </ul>
        </div>
        
        {% if tier == 'enterprise' %}
            <p>Contact our sales team for custom Enterprise pricing and deployment.</p>
            <a href="mailto:sales@yourdomain.com" class="btn">Contact Sales</a>
        {% else %}
            <button class="btn" onclick="checkout()">Subscribe for ${{ tier_info.price }}/month</button>
        {% endif %}
        
        <p><small>Cancel anytime • 30-day money-back guarantee</small></p>
    </div>
    
    <script>
        const stripe = Stripe('{{ config.STRIPE_PUBLISHABLE_KEY }}');
        
        function checkout() {
            fetch('/api/create-checkout-session', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({tier: '{{ tier }}'})
            })
            .then(response => response.json())
            .then(session => {
                return stripe.redirectToCheckout({sessionId: session.id});
            });
        }
    </script>
</body>
</html>
    """, tier_info=tier_info, tier=tier, config=Config)

@billing_bp.route('/success')
def success():
    """Payment success page"""
    session['user_tier'] = 'pro'  # In production, verify payment properly
    return render_template_string("""
    <h1>Welcome to Pro!</h1>
    <p>Your subscription is active. You now have access to 50 agents and premium features.</p>
    <a href="/dashboard">Go to Dashboard</a>
    """)