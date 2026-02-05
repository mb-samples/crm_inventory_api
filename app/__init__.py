"""Flask application factory"""
from flask import Flask
from flask_cors import CORS
from config.config import get_config
from app.utils.db_connection import initialize_pool, close_all
import logging

def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize CORS
    CORS(app, origins=config.CORS_ORIGINS.split(','))
    
    # Initialize database connection pool
    initialize_pool(config)
    
    # Register blueprints
    from app.routes.customer_routes import customer_bp
    from app.routes.product_routes import product_bp
    from app.routes.order_routes import order_bp
    
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # Cleanup on shutdown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_all()
    
    return app
