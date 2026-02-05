"""Activity service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class ActivityService:
    @staticmethod
    def get_all(page=1, limit=50, customer_id=None, assigned_user_id=None, status=None, activity_type=None):
        query = QueryBuilder('activities a').select("""
            a.*, c.company_name, u.username as assigned_to
        """).join('LEFT JOIN customers c ON a.customer_id = c.customer_id')
        query.join('LEFT JOIN users u ON a.assigned_user_id = u.user_id')
        
        if customer_id:
            query.where('a.customer_id = ?', customer_id)
        if assigned_user_id:
            query.where('a.assigned_user_id = ?', assigned_user_id)
        if status:
            query.where('a.status = ?', status)
        if activity_type:
            query.where('a.activity_type = ?', activity_type)
        
        query.order('a.activity_date DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(activity_id):
        query = """
        SELECT a.*, c.company_name, u.username as assigned_to
        FROM activities a
        LEFT JOIN customers c ON a.customer_id = c.customer_id
        LEFT JOIN users u ON a.assigned_user_id = u.user_id
        WHERE a.activity_id = ?
        """
        result = execute_query(query, [activity_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO activities (activity_type, subject, description, customer_id, contact_id,
                                order_id, activity_date, due_date, completed_date, status,
                                priority, assigned_user_id, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('activity_type'), data.get('subject'), data.get('description'),
                  data.get('customer_id'), data.get('contact_id'), data.get('order_id'),
                  data.get('activity_date'), data.get('due_date'), data.get('completed_date'),
                  data.get('status', 'pending'), data.get('priority', 'medium'),
                  data.get('assigned_user_id'), data.get('created_by')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(activity_id, data):
        query = """
        UPDATE activities 
        SET subject = ?, description = ?, activity_date = ?, due_date = ?, completed_date = ?,
            status = ?, priority = ?, assigned_user_id = ?, updated_at = GETDATE()
        WHERE activity_id = ?
        """
        params = [data.get('subject'), data.get('description'), data.get('activity_date'),
                  data.get('due_date'), data.get('completed_date'), data.get('status'),
                  data.get('priority'), data.get('assigned_user_id'), activity_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(activity_id):
        return execute_transaction('DELETE FROM activities WHERE activity_id = ?', [activity_id])
