"""Contact service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class ContactService:
    @staticmethod
    def get_all(page=1, limit=50, customer_id=None, account_id=None):
        query = QueryBuilder('contacts').select('*')
        if customer_id:
            query.where('customer_id = ?', customer_id)
        if account_id:
            query.where('account_id = ?', account_id)
        query.order('is_primary DESC, created_at DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(contact_id):
        result = execute_query('SELECT * FROM contacts WHERE contact_id = ?', [contact_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO contacts (customer_id, account_id, first_name, last_name, title, 
                              department, email, phone, mobile, is_primary, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('customer_id'), data.get('account_id'), data.get('first_name'),
                  data.get('last_name'), data.get('title'), data.get('department'),
                  data.get('email'), data.get('phone'), data.get('mobile'),
                  data.get('is_primary', False), data.get('status', 'active'), data.get('notes')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(contact_id, data):
        query = """
        UPDATE contacts 
        SET first_name = ?, last_name = ?, title = ?, department = ?, email = ?,
            phone = ?, mobile = ?, is_primary = ?, status = ?, notes = ?, updated_at = GETDATE()
        WHERE contact_id = ?
        """
        params = [data.get('first_name'), data.get('last_name'), data.get('title'),
                  data.get('department'), data.get('email'), data.get('phone'),
                  data.get('mobile'), data.get('is_primary'), data.get('status'),
                  data.get('notes'), contact_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(contact_id):
        return execute_transaction('DELETE FROM contacts WHERE contact_id = ?', [contact_id])
