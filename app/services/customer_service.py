"""Customer service layer"""
from app.utils.db_connection import get_connection
from app.utils.query_helpers import QueryBuilder, rows_to_dict_list
from app.models.customer import Customer
import logging

logger = logging.getLogger(__name__)

class CustomerService:
    @staticmethod
    def get_all(page=1, limit=50, status=None):
        """Get all customers with pagination"""
        with get_connection() as conn:
            query = QueryBuilder('customers').select('*')
            if status:
                query.where('status = ?', status)
            query.order('created_at DESC').paginate(page, limit)
            
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            return rows_to_dict_list(cursor)
    
    @staticmethod
    def get_by_id(customer_id):
        """Get customer by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,))
            row = cursor.fetchone()
            return dict(zip([col[0] for col in cursor.description], row)) if row else None
    
    @staticmethod
    def create(data):
        """Create new customer"""
        with get_connection() as conn:
            query = QueryBuilder('customers').build_insert_query(data)
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            cursor.execute('SELECT @@IDENTITY')
            customer_id = cursor.fetchone()[0]
            conn.commit()
            return CustomerService.get_by_id(customer_id)
    
    @staticmethod
    def update(customer_id, data):
        """Update customer"""
        with get_connection() as conn:
            query = QueryBuilder('customers').build_update_query(data, f'customer_id = {customer_id}')
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            conn.commit()
            return CustomerService.get_by_id(customer_id)
    
    @staticmethod
    def delete(customer_id):
        """Delete customer (soft delete)"""
        return CustomerService.update(customer_id, {'status': 'inactive'})
