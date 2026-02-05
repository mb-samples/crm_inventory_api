"""User service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder, rows_to_dict_list
from datetime import datetime

class UserService:
    @staticmethod
    def get_all(page=1, limit=50, role=None, is_active=None):
        query = QueryBuilder('users').select('user_id, username, email, first_name, last_name, role, is_active, last_login, created_at, updated_at')
        if role:
            query.where('role = ?', role)
        if is_active is not None:
            query.where('is_active = ?', is_active)
        query.order('created_at DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(user_id):
        query = 'SELECT user_id, username, email, first_name, last_name, role, is_active, last_login, created_at, updated_at FROM users WHERE user_id = ?'
        result = execute_query(query, [user_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('username'), data.get('email'), data.get('password_hash'),
                  data.get('first_name'), data.get('last_name'), 
                  data.get('role', 'user'), data.get('is_active', True)]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(user_id, data):
        query = """
        UPDATE users 
        SET username = ?, email = ?, first_name = ?, last_name = ?, 
            role = ?, is_active = ?, updated_at = GETDATE()
        WHERE user_id = ?
        """
        params = [data.get('username'), data.get('email'), data.get('first_name'),
                  data.get('last_name'), data.get('role'), data.get('is_active'), user_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(user_id):
        query = 'DELETE FROM users WHERE user_id = ?'
        return execute_transaction(query, [user_id])
