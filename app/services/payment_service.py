"""Payment service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class PaymentService:
    @staticmethod
    def get_all(page=1, limit=50, customer_id=None, invoice_id=None, status=None):
        query = QueryBuilder('payments p').select("""
            p.*, c.company_name, i.invoice_number
        """).join('customers c ON p.customer_id = c.customer_id')
        query.join('invoices i ON p.invoice_id = i.invoice_id')
        
        if customer_id:
            query.where('p.customer_id = ?', customer_id)
        if invoice_id:
            query.where('p.invoice_id = ?', invoice_id)
        if status:
            query.where('p.payment_status = ?', status)
        
        query.order('p.payment_date DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(payment_id):
        query = """
        SELECT p.*, c.company_name, i.invoice_number
        FROM payments p
        JOIN customers c ON p.customer_id = c.customer_id
        JOIN invoices i ON p.invoice_id = i.invoice_id
        WHERE p.payment_id = ?
        """
        result = execute_query(query, [payment_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO payments (payment_number, invoice_id, customer_id, payment_date, payment_method,
                              payment_amount, reference_number, payment_status, notes, processed_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('payment_number'), data.get('invoice_id'), data.get('customer_id'),
                  data.get('payment_date'), data.get('payment_method'), data.get('payment_amount'),
                  data.get('reference_number'), data.get('payment_status', 'completed'),
                  data.get('notes'), data.get('processed_by')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(payment_id, data):
        query = """
        UPDATE payments 
        SET payment_method = ?, payment_amount = ?, reference_number = ?, 
            payment_status = ?, notes = ?, updated_at = GETDATE()
        WHERE payment_id = ?
        """
        params = [data.get('payment_method'), data.get('payment_amount'), 
                  data.get('reference_number'), data.get('payment_status'),
                  data.get('notes'), payment_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(payment_id):
        return execute_transaction('DELETE FROM payments WHERE payment_id = ?', [payment_id])
