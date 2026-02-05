"""Advanced data layer with complex queries, analytics, and reporting"""
from app.utils.db_connection import get_db_connection, execute_query
from app.utils.query_helpers import QueryBuilder, rows_to_dict_list
from datetime import datetime, timedelta

class AdvancedDataLayer:
    """Complex database operations including analytics, aggregations, and multi-table joins"""
    
    @staticmethod
    def get_customer_analytics(customer_id=None, start_date=None, end_date=None):
        """Get comprehensive customer analytics with order history, revenue, and payment stats"""
        query = """
        SELECT 
            c.customer_id,
            c.company_name,
            c.customer_type,
            c.credit_limit,
            c.current_balance,
            COUNT(DISTINCT o.order_id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_revenue,
            COALESCE(AVG(o.total_amount), 0) as avg_order_value,
            COUNT(DISTINCT i.invoice_id) as total_invoices,
            COALESCE(SUM(i.amount_paid), 0) as total_paid,
            COALESCE(SUM(i.amount_due), 0) as outstanding_balance,
            COUNT(DISTINCT p.payment_id) as total_payments,
            MAX(o.order_date) as last_order_date,
            MAX(p.payment_date) as last_payment_date
        FROM dbo.customers c
        LEFT JOIN dbo.orders o ON c.customer_id = o.customer_id
        LEFT JOIN dbo.invoices i ON c.customer_id = i.customer_id
        LEFT JOIN dbo.payments p ON c.customer_id = p.customer_id
        WHERE 1=1
        """
        params = []
        
        if customer_id:
            query += " AND c.customer_id = ?"
            params.append(customer_id)
        
        if start_date:
            query += " AND o.order_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND o.order_date <= ?"
            params.append(end_date)
        
        query += " GROUP BY c.customer_id, c.company_name, c.customer_type, c.credit_limit, c.current_balance"
        query += " ORDER BY total_revenue DESC"
        
        return execute_query(query, params)
    
    @staticmethod
    def get_inventory_status_report():
        """Get comprehensive inventory status across all warehouses with reorder alerts"""
        query = """
        SELECT 
            p.product_id,
            p.product_code,
            p.product_name,
            p.category,
            p.unit_price,
            w.warehouse_id,
            w.warehouse_name,
            i.quantity_on_hand,
            i.quantity_reserved,
            i.quantity_available,
            p.reorder_level,
            p.reorder_quantity,
            CASE 
                WHEN i.quantity_available <= p.reorder_level THEN 'REORDER_NEEDED'
                WHEN i.quantity_available <= (p.reorder_level * 1.5) THEN 'LOW_STOCK'
                ELSE 'ADEQUATE'
            END as stock_status,
            s.supplier_name,
            s.supplier_code,
            i.last_stock_check,
            i.last_restock_date
        FROM dbo.products p
        LEFT JOIN dbo.inventory i ON p.product_id = i.product_id
        LEFT JOIN dbo.warehouses w ON i.warehouse_id = w.warehouse_id
        LEFT JOIN dbo.suppliers s ON p.supplier_id = s.supplier_id
        WHERE p.is_active = 1
        ORDER BY 
            CASE 
                WHEN i.quantity_available <= p.reorder_level THEN 1
                WHEN i.quantity_available <= (p.reorder_level * 1.5) THEN 2
                ELSE 3
            END,
            p.product_name
        """
        return execute_query(query)
    
    @staticmethod
    def get_sales_performance_by_period(period='month', start_date=None, end_date=None):
        """Get sales performance metrics grouped by time period"""
        date_format = {
            'day': "CONVERT(VARCHAR(10), o.order_date, 120)",
            'week': "DATEPART(YEAR, o.order_date) * 100 + DATEPART(WEEK, o.order_date)",
            'month': "FORMAT(o.order_date, 'yyyy-MM')",
            'quarter': "CONCAT(YEAR(o.order_date), '-Q', DATEPART(QUARTER, o.order_date))",
            'year': "YEAR(o.order_date)"
        }.get(period, "FORMAT(o.order_date, 'yyyy-MM')")
        
        query = f"""
        SELECT 
            {date_format} as period,
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(DISTINCT o.customer_id) as unique_customers,
            SUM(o.subtotal) as gross_revenue,
            SUM(o.discount_amount) as total_discounts,
            SUM(o.tax_amount) as total_tax,
            SUM(o.shipping_amount) as total_shipping,
            SUM(o.total_amount) as net_revenue,
            AVG(o.total_amount) as avg_order_value,
            COUNT(DISTINCT CASE WHEN o.order_status = 'cancelled' THEN o.order_id END) as cancelled_orders,
            SUM(CASE WHEN o.payment_status = 'paid' THEN o.total_amount ELSE 0 END) as paid_amount,
            SUM(CASE WHEN o.payment_status = 'unpaid' THEN o.total_amount ELSE 0 END) as unpaid_amount
        FROM dbo.orders o
        WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND o.order_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND o.order_date <= ?"
            params.append(end_date)
        
        query += f" GROUP BY {date_format}"
        query += " ORDER BY period DESC"
        
        return execute_query(query, params)
    
    @staticmethod
    def get_product_performance_analysis(top_n=20):
        """Get top performing products with sales metrics and profitability"""
        query = """
        SELECT TOP (?)
            p.product_id,
            p.product_code,
            p.product_name,
            p.category,
            p.unit_price,
            p.cost_price,
            COUNT(DISTINCT oi.order_id) as times_ordered,
            SUM(oi.quantity) as total_quantity_sold,
            SUM(oi.line_total) as total_revenue,
            AVG(oi.unit_price) as avg_selling_price,
            SUM(oi.quantity * p.cost_price) as total_cost,
            SUM(oi.line_total) - SUM(oi.quantity * p.cost_price) as gross_profit,
            CASE 
                WHEN SUM(oi.line_total) > 0 
                THEN ((SUM(oi.line_total) - SUM(oi.quantity * p.cost_price)) / SUM(oi.line_total)) * 100
                ELSE 0 
            END as profit_margin_pct,
            COUNT(DISTINCT o.customer_id) as unique_customers,
            MAX(o.order_date) as last_ordered_date
        FROM dbo.products p
        INNER JOIN dbo.order_items oi ON p.product_id = oi.product_id
        INNER JOIN dbo.orders o ON oi.order_id = o.order_id
        WHERE o.order_status NOT IN ('cancelled')
        GROUP BY p.product_id, p.product_code, p.product_name, p.category, p.unit_price, p.cost_price
        ORDER BY total_revenue DESC
        """
        return execute_query(query, [top_n])
    
    @staticmethod
    def get_order_fulfillment_metrics(start_date=None, end_date=None):
        """Get order fulfillment and shipping performance metrics"""
        query = """
        SELECT 
            o.order_status,
            COUNT(DISTINCT o.order_id) as order_count,
            AVG(DATEDIFF(day, o.order_date, o.shipped_date)) as avg_days_to_ship,
            AVG(DATEDIFF(day, o.order_date, s.actual_delivery)) as avg_days_to_deliver,
            COUNT(DISTINCT CASE WHEN s.actual_delivery <= s.estimated_delivery THEN s.shipment_id END) as on_time_deliveries,
            COUNT(DISTINCT CASE WHEN s.actual_delivery > s.estimated_delivery THEN s.shipment_id END) as late_deliveries,
            AVG(s.shipping_cost) as avg_shipping_cost,
            SUM(o.total_amount) as total_order_value,
            w.warehouse_name,
            w.warehouse_code
        FROM dbo.orders o
        LEFT JOIN dbo.shipments s ON o.order_id = s.order_id
        LEFT JOIN dbo.warehouses w ON o.warehouse_id = w.warehouse_id
        WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND o.order_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND o.order_date <= ?"
            params.append(end_date)
        
        query += """
        GROUP BY o.order_status, w.warehouse_name, w.warehouse_code
        ORDER BY order_count DESC
        """
        return execute_query(query, params)
    
    @staticmethod
    def get_customer_segmentation():
        """Segment customers by value and behavior"""
        query = """
        WITH CustomerMetrics AS (
            SELECT 
                c.customer_id,
                c.company_name,
                c.customer_type,
                COUNT(DISTINCT o.order_id) as order_count,
                COALESCE(SUM(o.total_amount), 0) as lifetime_value,
                COALESCE(AVG(o.total_amount), 0) as avg_order_value,
                MAX(o.order_date) as last_order_date,
                DATEDIFF(day, MAX(o.order_date), GETDATE()) as days_since_last_order,
                COALESCE(SUM(i.amount_due), 0) as outstanding_balance
            FROM dbo.customers c
            LEFT JOIN dbo.orders o ON c.customer_id = o.customer_id
            LEFT JOIN dbo.invoices i ON c.customer_id = i.customer_id AND i.invoice_status != 'paid'
            GROUP BY c.customer_id, c.company_name, c.customer_type
        )
        SELECT 
            customer_id,
            company_name,
            customer_type,
            order_count,
            lifetime_value,
            avg_order_value,
            last_order_date,
            days_since_last_order,
            outstanding_balance,
            CASE 
                WHEN lifetime_value >= 100000 THEN 'VIP'
                WHEN lifetime_value >= 50000 THEN 'High Value'
                WHEN lifetime_value >= 10000 THEN 'Medium Value'
                ELSE 'Low Value'
            END as value_segment,
            CASE 
                WHEN days_since_last_order <= 30 THEN 'Active'
                WHEN days_since_last_order <= 90 THEN 'At Risk'
                WHEN days_since_last_order <= 180 THEN 'Dormant'
                ELSE 'Inactive'
            END as activity_segment
        FROM CustomerMetrics
        ORDER BY lifetime_value DESC
        """
        return execute_query(query)
    
    @staticmethod
    def get_payment_collection_report():
        """Get accounts receivable and payment collection metrics"""
        query = """
        SELECT 
            c.customer_id,
            c.company_name,
            c.credit_limit,
            COUNT(DISTINCT i.invoice_id) as total_invoices,
            SUM(i.total_amount) as total_invoiced,
            SUM(i.amount_paid) as total_collected,
            SUM(i.amount_due) as total_outstanding,
            COUNT(DISTINCT CASE WHEN i.due_date < GETDATE() AND i.amount_due > 0 THEN i.invoice_id END) as overdue_invoices,
            SUM(CASE WHEN i.due_date < GETDATE() THEN i.amount_due ELSE 0 END) as overdue_amount,
            AVG(DATEDIFF(day, i.invoice_date, p.payment_date)) as avg_days_to_payment,
            MAX(i.due_date) as latest_due_date,
            CASE 
                WHEN SUM(CASE WHEN i.due_date < GETDATE() THEN i.amount_due ELSE 0 END) > c.credit_limit * 0.8 THEN 'CRITICAL'
                WHEN SUM(CASE WHEN i.due_date < GETDATE() THEN i.amount_due ELSE 0 END) > c.credit_limit * 0.5 THEN 'WARNING'
                ELSE 'GOOD'
            END as credit_status
        FROM dbo.customers c
        LEFT JOIN dbo.invoices i ON c.customer_id = i.customer_id
        LEFT JOIN dbo.payments p ON i.invoice_id = p.invoice_id
        GROUP BY c.customer_id, c.company_name, c.credit_limit
        HAVING SUM(i.amount_due) > 0
        ORDER BY total_outstanding DESC
        """
        return execute_query(query)
    
    @staticmethod
    def get_warehouse_utilization():
        """Get warehouse capacity and utilization metrics"""
        query = """
        SELECT 
            w.warehouse_id,
            w.warehouse_code,
            w.warehouse_name,
            w.location,
            w.capacity,
            COUNT(DISTINCT i.product_id) as unique_products,
            SUM(i.quantity_on_hand) as total_units_stored,
            SUM(i.quantity_reserved) as total_units_reserved,
            SUM(i.quantity_available) as total_units_available,
            CASE 
                WHEN w.capacity > 0 THEN (CAST(SUM(i.quantity_on_hand) AS FLOAT) / w.capacity) * 100
                ELSE 0 
            END as utilization_pct,
            COUNT(DISTINCT o.order_id) as orders_fulfilled,
            COUNT(DISTINCT s.shipment_id) as shipments_sent,
            u.first_name + ' ' + u.last_name as manager_name
        FROM dbo.warehouses w
        LEFT JOIN dbo.inventory i ON w.warehouse_id = i.warehouse_id
        LEFT JOIN dbo.orders o ON w.warehouse_id = o.warehouse_id
        LEFT JOIN dbo.shipments s ON w.warehouse_id = s.warehouse_id
        LEFT JOIN dbo.users u ON w.manager_user_id = u.user_id
        GROUP BY w.warehouse_id, w.warehouse_code, w.warehouse_name, w.location, 
                 w.capacity, u.first_name, u.last_name
        ORDER BY utilization_pct DESC
        """
        return execute_query(query)
    
    @staticmethod
    def get_activity_summary_by_user(start_date=None, end_date=None):
        """Get CRM activity summary by user with completion rates"""
        query = """
        SELECT 
            u.user_id,
            u.username,
            u.first_name + ' ' + u.last_name as full_name,
            u.role,
            a.activity_type,
            COUNT(*) as total_activities,
            COUNT(CASE WHEN a.status = 'completed' THEN 1 END) as completed_activities,
            COUNT(CASE WHEN a.status = 'pending' THEN 1 END) as pending_activities,
            COUNT(CASE WHEN a.status = 'cancelled' THEN 1 END) as cancelled_activities,
            CASE 
                WHEN COUNT(*) > 0 THEN (CAST(COUNT(CASE WHEN a.status = 'completed' THEN 1 END) AS FLOAT) / COUNT(*)) * 100
                ELSE 0 
            END as completion_rate_pct,
            AVG(DATEDIFF(day, a.activity_date, a.completed_date)) as avg_days_to_complete,
            COUNT(DISTINCT a.customer_id) as unique_customers_contacted
        FROM dbo.users u
        LEFT JOIN dbo.activities a ON u.user_id = a.assigned_user_id
        WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND a.activity_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND a.activity_date <= ?"
            params.append(end_date)
        
        query += """
        GROUP BY u.user_id, u.username, u.first_name, u.last_name, u.role, a.activity_type
        ORDER BY total_activities DESC
        """
        return execute_query(query, params)
    
    @staticmethod
    def get_supplier_performance():
        """Get supplier performance metrics and ratings"""
        query = """
        SELECT 
            s.supplier_id,
            s.supplier_code,
            s.supplier_name,
            s.rating,
            s.payment_terms,
            COUNT(DISTINCT p.product_id) as products_supplied,
            COUNT(DISTINCT i.inventory_id) as inventory_locations,
            SUM(i.quantity_on_hand) as total_units_in_stock,
            COUNT(DISTINCT oi.order_id) as orders_containing_products,
            SUM(oi.quantity) as total_units_sold,
            SUM(oi.line_total) as total_sales_value,
            AVG(p.unit_price - p.cost_price) as avg_profit_per_unit,
            MAX(i.last_restock_date) as last_restock_date
        FROM dbo.suppliers s
        LEFT JOIN dbo.products p ON s.supplier_id = p.supplier_id
        LEFT JOIN dbo.inventory i ON p.product_id = i.product_id
        LEFT JOIN dbo.order_items oi ON p.product_id = oi.product_id
        WHERE s.status = 'active'
        GROUP BY s.supplier_id, s.supplier_code, s.supplier_name, s.rating, s.payment_terms
        ORDER BY total_sales_value DESC
        """
        return execute_query(query)
    
    @staticmethod
    def get_revenue_forecast(months_ahead=3):
        """Get revenue forecast based on historical trends"""
        query = """
        WITH MonthlyRevenue AS (
            SELECT 
                FORMAT(order_date, 'yyyy-MM') as month,
                SUM(total_amount) as revenue,
                COUNT(DISTINCT order_id) as order_count,
                AVG(total_amount) as avg_order_value
            FROM dbo.orders
            WHERE order_status NOT IN ('cancelled')
                AND order_date >= DATEADD(MONTH, -12, GETDATE())
            GROUP BY FORMAT(order_date, 'yyyy-MM')
        )
        SELECT 
            month,
            revenue,
            order_count,
            avg_order_value,
            AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg_3month,
            (revenue - LAG(revenue) OVER (ORDER BY month)) / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100 as growth_rate_pct
        FROM MonthlyRevenue
        ORDER BY month DESC
        """
        return execute_query(query)
