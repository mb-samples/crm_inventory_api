"""Supplier service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class SupplierService:
    @staticmethod
    def get_all(page=1, limit=50, status=None):
        query = QueryBuilder('suppliers').select('*')
        if status:
            query.where('status = ?', status)
        query.order('supplier_name').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(supplier_id):
        result = execute_query('SELECT * FROM suppliers WHERE supplier_id = ?', [supplier_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO suppliers (supplier_code, supplier_name, contact_person, email, phone,
                               address, city, state, country, postal_code, payment_terms, 
                               tax_id, rating, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('supplier_code'), data.get('supplier_name'), data.get('contact_person'),
                  data.get('email'), data.get('phone'), data.get('address'), data.get('city'),
                  data.get('state'), data.get('country'), data.get('postal_code'),
                  data.get('payment_terms', 30), data.get('tax_id'), data.get('rating'),
                  data.get('status', 'active')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(supplier_id, data):
        query = """
        UPDATE suppliers 
        SET supplier_name = ?, contact_person = ?, email = ?, phone = ?, address = ?,
            city = ?, state = ?, country = ?, postal_code = ?, payment_terms = ?,
            tax_id = ?, rating = ?, status = ?, updated_at = GETDATE()
        WHERE supplier_id = ?
        """
        params = [data.get('supplier_name'), data.get('contact_person'), data.get('email'),
                  data.get('phone'), data.get('address'), data.get('city'), data.get('state'),
                  data.get('country'), data.get('postal_code'), data.get('payment_terms'),
                  data.get('tax_id'), data.get('rating'), data.get('status'), supplier_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(supplier_id):
        return execute_transaction('DELETE FROM suppliers WHERE supplier_id = ?', [supplier_id])
