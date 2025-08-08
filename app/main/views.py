"""
Main application views
"""
from flask import render_template_string, jsonify
from datetime import datetime
from . import main_bp

@main_bp.route('/')
def landing_page():
    """Landing page with pricing and features"""
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>OpenRouter AI Agents - Automate Everything with AI</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Create autonomous AI agents that work together to automate your workflows. Start FREE with OpenRouter models.">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; }
        
        /* Header */
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; text-align: center; }
        .header h1 { font-size: 3rem; margin-bottom: 1rem; }
        .header p { font-size: 1.2rem; opacity: 0.9; max-width: 600px; margin: 0 auto 2rem; }
        .cta-button { background: #ff6b6b; color: white; padding: 1rem 2rem; border: none; border-radius: 5px; font-size: 1.1rem; cursor: pointer; text-decoration: none; display: inline-block; transition: all 0.3s; }
        .cta-button:hover { background: #ff5252; transform: translateY(-2px); }
        
        /* Features */
        .features { padding: 4rem 2rem; max-width: 1200px; margin: 0 auto; }
        .features h2 { text-align: center; margin-bottom: 3rem; font-size: 2.5rem; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .feature { text-align: center; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .feature h3 { color: #667eea; margin-bottom: 1rem; }
        
        /* Pricing */
        .pricing { background: #f8f9fa; padding: 4rem 2rem; }
        .pricing h2 { text-align: center; margin-bottom: 3rem; font-size: 2.5rem; }
        .pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; max-width: 1000px; margin: 0 auto; }
        .pricing-card { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); text-align: center; position: relative; }
        .pricing-card.featured { border: 3px solid #667eea; transform: scale(1.05); }
        .pricing-card h3 { color: #667eea; margin-bottom: 1rem; }
        .price { font-size: 2.5rem; color: #333; margin-bottom: 1rem; }
        .price span { font-size: 1rem; color: #666; }
        .features-list { list-style: none; margin: 2rem 0; }
        .features-list li { padding: 0.5rem 0; }
        
        /* Footer */
        .footer { background: #333; color: white; padding: 3rem 2rem; text-align: center; }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .pricing-card.featured { transform: none; }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <h1>OpenRouter AI Agents</h1>
        <p>Create autonomous AI agents that research, code, write, and coordinate complex tasks. Start completely FREE with OpenRouter models!</p>
        <a href="/dashboard" class="cta-button">Start Free Now</a>
        <br><br>
        <small>No Credit Card Required • $0 to Start • Unlimited Free Tier</small>
    </div>
    
    <!-- Features -->
    <div class="features">
        <h2>Why Choose OpenRouter AI Agents?</h2>
        <div class="feature-grid">
            <div class="feature">
                <h3>Start Completely Free</h3>
                <p>Use OpenRouter's free models with unlimited agents and tasks. No credit card, no hidden costs, no limits on the free tier.</p>
            </div>
            <div class="feature">
                <h3>7 Specialized Agents</h3>
                <p>Coordinator, Researcher, Coder, Writer, Analyst, Reviewer, and Executor agents - each optimized for specific tasks.</p>
            </div>
            <div class="feature">
                <h3>Production Ready</h3>
                <p>Battle-tested system with web dashboard, REST API, monitoring, and enterprise-grade reliability.</p>
            </div>
            <div class="feature">
                <h3>Multi-Agent Workflows</h3>
                <p>Agents collaborate and coordinate automatically. Create complex workflows that run autonomously.</p>
            </div>
            <div class="feature">
                <h3>Easy Integration</h3>
                <p>REST API, Python SDK, web dashboard, and Docker deployment. Integrate with any existing system.</p>
            </div>
            <div class="feature">
                <h3>Real-Time Monitoring</h3>
                <p>Track agent performance, costs, and results in real-time. Complete transparency and control.</p>
            </div>
        </div>
    </div>
    
    <!-- Pricing -->
    <div class="pricing">
        <h2>Pricing Plans</h2>
        <div class="pricing-grid">
            <div class="pricing-card">
                <h3>Free</h3>
                <div class="price">$0<span>/month</span></div>
                <ul class="features-list">
                    <li>3 Agents</li>
                    <li>10 Tasks/hour</li>
                    <li>Free OpenRouter models</li>
                    <li>Web dashboard</li>
                    <li>Community support</li>
                </ul>
                <a href="/dashboard" class="cta-button">Get Started Free</a>
            </div>
            
            <div class="pricing-card featured">
                <h3>Pro</h3>
                <div class="price">$29<span>/month</span></div>
                <ul class="features-list">
                    <li>50 Agents</li>
                    <li>500 Tasks/hour</li>
                    <li>Premium AI models</li>
                    <li>API access</li>
                    <li>Priority support</li>
                    <li>Advanced workflows</li>
                </ul>
                <a href="/billing/upgrade/pro" class="cta-button">Upgrade to Pro</a>
            </div>
            
            <div class="pricing-card">
                <h3>Enterprise</h3>
                <div class="price">$299<span>/month</span></div>
                <ul class="features-list">
                    <li>Unlimited agents</li>
                    <li>Unlimited tasks</li>
                    <li>Custom deployment</li>
                    <li>SLA guarantee</li>
                    <li>24/7 support</li>
                    <li>Custom integrations</li>
                </ul>
                <a href="/billing/upgrade/enterprise" class="cta-button">Contact Sales</a>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="footer">
        <p>Built with love for developers and teams who want to automate everything</p>
        <p>Questions? <a href="mailto:support@yourdomain.com" style="color: #667eea;">Contact Support</a></p>
    </div>
</body>
</html>
    """)

@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })