"""Inventory service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class InventoryService:
    @staticmethod
    def get_all(page=1, limit=50, product_id=None, warehouse_id=None, low_stock=False):
        query = QueryBuilder('inventory i').select("""
            i.*, p.product_name, p.product_code, w.warehouse_name
        """).join('products p ON i.product_id = p.product_id')
        query.join('warehouses w ON i.warehouse_id = w.warehouse_id')
        
        if product_id:
            query.where('i.product_id = ?', product_id)
        if warehouse_id:
            query.where('i.warehouse_id = ?', warehouse_id)
        if low_stock:
            query.where('i.quantity_available <= p.reorder_level')
        
        query.order('i.updated_at DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(inventory_id):
        query = """
        SELECT i.*, p.product_name, p.product_code, w.warehouse_name
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN warehouses w ON i.warehouse_id = w.warehouse_id
        WHERE i.inventory_id = ?
        """
        result = execute_query(query, [inventory_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO inventory (product_id, warehouse_id, quantity_on_hand, quantity_reserved, 
                               bin_location, last_stock_check, last_restock_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('product_id'), data.get('warehouse_id'), 
                  data.get('quantity_on_hand', 0), data.get('quantity_reserved', 0),
                  data.get('bin_location'), data.get('last_stock_check'), 
                  data.get('last_restock_date')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(inventory_id, data):
        query = """
        UPDATE inventory 
        SET quantity_on_hand = ?, quantity_reserved = ?, bin_location = ?,
            last_stock_check = ?, last_restock_date = ?, updated_at = GETDATE()
        WHERE inventory_id = ?
        """
        params = [data.get('quantity_on_hand'), data.get('quantity_reserved'),
                  data.get('bin_location'), data.get('last_stock_check'),
                  data.get('last_restock_date'), inventory_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(inventory_id):
        return execute_transaction('DELETE FROM inventory WHERE inventory_id = ?', [inventory_id])
