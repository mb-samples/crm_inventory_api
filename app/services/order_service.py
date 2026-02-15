"""Order service layer"""
from app.utils.db_connection import get_connection
from app.utils.query_helpers import QueryBuilder, rows_to_dict_list
from app.models.order import Order
import logging

logger = logging.getLogger(__name__)

class OrderService:
    @staticmethod
    def get_all(page=1, limit=50, customer_id=None, status=None):
        """Get all orders with pagination"""
        with get_connection() as conn:
            query = QueryBuilder('orders').select('*')
            if customer_id:
                query.where('customer_id = ?', customer_id)
            if status:
                query.where('status = ?', status)
            query.order('order_date', 'DESC').paginate(page, limit)
            
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    @staticmethod
    def get_by_id(order_id):
        """Get order by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
            row = cursor.fetchone()
            return dict(zip([col[0] for col in cursor.description], row)) if row else None
    
    @staticmethod
    def create(data):
        """Create new order"""
        with get_connection() as conn:
            query = QueryBuilder('orders').build_insert_query(data)
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            cursor.execute('SELECT @@IDENTITY')
            order_id = cursor.fetchone()[0]
            conn.commit()
            return OrderService.get_by_id(order_id)
    
    @staticmethod
    def update(order_id, data):
        """Update order"""
        with get_connection() as conn:
            query = QueryBuilder('orders').build_update_query(data, f'order_id = {order_id}')
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            conn.commit()
            return OrderService.get_by_id(order_id)
    
    @staticmethod
    def delete(order_id):
        """Delete order (soft delete)"""
        return OrderService.update(order_id, {'status': 'cancelled'})
