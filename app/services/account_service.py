"""Account service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class AccountService:
    @staticmethod
    def get_all(page=1, limit=50, customer_id=None, status=None):
        query = QueryBuilder('accounts').select('*')
        if customer_id:
            query.where('customer_id = ?', customer_id)
        if status:
            query.where('status = ?', status)
        query.order('created_at DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(account_id):
        result = execute_query('SELECT * FROM accounts WHERE account_id = ?', [account_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO accounts (customer_id, account_number, account_name, account_type, 
                              status, billing_address, shipping_address, phone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('customer_id'), data.get('account_number'), data.get('account_name'),
                  data.get('account_type'), data.get('status', 'active'), data.get('billing_address'),
                  data.get('shipping_address'), data.get('phone'), data.get('email')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(account_id, data):
        query = """
        UPDATE accounts 
        SET account_name = ?, account_type = ?, status = ?, billing_address = ?,
            shipping_address = ?, phone = ?, email = ?, updated_at = GETDATE()
        WHERE account_id = ?
        """
        params = [data.get('account_name'), data.get('account_type'), data.get('status'),
                  data.get('billing_address'), data.get('shipping_address'), 
                  data.get('phone'), data.get('email'), account_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(account_id):
        return execute_transaction('DELETE FROM accounts WHERE account_id = ?', [account_id])
