"""Product routes"""
from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
import logging

logger = logging.getLogger(__name__)
product_bp = Blueprint('products', __name__)

@product_bp.route('', methods=['GET'])
def get_products():
    """
    Get all products with pagination
    ---
    tags:
      - Products
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number
      - name: limit
        in: query
        type: integer
        default: 50
        description: Items per page
      - name: category
        in: query
        type: string
        description: Filter by category
      - name: status
        in: query
        type: string
        description: Filter by status (active, discontinued)
    responses:
      200:
        description: List of products
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
            page:
              type: integer
            limit:
              type: integer
    """
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
    """
    Get product by ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: Product ID
    responses:
      200:
        description: Product details
      404:
        description: Product not found
    """
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
    """
    Create new product
    ---
    tags:
      - Products
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - product_code
            - product_name
            - category
            - unit_price
          properties:
            product_code:
              type: string
              example: PROD004
            product_name:
              type: string
              example: New Product
            category:
              type: string
              example: Electronics
            description:
              type: string
              example: Product description
            unit_price:
              type: number
              example: 99.99
            cost_price:
              type: number
              example: 50.00
            reorder_level:
              type: integer
              example: 10
    responses:
      201:
        description: Product created successfully
      400:
        description: Invalid input
    """
    try:
        data = request.get_json()
        product = ProductService.create(data)
        return jsonify(product), 201
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: Product ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            product_name:
              type: string
            category:
              type: string
            description:
              type: string
            unit_price:
              type: number
            cost_price:
              type: number
            status:
              type: string
    responses:
      200:
        description: Product updated successfully
      404:
        description: Product not found
    """
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
    """
    Delete product (soft delete)
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: Product ID
    responses:
      200:
        description: Product deleted successfully
      404:
        description: Product not found
    """
    try:
        ProductService.delete(product_id)
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        return jsonify({'error': str(e)}), 500
