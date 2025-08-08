"""
OpenRouter AI Multi-Agent System
Production Flask Application
"""

from flask import Flask
from flask_cors import CORS
import os

def create_app(config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    app.config['OPENROUTER_API_KEY'] = os.environ.get('OPENROUTER_API_KEY')
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.main import main_bp
    from app.api import api_bp
    from app.dashboard import dashboard_bp
    from app.auth import auth_bp
    from app.billing import billing_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(billing_bp, url_prefix='/billing')
    
    return app