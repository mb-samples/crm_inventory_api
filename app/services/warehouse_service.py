"""Warehouse service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class WarehouseService:
    @staticmethod
    def get_all(page=1, limit=50, status=None):
        query = QueryBuilder('warehouses').select('*')
        if status:
            query.where('status = ?', status)
        query.order('warehouse_name').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(warehouse_id):
        result = execute_query('SELECT * FROM warehouses WHERE warehouse_id = ?', [warehouse_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO warehouses (warehouse_code, warehouse_name, location, address, city, 
                                state, country, postal_code, phone, manager_user_id, capacity, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('warehouse_code'), data.get('warehouse_name'), data.get('location'),
                  data.get('address'), data.get('city'), data.get('state'), data.get('country'),
                  data.get('postal_code'), data.get('phone'), data.get('manager_user_id'),
                  data.get('capacity'), data.get('status', 'active')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(warehouse_id, data):
        query = """
        UPDATE warehouses 
        SET warehouse_name = ?, location = ?, address = ?, city = ?, state = ?,
            country = ?, postal_code = ?, phone = ?, manager_user_id = ?, 
            capacity = ?, status = ?, updated_at = GETDATE()
        WHERE warehouse_id = ?
        """
        params = [data.get('warehouse_name'), data.get('location'), data.get('address'),
                  data.get('city'), data.get('state'), data.get('country'),
                  data.get('postal_code'), data.get('phone'), data.get('manager_user_id'),
                  data.get('capacity'), data.get('status'), warehouse_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(warehouse_id):
        return execute_transaction('DELETE FROM warehouses WHERE warehouse_id = ?', [warehouse_id])
