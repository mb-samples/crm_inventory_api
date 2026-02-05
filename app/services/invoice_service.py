"""Invoice service layer"""
from app.utils.db_connection import execute_query, execute_transaction
from app.utils.query_helpers import QueryBuilder

class InvoiceService:
    @staticmethod
    def get_all(page=1, limit=50, customer_id=None, status=None, overdue=False):
        query = QueryBuilder('invoices i').select("""
            i.*, c.company_name, o.order_number
        """).join('customers c ON i.customer_id = c.customer_id')
        query.join('orders o ON i.order_id = o.order_id')
        
        if customer_id:
            query.where('i.customer_id = ?', customer_id)
        if status:
            query.where('i.invoice_status = ?', status)
        if overdue:
            query.where('i.due_date < GETDATE() AND i.amount_due > 0')
        
        query.order('i.invoice_date DESC').paginate(page, limit)
        return execute_query(query.sql, query.params)
    
    @staticmethod
    def get_by_id(invoice_id):
        query = """
        SELECT i.*, c.company_name, o.order_number
        FROM invoices i
        JOIN customers c ON i.customer_id = c.customer_id
        JOIN orders o ON i.order_id = o.order_id
        WHERE i.invoice_id = ?
        """
        result = execute_query(query, [invoice_id])
        return result[0] if result else None
    
    @staticmethod
    def create(data):
        query = """
        INSERT INTO invoices (invoice_number, order_id, customer_id, invoice_date, due_date,
                              subtotal, tax_amount, total_amount, amount_paid, invoice_status,
                              payment_terms, notes, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [data.get('invoice_number'), data.get('order_id'), data.get('customer_id'),
                  data.get('invoice_date'), data.get('due_date'), data.get('subtotal'),
                  data.get('tax_amount', 0), data.get('total_amount'), data.get('amount_paid', 0),
                  data.get('invoice_status', 'draft'), data.get('payment_terms', 30),
                  data.get('notes'), data.get('created_by')]
        return execute_transaction(query, params)
    
    @staticmethod
    def update(invoice_id, data):
        query = """
        UPDATE invoices 
        SET due_date = ?, subtotal = ?, tax_amount = ?, total_amount = ?, amount_paid = ?,
            invoice_status = ?, payment_terms = ?, notes = ?, updated_at = GETDATE()
        WHERE invoice_id = ?
        """
        params = [data.get('due_date'), data.get('subtotal'), data.get('tax_amount'),
                  data.get('total_amount'), data.get('amount_paid'), data.get('invoice_status'),
                  data.get('payment_terms'), data.get('notes'), invoice_id]
        return execute_transaction(query, params)
    
    @staticmethod
    def delete(invoice_id):
        return execute_transaction('DELETE FROM invoices WHERE invoice_id = ?', [invoice_id])
