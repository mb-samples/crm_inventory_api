"""Customer routes"""
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.customer_service import CustomerService
import logging

logger = logging.getLogger(__name__)
customer_bp = Blueprint('customers', __name__)

@customer_bp.route('', methods=['GET'])
def get_customers():
    """
    Get all customers with pagination
    ---
    tags:
      - Customers
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
      - name: status
        in: query
        type: string
        description: Filter by status (active, inactive)
    responses:
      200:
        description: List of customers
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
        status = request.args.get('status')
        
        customers = CustomerService.get_all(page, limit, status)
        return jsonify({'data': customers, 'page': page, 'limit': limit}), 200
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """
    Get customer by ID
    ---
    tags:
      - Customers
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
        description: Customer ID
    responses:
      200:
        description: Customer details
      404:
        description: Customer not found
    """
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
    """
    Create new customer
    ---
    tags:
      - Customers
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_code
            - company_name
            - email
          properties:
            customer_code:
              type: string
              example: CUST004
            company_name:
              type: string
              example: New Company Inc
            customer_type:
              type: string
              example: corporate
            contact_name:
              type: string
              example: John Doe
            email:
              type: string
              example: john@newcompany.com
            phone:
              type: string
              example: 555-1234
            address:
              type: string
              example: 123 Business St
            credit_limit:
              type: number
              example: 50000
    responses:
      201:
        description: Customer created successfully
      400:
        description: Invalid input
    """
    try:
        data = request.get_json()
        customer = CustomerService.create(data)
        return jsonify(customer), 201
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """
    Update customer
    ---
    tags:
      - Customers
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
        description: Customer ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            company_name:
              type: string
            contact_name:
              type: string
            email:
              type: string
            phone:
              type: string
            address:
              type: string
            status:
              type: string
    responses:
      200:
        description: Customer updated successfully
      404:
        description: Customer not found
    """
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
    """
    Delete customer (soft delete)
    ---
    tags:
      - Customers
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
        description: Customer ID
    responses:
      200:
        description: Customer deleted successfully
      404:
        description: Customer not found
    """
    try:
        CustomerService.delete(customer_id)
        return jsonify({'message': 'Customer deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting customer: {str(e)}")
        return jsonify({'error': str(e)}), 500
