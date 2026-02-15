"""Flask application factory"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
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
    
    logger = logging.getLogger(__name__)
    
    # Initialize CORS
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "CRM & Inventory Management API",
            "description": "RESTful API with MSSQL data layer (Mock DB enabled)",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Initialize database connection pool
    try:
        # Get connection string as string, not property
        config_instance = config()
        initialize_pool(config_instance)
        db_available = True
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        db_available = False
        logger.warning(f"Database connection failed: {str(e)}")
        logger.warning("Running in NO-DATABASE mode. API endpoints will not work.")
    
    # Store database availability in app config
    app.config['DB_AVAILABLE'] = db_available
    
    # Register blueprints only if database is available
    if db_available:
        from app.routes.customer_routes import customer_bp
        from app.routes.product_routes import product_bp
        from app.routes.order_routes import order_bp
        
        app.register_blueprint(customer_bp, url_prefix='/api/customers')
        app.register_blueprint(product_bp, url_prefix='/api/products')
        app.register_blueprint(order_bp, url_prefix='/api/orders')
        logger.info("API routes registered successfully")
    else:
        logger.warning("API routes not registered - database unavailable")
    
    # Health check endpoint
    @app.route('/health')
    def health():
        db_status = 'connected' if app.config.get('DB_AVAILABLE', False) else 'disconnected'
        return {
            'status': 'healthy',
            'database': db_status,
            'message': 'API is running' if db_status == 'connected' else 'API running without database'
        }, 200
    
    # Cleanup on shutdown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_all()
    
    return app
