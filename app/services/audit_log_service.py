"""Audit Log service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class AuditLogService:
    @staticmethod
    def get_all(page=1, limit=50, table_name=None, record_id=None, action=None, changed_by=None):
        query = QueryBuilder('audit_logs a').select("""
            a.*, u.username as changed_by_username
        """).join('LEFT JOIN users u ON a.changed_by = u.user_id')
        
        if table_name:
            query.where('a.table_name = ?', table_name)
        if record_id:
            query.where('a.record_id = ?', record_id)
        if action:
            query.where('a.action = ?', action)
        if changed_by:
            query.where('a.changed_by = ?', changed_by)
        
        query.order('a.changed_at DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(audit_id):
        query = """
        SELECT a.*, u.username as changed_by_username
        FROM audit_logs a
        LEFT JOIN users u ON a.changed_by = u.user_id
        WHERE a.audit_id = ?
        """
        result = execute_query(query, [audit_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO audit_logs (table_name, record_id, action, old_values, new_values,
                                changed_by, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('table_name'), data.get('record_id'), data.get('action'),
                  data.get('old_values'), data.get('new_values'), data.get('changed_by'),
                  data.get('ip_address'), data.get('user_agent')]
        return execute_transaction(query, params)
    
    @staticmethod
    def get_record_history(table_name, record_id):
        """Get complete audit history for a specific record"""
        query = """
        SELECT a.*, u.username as changed_by_username
        FROM audit_logs a
        LEFT JOIN users u ON a.changed_by = u.user_id
        WHERE a.table_name = ? AND a.record_id = ?
        ORDER BY a.changed_at DESC
        """
        return execute_query(query, [table_name, record_id])
