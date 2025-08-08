"""
Application configuration
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_...')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_...')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    
    # Pricing configuration
    PRICING_TIERS = {
        'free': {
            'name': 'Free Tier',
            'price': 0,
            'agents_limit': 3,
            'tasks_per_hour': 10,
            'features': ['Basic agents', 'Free OpenRouter models', 'Web dashboard']
        },
        'pro': {
            'name': 'Pro',
            'price': 29,
            'agents_limit': 50,
            'tasks_per_hour': 500,
            'features': ['All agent types', 'Premium models', 'Priority support', 'API access']
        },
        'enterprise': {
            'name': 'Enterprise',
            'price': 299,
            'agents_limit': -1,
            'tasks_per_hour': -1,
            'features': ['Unlimited agents', 'Custom deployment', 'SLA', '24/7 support']
        }
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'