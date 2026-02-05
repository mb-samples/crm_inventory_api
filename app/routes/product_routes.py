"""Product routes"""
from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
import logging

logger = logging.getLogger(__name__)
product_bp = Blueprint('products', __name__)

@product_bp.route('', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        category = request.args.get('category')
        status = request.args.get('status')
        
        products = ProductService.get_all(page, limit, category, status)
        return jsonify({'data': products, 'page': page, 'limit': limit}), 200
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    try:
        product = ProductService.get_by_id(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product), 200
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('', methods=['POST'])
def create_product():
    """Create new product"""
    try:
        data = request.get_json()
        product = ProductService.create(data)
        return jsonify(product), 201
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product"""
    try:
        data = request.get_json()
        product = ProductService.update(product_id, data)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product), 200
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product"""
    try:
        ProductService.delete(product_id)
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        return jsonify({'error': str(e)}), 500
