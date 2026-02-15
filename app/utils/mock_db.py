"""
Mock Database Connection for Testing MSSQL Queries
Intercepts pyodbc calls and returns fake data matching MSSQL structure
"""
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


class MockCursor:
    """Mock cursor that simulates pyodbc cursor behavior"""
    
    def __init__(self):
        self.description = None
        self._results = []
        self._rowcount = 0
        self._last_query = None
        
    def execute(self, query, params=None):
        """Execute a query and return mock data based on query pattern"""
        self._last_query = query.lower()
        logger.debug(f"Mock executing query: {query[:100]}...")
        
        # Parse query to determine what data to return
        if 'select' in self._last_query:
            self._results = self._generate_mock_data(query, params)
            self._rowcount = len(self._results)
        elif 'insert' in self._last_query:
            self._rowcount = 1
            self._results = []
        elif 'update' in self._last_query:
            self._rowcount = 1
            self._results = []
        elif 'delete' in self._last_query:
            self._rowcount = 1
            self._results = []
        else:
            self._results = []
            self._rowcount = 0
            
        return self
    
    def executemany(self, query, params_list):
        """Execute query multiple times"""
        self._rowcount = len(params_list)
        return self
    
    def fetchone(self):
        """Fetch one row"""
        if self._results:
            return self._results[0]
        return None
    
    def fetchall(self):
        """Fetch all rows"""
        return self._results
    
    def close(self):
        """Close cursor"""
        pass
    
    @property
    def rowcount(self):
        """Return number of affected rows"""
        return self._rowcount
    
    def _generate_mock_data(self, query, params):
        """Generate mock data based on query pattern"""
        query_lower = query.lower()
        
        # Customer queries
        if 'from customers' in query_lower or 'from customer' in query_lower:
            return self._mock_customers(query_lower)
        
        # Product queries
        elif 'from products' in query_lower or 'from product' in query_lower:
            return self._mock_products(query_lower)
        
        # Order queries
        elif 'from orders' in query_lower or 'from order' in query_lower:
            return self._mock_orders(query_lower)
        
        # Invoice queries
        elif 'from invoices' in query_lower or 'from invoice' in query_lower:
            return self._mock_invoices(query_lower)
        
        # Payment queries
        elif 'from payments' in query_lower or 'from payment' in query_lower:
            return self._mock_payments(query_lower)
        
        # Inventory queries
        elif 'from inventory' in query_lower:
            return self._mock_inventory(query_lower)
        
        # Warehouse queries
        elif 'from warehouses' in query_lower or 'from warehouse' in query_lower:
            return self._mock_warehouses(query_lower)
        
        # Supplier queries
        elif 'from suppliers' in query_lower or 'from supplier' in query_lower:
            return self._mock_suppliers(query_lower)
        
        # Shipment queries
        elif 'from shipments' in query_lower or 'from shipment' in query_lower:
            return self._mock_shipments(query_lower)
        
        # User/Activity queries
        elif 'from users' in query_lower or 'from activities' in query_lower:
            return self._mock_users_activities(query_lower)
        
        # Analytics/Aggregation queries
        elif any(keyword in query_lower for keyword in ['count(*)', 'sum(', 'avg(', 'group by']):
            return self._mock_analytics(query_lower)
        
        # Default empty result
        return []
    
    def _mock_customers(self, query):
        """Generate mock customer data"""
        customers = [
            (1, 'CUST001', 'Acme Corp', 'corporate', 'John Doe', 'john@acme.com', 
             '555-0100', '123 Main St', 'active', 50000.00, datetime.now() - timedelta(days=365)),
            (2, 'CUST002', 'Tech Solutions Inc', 'corporate', 'Jane Smith', 'jane@techsol.com',
             '555-0200', '456 Oak Ave', 'active', 75000.00, datetime.now() - timedelta(days=300)),
            (3, 'CUST003', 'Small Business LLC', 'small_business', 'Bob Johnson', 'bob@smallbiz.com',
             '555-0300', '789 Pine Rd', 'active', 25000.00, datetime.now() - timedelta(days=180)),
        ]
        
        # Set column descriptions
        self.description = [
            ('customer_id',), ('customer_code',), ('company_name',), ('customer_type',),
            ('contact_name',), ('email',), ('phone',), ('address',), ('status',),
            ('credit_limit',), ('created_at',)
        ]
        
        if 'where' in query and 'customer_id' in query:
            return [customers[0]]
        
        return customers
    
    def _mock_products(self, query):
        """Generate mock product data"""
        products = [
            (1, 'WGT-A-001', 'Widget A', 'Electronics', 29.99, 15.00, 'active', datetime.now()),
            (2, 'WGT-B-002', 'Widget B', 'Electronics', 49.99, 25.00, 'active', datetime.now()),
            (3, 'WGT-C-003', 'Widget C', 'Hardware', 39.99, 20.00, 'active', datetime.now()),
        ]
        
        self.description = [
            ('product_id',), ('product_code',), ('product_name',), ('category',),
            ('unit_price',), ('cost_price',), ('status',), ('created_at',)
        ]
        
        if 'where' in query and 'product_id' in query:
            return [products[0]]
        
        return products
    
    def _mock_orders(self, query):
        """Generate mock order data"""
        orders = [
            (1, 1, datetime.now() - timedelta(days=5), 'completed', 299.99, 10.00, 25.00, 15.00, 329.99),
            (2, 2, datetime.now() - timedelta(days=3), 'pending', 149.99, 5.00, 12.00, 10.00, 166.99),
            (3, 1, datetime.now() - timedelta(days=1), 'processing', 499.99, 20.00, 40.00, 20.00, 539.99),
        ]
        
        self.description = [
            ('order_id',), ('customer_id',), ('order_date',), ('status',),
            ('subtotal',), ('discount',), ('tax',), ('shipping',), ('total',)
        ]
        
        if 'where' in query and 'order_id' in query:
            return [orders[0]]
        
        return orders
    
    def _mock_invoices(self, query):
        """Generate mock invoice data"""
        invoices = [
            (1, 1, 1, datetime.now() - timedelta(days=5), datetime.now() + timedelta(days=25),
             329.99, 329.99, 0.00, 'paid'),
            (2, 2, 2, datetime.now() - timedelta(days=3), datetime.now() + timedelta(days=27),
             166.99, 100.00, 66.99, 'partial'),
            (3, 1, 3, datetime.now() - timedelta(days=1), datetime.now() + timedelta(days=29),
             539.99, 0.00, 539.99, 'unpaid'),
        ]
        
        self.description = [
            ('invoice_id',), ('customer_id',), ('order_id',), ('invoice_date',),
            ('due_date',), ('total_amount',), ('paid_amount',), ('balance',), ('status',)
        ]
        
        return invoices
    
    def _mock_payments(self, query):
        """Generate mock payment data"""
        payments = [
            (1, 1, 1, datetime.now() - timedelta(days=4), 329.99, 'credit_card', 'completed', 'TXN001'),
            (2, 2, 2, datetime.now() - timedelta(days=2), 100.00, 'bank_transfer', 'completed', 'TXN002'),
        ]
        
        self.description = [
            ('payment_id',), ('customer_id',), ('invoice_id',), ('payment_date',),
            ('amount',), ('payment_method',), ('status',), ('transaction_id',)
        ]
        
        return payments
    
    def _mock_inventory(self, query):
        """Generate mock inventory data"""
        inventory = [
            (1, 1, 1, 100, 20, 80, 50, 200, datetime.now()),
            (2, 2, 1, 35, 10, 25, 50, 150, datetime.now()),
            (3, 3, 1, 150, 30, 120, 40, 180, datetime.now()),
        ]
        
        self.description = [
            ('inventory_id',), ('product_id',), ('warehouse_id',), ('quantity_on_hand',),
            ('quantity_reserved',), ('quantity_available',), ('reorder_level',),
            ('reorder_quantity',), ('last_updated',)
        ]
        
        return inventory
    
    def _mock_warehouses(self, query):
        """Generate mock warehouse data"""
        warehouses = [
            (1, 'WH-001', 'Main Warehouse', '100 Storage Ln', 10000, 6500, 'active'),
            (2, 'WH-002', 'East Warehouse', '200 Depot St', 8000, 5000, 'active'),
        ]
        
        self.description = [
            ('warehouse_id',), ('warehouse_code',), ('warehouse_name',), ('address',),
            ('capacity',), ('current_stock',), ('status',)
        ]
        
        return warehouses
    
    def _mock_suppliers(self, query):
        """Generate mock supplier data"""
        suppliers = [
            (1, 'SUP-001', 'Tech Supplies Co', 'Alice Brown', 'alice@techsup.com',
             '555-1000', '500 Supply Ave', 'active', datetime.now() - timedelta(days=500)),
            (2, 'SUP-002', 'Hardware Direct', 'Charlie Davis', 'charlie@hwdirect.com',
             '555-2000', '600 Parts Blvd', 'active', datetime.now() - timedelta(days=400)),
        ]
        
        self.description = [
            ('supplier_id',), ('supplier_code',), ('supplier_name',), ('contact_name',),
            ('email',), ('phone',), ('address',), ('status',), ('created_at',)
        ]
        
        return suppliers
    
    def _mock_shipments(self, query):
        """Generate mock shipment data"""
        shipments = [
            (1, 1, 1, datetime.now() - timedelta(days=4), datetime.now() - timedelta(days=1),
             'FedEx', 'TRACK001', 'delivered', datetime.now() - timedelta(days=1)),
            (2, 2, 1, datetime.now() - timedelta(days=2), datetime.now() + timedelta(days=2),
             'UPS', 'TRACK002', 'in_transit', None),
        ]
        
        self.description = [
            ('shipment_id',), ('order_id',), ('warehouse_id',), ('ship_date',),
            ('estimated_delivery',), ('carrier',), ('tracking_number',), ('status',),
            ('actual_delivery',)
        ]
        
        return shipments
    
    def _mock_users_activities(self, query):
        """Generate mock user/activity data"""
        if 'from users' in query:
            users = [
                (1, 'admin', 'admin@company.com', 'Admin User', 'admin', 'active', datetime.now()),
                (2, 'sales1', 'sales1@company.com', 'Sales Rep 1', 'sales', 'active', datetime.now()),
            ]
            self.description = [
                ('user_id',), ('username',), ('email',), ('full_name',),
                ('role',), ('status',), ('created_at',)
            ]
            return users
        else:
            activities = [
                (1, 1, 1, 'customer', 'created', datetime.now() - timedelta(days=10)),
                (2, 2, 1, 'order', 'updated', datetime.now() - timedelta(days=5)),
            ]
            self.description = [
                ('activity_id',), ('user_id',), ('entity_id',), ('entity_type',),
                ('action',), ('created_at',)
            ]
            return activities
    
    def _mock_analytics(self, query):
        """Generate mock analytics/aggregation data"""
        # Customer segmentation
        if 'lifetime_value' in query or 'value_segment' in query:
            data = [
                (1, 'Acme Corp', 125, 350000.00, 2800.00, 4, 5000.00, 'VIP', 'Active'),
                (2, 'Tech Solutions Inc', 85, 185000.00, 2176.47, 21, 2500.00, 'VIP', 'Active'),
                (3, 'Small Business LLC', 12, 15000.00, 1250.00, 77, 0.00, 'Medium Value', 'At Risk'),
            ]
            self.description = [
                ('customer_id',), ('company_name',), ('order_count',), ('lifetime_value',),
                ('avg_order_value',), ('days_since_last_order',), ('outstanding_balance',),
                ('value_segment',), ('activity_segment',)
            ]
            return data
        
        # Sales performance
        elif 'total_orders' in query or 'total_revenue' in query:
            data = [
                ('2024-02', 156, 89, 425000.00, 12500.00, 35000.00, 7800.00, 455300.00, 2918.59),
                ('2024-01', 142, 82, 385000.00, 11000.00, 31500.00, 7100.00, 412600.00, 2905.63),
            ]
            self.description = [
                ('period',), ('total_orders',), ('unique_customers',), ('gross_revenue',),
                ('total_discounts',), ('total_tax',), ('total_shipping',), ('net_revenue',),
                ('avg_order_value',)
            ]
            return data
        
        # Product performance
        elif 'total_quantity_sold' in query or 'profit_margin' in query:
            data = [
                (1, 'WGT-A-001', 'Widget A', 145, 580, 17394.20, 8700.00, 8694.20, 50.00),
                (2, 'WGT-B-002', 'Widget B', 98, 392, 19596.08, 9800.00, 9796.08, 50.00),
            ]
            self.description = [
                ('product_id',), ('product_code',), ('product_name',), ('times_ordered',),
                ('total_quantity_sold',), ('total_revenue',), ('total_cost',),
                ('gross_profit',), ('profit_margin_pct',)
            ]
            return data
        
        # Simple count
        elif 'count(*)' in query:
            return [(random.randint(10, 100),)]
        
        # Default aggregation
        return [(0,)]


class MockConnection:
    """Mock connection that simulates pyodbc connection behavior"""
    
    def __init__(self, connection_string, **kwargs):
        self.connection_string = connection_string
        self.autocommit = False
        self.closed = False
        logger.info(f"Mock database connection created")
    
    def cursor(self):
        """Return a mock cursor"""
        return MockCursor()
    
    def commit(self):
        """Commit transaction"""
        logger.debug("Mock commit")
        pass
    
    def rollback(self):
        """Rollback transaction"""
        logger.debug("Mock rollback")
        pass
    
    def close(self):
        """Close connection"""
        self.closed = True
        logger.debug("Mock connection closed")


def mock_connect(connection_string, **kwargs):
    """Mock pyodbc.connect function"""
    return MockConnection(connection_string, **kwargs)
