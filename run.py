#!/usr/bin/env python3
"""
OpenRouter AI Multi-Agent System - Production Entry Point
Run the Flask application with proper configuration
"""

import os
from app import create_app
from app.core.config import DevelopmentConfig, ProductionConfig

def main():
    """Main application entry point"""
    # Determine environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        config = ProductionConfig
    else:
        config = DevelopmentConfig
    
    # Create Flask app
    app = create_app(config)
    
    # Print startup info
    print("🚀 OpenRouter AI Multi-Agent System")
    print("=" * 50)
    print("💰 Monetization Features:")
    print("  - Free tier with limits")
    print("  - Pro tier ($29/month)")
    print("  - Enterprise tier ($299/month)")
    print("  - Stripe payment integration")
    print()
    print("🌐 Starting server...")
    print("  Landing page: http://localhost:5000")
    print("  Dashboard: http://localhost:5000/dashboard")
    print("  API: http://localhost:5000/api")
    print()
    print("💡 Ready for production deployment!")
    
    # Run the app
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )

if __name__ == '__main__':
    main()