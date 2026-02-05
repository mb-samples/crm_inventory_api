"""Customer routes"""
from flask import Blueprint, request, jsonify
from app.services.customer_service import CustomerService
import logging

logger = logging.getLogger(__name__)
customer_bp = Blueprint('customers', __name__)

@customer_bp.route('', methods=['GET'])
def get_customers():
    """Get all customers"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        status = request.args.get('status')
        
        customers = CustomerService.get_all(page, limit, status)
        return jsonify({'data': customers, 'page': page, 'limit': limit}), 200
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get customer by ID"""
    try:
        customer = CustomerService.get_by_id(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        return jsonify(customer), 200
    except Exception as e:
        logger.error(f"Error fetching customer: {str(e)}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('', methods=['POST'])
def create_customer():
    """Create new customer"""
    try:
        data = request.get_json()
        customer = CustomerService.create(data)
        return jsonify(customer), 201
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update customer"""
    try:
        data = request.get_json()
        customer = CustomerService.update(customer_id, data)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        return jsonify(customer), 200
    except Exception as e:
        logger.error(f"Error updating customer: {str(e)}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete customer"""
    try:
        CustomerService.delete(customer_id)
        return jsonify({'message': 'Customer deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting customer: {str(e)}")
        return jsonify({'error': str(e)}), 500
