"""Order routes"""
from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService
import logging

logger = logging.getLogger(__name__)
order_bp = Blueprint('orders', __name__)

@order_bp.route('', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        customer_id = request.args.get('customer_id')
        status = request.args.get('status')
        
        orders = OrderService.get_all(page, limit, customer_id, status)
        return jsonify({'data': orders, 'page': page, 'limit': limit}), 200
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    try:
        order = OrderService.get_by_id(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify(order), 200
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        return jsonify({'error': str(e)}), 500

@order_bp.route('', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.get_json()
        order = OrderService.create(data)
        return jsonify(order), 201
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order"""
    try:
        data = request.get_json()
        order = OrderService.update(order_id, data)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify(order), 200
    except Exception as e:
        logger.error(f"Error updating order: {str(e)}")
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete order"""
    try:
        OrderService.delete(order_id)
        return jsonify({'message': 'Order cancelled'}), 200
    except Exception as e:
        logger.error(f"Error deleting order: {str(e)}")
        return jsonify({'error': str(e)}), 500
