"""Order routes"""
from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService
import logging

logger = logging.getLogger(__name__)
order_bp = Blueprint('orders', __name__)

@order_bp.route('', methods=['GET'])
def get_orders():
    """
    Get all orders with pagination
    ---
    tags:
      - Orders
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
      - name: customer_id
        in: query
        type: integer
        description: Filter by customer ID
      - name: status
        in: query
        type: string
        description: Filter by status (pending, confirmed, shipped, delivered, cancelled)
    responses:
      200:
        description: List of orders
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
        customer_id = request.args.get('customer_id')
        status = request.args.get('status')
        
        orders = OrderService.get_all(page, limit, customer_id, status)
        return jsonify({'data': orders, 'page': page, 'limit': limit}), 200
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get order by ID
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: Order ID
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
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
    """
    Create new order
    ---
    tags:
      - Orders
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_id
            - order_date
            - total_amount
          properties:
            customer_id:
              type: integer
              example: 1
            order_date:
              type: string
              format: date
              example: "2024-01-15"
            total_amount:
              type: number
              example: 1500.00
            status:
              type: string
              example: pending
            shipping_address:
              type: string
              example: 123 Main St, City, State
            payment_method:
              type: string
              example: credit_card
    responses:
      201:
        description: Order created successfully
      400:
        description: Invalid input
    """
    try:
        data = request.get_json()
        order = OrderService.create(data)
        return jsonify(order), 201
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return jsonify({'error': str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Update order
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: Order ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
              example: shipped
            shipping_address:
              type: string
            payment_method:
              type: string
            notes:
              type: string
    responses:
      200:
        description: Order updated successfully
      404:
        description: Order not found
    """
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
    """
    Cancel order
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: Order ID
    responses:
      200:
        description: Order cancelled successfully
      404:
        description: Order not found
    """
    try:
        OrderService.delete(order_id)
        return jsonify({'message': 'Order cancelled'}), 200
    except Exception as e:
        logger.error(f"Error deleting order: {str(e)}")
        return jsonify({'error': str(e)}), 500
