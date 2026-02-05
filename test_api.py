"""
Simple test script to verify API endpoints without database
"""
import os
os.environ['FLASK_ENV'] = 'development'
os.environ['DB_SERVER'] = 'mock'

# Mock pyodbc before importing app
import sys
from unittest.mock import MagicMock
sys.modules['pyodbc'] = MagicMock()

from flask import Flask, jsonify

app = Flask(__name__)

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

# Mock API endpoints
@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify({
        'data': [
            {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
            {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
        ],
        'total': 2,
        'page': 1
    }), 200

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    return jsonify({
        'id': customer_id,
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '555-0123',
        'company': 'Acme Corp'
    }), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({
        'data': [
            {'id': 1, 'name': 'Widget A', 'price': 29.99, 'stock': 100},
            {'id': 2, 'name': 'Widget B', 'price': 49.99, 'stock': 50}
        ],
        'total': 2,
        'page': 1
    }), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return jsonify({
        'id': product_id,
        'name': 'Widget A',
        'price': 29.99,
        'stock': 100,
        'category': 'Electronics'
    }), 200

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify({
        'data': [
            {'id': 1, 'customer_id': 1, 'total': 299.99, 'status': 'completed'},
            {'id': 2, 'customer_id': 2, 'total': 149.99, 'status': 'pending'}
        ],
        'total': 2,
        'page': 1
    }), 200

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    return jsonify({
        'id': order_id,
        'customer_id': 1,
        'total': 299.99,
        'status': 'completed',
        'items': [
            {'product_id': 1, 'quantity': 2, 'price': 29.99}
        ]
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n{'='*60}")
    print(f"🚀 Mock CRM & Inventory API Server Starting")
    print(f"{'='*60}")
    print(f"Server running at: http://localhost:{port}")
    print(f"\nAvailable endpoints:")
    print(f"  GET  http://localhost:{port}/health")
    print(f"  GET  http://localhost:{port}/api/customers")
    print(f"  GET  http://localhost:{port}/api/customers/<id>")
    print(f"  GET  http://localhost:{port}/api/products")
    print(f"  GET  http://localhost:{port}/api/products/<id>")
    print(f"  GET  http://localhost:{port}/api/orders")
    print(f"  GET  http://localhost:{port}/api/orders/<id>")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
