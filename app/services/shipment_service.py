"""Shipment service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class ShipmentService:
    @staticmethod
    def get_all(page=1, limit=50, order_id=None, status=None):
        query = QueryBuilder('shipments s').select("""
            s.*, o.order_number, w.warehouse_name
        """).join('orders o ON s.order_id = o.order_id')
        query.join('warehouses w ON s.warehouse_id = w.warehouse_id')
        
        if order_id:
            query.where('s.order_id = ?', order_id)
        if status:
            query.where('s.shipment_status = ?', status)
        
        query.order('s.shipment_date DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(shipment_id):
        query = """
        SELECT s.*, o.order_number, w.warehouse_name
        FROM shipments s
        JOIN orders o ON s.order_id = o.order_id
        JOIN warehouses w ON s.warehouse_id = w.warehouse_id
        WHERE s.shipment_id = ?
        """
        result = execute_query(query, [shipment_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO shipments (shipment_number, order_id, warehouse_id, carrier, tracking_number,
                               shipment_date, estimated_delivery, actual_delivery, shipment_status,
                               shipping_cost, weight, notes, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('shipment_number'), data.get('order_id'), data.get('warehouse_id'),
                  data.get('carrier'), data.get('tracking_number'), data.get('shipment_date'),
                  data.get('estimated_delivery'), data.get('actual_delivery'),
                  data.get('shipment_status', 'preparing'), data.get('shipping_cost'),
                  data.get('weight'), data.get('notes'), data.get('created_by')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(shipment_id, data):
        query = """
        UPDATE shipments 
        SET carrier = ?, tracking_number = ?, estimated_delivery = ?, actual_delivery = ?,
            shipment_status = ?, shipping_cost = ?, weight = ?, notes = ?, updated_at = GETDATE()
        WHERE shipment_id = ?
        """
        params = [data.get('carrier'), data.get('tracking_number'), data.get('estimated_delivery'),
                  data.get('actual_delivery'), data.get('shipment_status'), data.get('shipping_cost'),
                  data.get('weight'), data.get('notes'), shipment_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(shipment_id):
        return execute_transaction('DELETE FROM shipments WHERE shipment_id = ?', [shipment_id])
