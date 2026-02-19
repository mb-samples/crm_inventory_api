"""Analytics routes"""
from flask import Blueprint, request, jsonify
from app.utils.advanced_data_layer import AdvancedDataLayer
import logging

logger = logging.getLogger(__name__)
analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/customers', methods=['GET'])
def get_customer_analytics():
    """
    Get customer analytics
    ---
    tags:
      - Analytics
    parameters:
      - name: customer_id
        in: query
        type: integer
        description: Filter by customer ID
      - name: start_date
        in: query
        type: string
        format: date
        description: Start date for analysis
      - name: end_date
        in: query
        type: string
        format: date
        description: End date for analysis
    responses:
      200:
        description: Customer analytics data
    """
    try:
        customer_id = request.args.get('customer_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        data = AdvancedDataLayer.get_customer_analytics(customer_id, start_date, end_date)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching customer analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/inventory-status', methods=['GET'])
def get_inventory_status():
    """
    Get inventory status report
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Inventory status across all warehouses
    """
    try:
        data = AdvancedDataLayer.get_inventory_status_report()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching inventory status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/sales-performance', methods=['GET'])
def get_sales_performance():
    """
    Get sales performance by period
    ---
    tags:
      - Analytics
    parameters:
      - name: period
        in: query
        type: string
        enum: [day, week, month, quarter, year]
        default: month
        description: Time period for aggregation
      - name: start_date
        in: query
        type: string
        format: date
        description: Start date for analysis
      - name: end_date
        in: query
        type: string
        format: date
        description: End date for analysis
    responses:
      200:
        description: Sales performance data
    """
    try:
        period = request.args.get('period', 'month')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        data = AdvancedDataLayer.get_sales_performance_by_period(period, start_date, end_date)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching sales performance: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/product-performance', methods=['GET'])
def get_product_performance():
    """
    Get product performance metrics
    ---
    tags:
      - Analytics
    parameters:
      - name: top_n
        in: query
        type: integer
        default: 20
        description: Number of top products to return
    responses:
      200:
        description: Product performance data
    """
    try:
        top_n = int(request.args.get('top_n', 20))
        data = AdvancedDataLayer.get_product_performance_analysis(top_n)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching product performance: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/order-fulfillment', methods=['GET'])
def get_order_fulfillment():
    """
    Get order fulfillment metrics
    ---
    tags:
      - Analytics
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        description: Start date for analysis
      - name: end_date
        in: query
        type: string
        format: date
        description: End date for analysis
    responses:
      200:
        description: Order fulfillment statistics
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        data = AdvancedDataLayer.get_order_fulfillment_metrics(start_date, end_date)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching order fulfillment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/customer-segmentation', methods=['GET'])
def get_customer_segmentation():
    """
    Get customer segmentation analysis
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Customer segments by value and behavior
    """
    try:
        data = AdvancedDataLayer.get_customer_segmentation()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching customer segmentation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/payment-collection', methods=['GET'])
def get_payment_collection():
    """
    Get payment collection efficiency
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Payment collection metrics
    """
    try:
        data = AdvancedDataLayer.get_payment_collection_report()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching payment collection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/warehouse-utilization', methods=['GET'])
def get_warehouse_utilization():
    """
    Get warehouse utilization metrics
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Warehouse capacity and utilization
    """
    try:
        data = AdvancedDataLayer.get_warehouse_utilization()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching warehouse utilization: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/user-activity', methods=['GET'])
def get_user_activity():
    """
    Get user activity summary
    ---
    tags:
      - Analytics
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        description: Start date for analysis
      - name: end_date
        in: query
        type: string
        format: date
        description: End date for analysis
    responses:
      200:
        description: User activity metrics
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        data = AdvancedDataLayer.get_activity_summary_by_user(start_date, end_date)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching user activity: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/supplier-performance', methods=['GET'])
def get_supplier_performance():
    """
    Get supplier performance metrics
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Supplier delivery and quality metrics
    """
    try:
        data = AdvancedDataLayer.get_supplier_performance()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching supplier performance: {str(e)}")
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/revenue-forecast', methods=['GET'])
def get_revenue_forecast():
    """
    Get revenue forecast
    ---
    tags:
      - Analytics
    parameters:
      - name: months_ahead
        in: query
        type: integer
        default: 3
        description: Number of months to forecast
    responses:
      200:
        description: Revenue forecast data
    """
    try:
        months_ahead = int(request.args.get('months_ahead', 3))
        data = AdvancedDataLayer.get_revenue_forecast(months_ahead)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error fetching revenue forecast: {str(e)}")
        return jsonify({'error': str(e)}), 500
