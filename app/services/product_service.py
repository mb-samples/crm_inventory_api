"""Product service layer"""
from app.utils.db_connection import get_connection
from app.utils.query_helpers import QueryBuilder, rows_to_dict_list
from app.models.product import Product
import logging

logger = logging.getLogger(__name__)

class ProductService:
    @staticmethod
    def get_all(page=1, limit=50, category=None, status=None):
        """Get all products with pagination"""
        with get_connection() as conn:
            query = QueryBuilder('products').select('*')
            if category:
                query.where('category = ?', category)
            if status:
                query.where('status = ?', status)
            query.order('created_at', 'DESC').paginate(page, limit)
            
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
            row = cursor.fetchone()
            return dict(zip([col[0] for col in cursor.description], row)) if row else None
    
    @staticmethod
    def create(data):
        """Create new product"""
        with get_connection() as conn:
            query = QueryBuilder('products').build_insert_query(data)
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            cursor.execute('SELECT @@IDENTITY')
            product_id = cursor.fetchone()[0]
            conn.commit()
            return ProductService.get_by_id(product_id)
    
    @staticmethod
    def update(product_id, data):
        """Update product"""
        with get_connection() as conn:
            query = QueryBuilder('products').build_update_query(data, f'product_id = {product_id}')
            cursor = conn.cursor()
            cursor.execute(query.sql, query.params)
            conn.commit()
            return ProductService.get_by_id(product_id)
    
    @staticmethod
    def delete(product_id):
        """Delete product (soft delete)"""
        return ProductService.update(product_id, {'status': 'inactive'})
