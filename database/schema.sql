-- =====================================================
-- CRM & Inventory Management Database Schema
-- MSSQL Server Database
-- =====================================================

-- Drop existing tables if they exist (in reverse order of dependencies)
IF OBJECT_ID('dbo.audit_logs', 'U') IS NOT NULL DROP TABLE dbo.audit_logs;
IF OBJECT_ID('dbo.activities', 'U') IS NOT NULL DROP TABLE dbo.activities;
IF OBJECT_ID('dbo.payments', 'U') IS NOT NULL DROP TABLE dbo.payments;
IF OBJECT_ID('dbo.invoices', 'U') IS NOT NULL DROP TABLE dbo.invoices;
IF OBJECT_ID('dbo.shipments', 'U') IS NOT NULL DROP TABLE dbo.shipments;
IF OBJECT_ID('dbo.order_items', 'U') IS NOT NULL DROP TABLE dbo.order_items;
IF OBJECT_ID('dbo.orders', 'U') IS NOT NULL DROP TABLE dbo.orders;
IF OBJECT_ID('dbo.inventory', 'U') IS NOT NULL DROP TABLE dbo.inventory;
IF OBJECT_ID('dbo.products', 'U') IS NOT NULL DROP TABLE dbo.products;
IF OBJECT_ID('dbo.suppliers', 'U') IS NOT NULL DROP TABLE dbo.suppliers;
IF OBJECT_ID('dbo.warehouses', 'U') IS NOT NULL DROP TABLE dbo.warehouses;
IF OBJECT_ID('dbo.contacts', 'U') IS NOT NULL DROP TABLE dbo.contacts;
IF OBJECT_ID('dbo.accounts', 'U') IS NOT NULL DROP TABLE dbo.accounts;
IF OBJECT_ID('dbo.customers', 'U') IS NOT NULL DROP TABLE dbo.customers;
IF OBJECT_ID('dbo.users', 'U') IS NOT NULL DROP TABLE dbo.users;

-- =====================================================
-- Users Table
-- =====================================================
CREATE TABLE dbo.users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(100) NOT NULL UNIQUE,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    first_name NVARCHAR(100),
    last_name NVARCHAR(100),
    role NVARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BIT NOT NULL DEFAULT 1,
    last_login DATETIME2,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    INDEX idx_users_email (email),
    INDEX idx_users_username (username),
    INDEX idx_users_role (role)
);

-- =====================================================
-- Customers Table
-- =====================================================
CREATE TABLE dbo.customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_code NVARCHAR(50) NOT NULL UNIQUE,
    company_name NVARCHAR(255) NOT NULL,
    customer_type NVARCHAR(50) NOT NULL, -- 'individual', 'business', 'enterprise'
    industry NVARCHAR(100),
    tax_id NVARCHAR(50),
    credit_limit DECIMAL(15,2) DEFAULT 0.00,
    current_balance DECIMAL(15,2) DEFAULT 0.00,
    payment_terms INT DEFAULT 30, -- days
    status NVARCHAR(50) NOT NULL DEFAULT 'active',
    billing_address NVARCHAR(500),
    shipping_address NVARCHAR(500),
    phone NVARCHAR(50),
    email NVARCHAR(255),
    website NVARCHAR(255),
    assigned_user_id INT,
    created_by INT,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (assigned_user_id) REFERENCES dbo.users(user_id),
    FOREIGN KEY (created_by) REFERENCES dbo.users(user_id),
    INDEX idx_customers_code (customer_code),
    INDEX idx_customers_type (customer_type),
    INDEX idx_customers_status (status),
    INDEX idx_customers_assigned (assigned_user_id)
);

-- =====================================================
-- Accounts Table (Sub-accounts under customers)
-- =====================================================
CREATE TABLE dbo.accounts (
    account_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    account_number NVARCHAR(50) NOT NULL UNIQUE,
    account_name NVARCHAR(255) NOT NULL,
    account_type NVARCHAR(50) NOT NULL, -- 'primary', 'secondary', 'billing'
    status NVARCHAR(50) NOT NULL DEFAULT 'active',
    billing_address NVARCHAR(500),
    shipping_address NVARCHAR(500),
    phone NVARCHAR(50),
    email NVARCHAR(255),
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id) ON DELETE CASCADE,
    INDEX idx_accounts_customer (customer_id),
    INDEX idx_accounts_number (account_number),
    INDEX idx_accounts_status (status)
);

-- =====================================================
-- Contacts Table
-- =====================================================
CREATE TABLE dbo.contacts (
    contact_id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    account_id INT,
    first_name NVARCHAR(100) NOT NULL,
    last_name NVARCHAR(100) NOT NULL,
    title NVARCHAR(100),
    department NVARCHAR(100),
    email NVARCHAR(255),
    phone NVARCHAR(50),
    mobile NVARCHAR(50),
    is_primary BIT NOT NULL DEFAULT 0,
    status NVARCHAR(50) NOT NULL DEFAULT 'active',
    notes NVARCHAR(MAX),
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES dbo.accounts(account_id),
    INDEX idx_contacts_customer (customer_id),
    INDEX idx_contacts_account (account_id),
    INDEX idx_contacts_email (email),
    INDEX idx_contacts_primary (is_primary)
);

-- =====================================================
-- Warehouses Table
-- =====================================================
CREATE TABLE dbo.warehouses (
    warehouse_id INT IDENTITY(1,1) PRIMARY KEY,
    warehouse_code NVARCHAR(50) NOT NULL UNIQUE,
    warehouse_name NVARCHAR(255) NOT NULL,
    location NVARCHAR(255),
    address NVARCHAR(500),
    city NVARCHAR(100),
    state NVARCHAR(100),
    country NVARCHAR(100),
    postal_code NVARCHAR(20),
    phone NVARCHAR(50),
    manager_user_id INT,
    capacity INT,
    status NVARCHAR(50) NOT NULL DEFAULT 'active',
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (manager_user_id) REFERENCES dbo.users(user_id),
    INDEX idx_warehouses_code (warehouse_code),
    INDEX idx_warehouses_status (status)
);

-- =====================================================
-- Suppliers Table
-- =====================================================
CREATE TABLE dbo.suppliers (
    supplier_id INT IDENTITY(1,1) PRIMARY KEY,
    supplier_code NVARCHAR(50) NOT NULL UNIQUE,
    supplier_name NVARCHAR(255) NOT NULL,
    contact_person NVARCHAR(255),
    email NVARCHAR(255),
    phone NVARCHAR(50),
    address NVARCHAR(500),
    city NVARCHAR(100),
    state NVARCHAR(100),
    country NVARCHAR(100),
    postal_code NVARCHAR(20),
    payment_terms INT DEFAULT 30,
    tax_id NVARCHAR(50),
    rating DECIMAL(3,2), -- 0.00 to 5.00
    status NVARCHAR(50) NOT NULL DEFAULT 'active',
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    INDEX idx_suppliers_code (supplier_code),
    INDEX idx_suppliers_status (status)
);

-- =====================================================
-- Products Table
-- =====================================================
CREATE TABLE dbo.products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    product_code NVARCHAR(100) NOT NULL UNIQUE,
    product_name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    category NVARCHAR(100),
    subcategory NVARCHAR(100),
    brand NVARCHAR(100),
    unit_of_measure NVARCHAR(50) NOT NULL DEFAULT 'each',
    unit_price DECIMAL(15,2) NOT NULL,
    cost_price DECIMAL(15,2),
    weight DECIMAL(10,2),
    dimensions NVARCHAR(100),
    supplier_id INT,
    reorder_level INT DEFAULT 10,
    reorder_quantity INT DEFAULT 50,
    is_active BIT NOT NULL DEFAULT 1,
    is_serialized BIT NOT NULL DEFAULT 0,
    tax_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (supplier_id) REFERENCES dbo.suppliers(supplier_id),
    INDEX idx_products_code (product_code),
    INDEX idx_products_category (category),
    INDEX idx_products_supplier (supplier_id),
    INDEX idx_products_active (is_active)
);

-- =====================================================
-- Inventory Table
-- =====================================================
CREATE TABLE dbo.inventory (
    inventory_id INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity_on_hand INT NOT NULL DEFAULT 0,
    quantity_reserved INT NOT NULL DEFAULT 0,
    quantity_available AS (quantity_on_hand - quantity_reserved) PERSISTED,
    bin_location NVARCHAR(50),
    last_stock_check DATETIME2,
    last_restock_date DATETIME2,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (product_id) REFERENCES dbo.products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES dbo.warehouses(warehouse_id),
    UNIQUE (product_id, warehouse_id),
    INDEX idx_inventory_product (product_id),
    INDEX idx_inventory_warehouse (warehouse_id),
    INDEX idx_inventory_available (quantity_available)
);

-- =====================================================
-- Orders Table
-- =====================================================
CREATE TABLE dbo.orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    order_number NVARCHAR(50) NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    account_id INT,
    order_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    required_date DATETIME2,
    shipped_date DATETIME2,
    order_status NVARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, confirmed, processing, shipped, delivered, cancelled
    payment_status NVARCHAR(50) NOT NULL DEFAULT 'unpaid', -- unpaid, partial, paid, refunded
    subtotal DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    shipping_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    shipping_address NVARCHAR(500),
    billing_address NVARCHAR(500),
    warehouse_id INT,
    assigned_user_id INT,
    notes NVARCHAR(MAX),
    created_by INT,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES dbo.accounts(account_id),
    FOREIGN KEY (warehouse_id) REFERENCES dbo.warehouses(warehouse_id),
    FOREIGN KEY (assigned_user_id) REFERENCES dbo.users(user_id),
    FOREIGN KEY (created_by) REFERENCES dbo.users(user_id),
    INDEX idx_orders_number (order_number),
    INDEX idx_orders_customer (customer_id),
    INDEX idx_orders_status (order_status),
    INDEX idx_orders_payment (payment_status),
    INDEX idx_orders_date (order_date)
);

-- =====================================================
-- Order Items Table
-- =====================================================
CREATE TABLE dbo.order_items (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0.00,
    tax_rate DECIMAL(5,2) DEFAULT 0.00,
    line_total DECIMAL(15,2) NOT NULL,
    notes NVARCHAR(500),
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (order_id) REFERENCES dbo.orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES dbo.products(product_id),
    INDEX idx_order_items_order (order_id),
    INDEX idx_order_items_product (product_id)
);

-- =====================================================
-- Shipments Table
-- =====================================================
CREATE TABLE dbo.shipments (
    shipment_id INT IDENTITY(1,1) PRIMARY KEY,
    shipment_number NVARCHAR(50) NOT NULL UNIQUE,
    order_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    carrier NVARCHAR(100),
    tracking_number NVARCHAR(100),
    shipment_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    estimated_delivery DATETIME2,
    actual_delivery DATETIME2,
    shipment_status NVARCHAR(50) NOT NULL DEFAULT 'preparing', -- preparing, shipped, in_transit, delivered, returned
    shipping_cost DECIMAL(15,2),
    weight DECIMAL(10,2),
    notes NVARCHAR(MAX),
    created_by INT,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (order_id) REFERENCES dbo.orders(order_id),
    FOREIGN KEY (warehouse_id) REFERENCES dbo.warehouses(warehouse_id),
    FOREIGN KEY (created_by) REFERENCES dbo.users(user_id),
    INDEX idx_shipments_number (shipment_number),
    INDEX idx_shipments_order (order_id),
    INDEX idx_shipments_status (shipment_status),
    INDEX idx_shipments_tracking (tracking_number)
);

-- =====================================================
-- Invoices Table
-- =====================================================
CREATE TABLE dbo.invoices (
    invoice_id INT IDENTITY(1,1) PRIMARY KEY,
    invoice_number NVARCHAR(50) NOT NULL UNIQUE,
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    invoice_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    due_date DATETIME2 NOT NULL,
    subtotal DECIMAL(15,2) NOT NULL,
    tax_amount DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(15,2) NOT NULL,
    amount_paid DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    amount_due AS (total_amount - amount_paid) PERSISTED,
    invoice_status NVARCHAR(50) NOT NULL DEFAULT 'draft', -- draft, sent, partial, paid, overdue, cancelled
    payment_terms INT DEFAULT 30,
    notes NVARCHAR(MAX),
    created_by INT,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (order_id) REFERENCES dbo.orders(order_id),
    FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id),
    FOREIGN KEY (created_by) REFERENCES dbo.users(user_id),
    INDEX idx_invoices_number (invoice_number),
    INDEX idx_invoices_order (order_id),
    INDEX idx_invoices_customer (customer_id),
    INDEX idx_invoices_status (invoice_status),
    INDEX idx_invoices_due_date (due_date)
);

-- =====================================================
-- Payments Table
-- =====================================================
CREATE TABLE dbo.payments (
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    payment_number NVARCHAR(50) NOT NULL UNIQUE,
    invoice_id INT NOT NULL,
    customer_id INT NOT NULL,
    payment_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    payment_method NVARCHAR(50) NOT NULL, -- cash, check, credit_card, bank_transfer, paypal
    payment_amount DECIMAL(15,2) NOT NULL,
    reference_number NVARCHAR(100),
    payment_status NVARCHAR(50) NOT NULL DEFAULT 'completed', -- pending, completed, failed, refunded
    notes NVARCHAR(MAX),
    processed_by INT,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (invoice_id) REFERENCES dbo.invoices(invoice_id),
    FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id),
    FOREIGN KEY (processed_by) REFERENCES dbo.users(user_id),
    INDEX idx_payments_number (payment_number),
    INDEX idx_payments_invoice (invoice_id),
    INDEX idx_payments_customer (customer_id),
    INDEX idx_payments_date (payment_date),
    INDEX idx_payments_status (payment_status)
);

-- =====================================================
-- Activities Table (CRM Activities)
-- =====================================================
CREATE TABLE dbo.activities (
    activity_id INT IDENTITY(1,1) PRIMARY KEY,
    activity_type NVARCHAR(50) NOT NULL, -- call, email, meeting, task, note
    subject NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    customer_id INT,
    contact_id INT,
    order_id INT,
    activity_date DATETIME2 NOT NULL DEFAULT GETDATE(),
    due_date DATETIME2,
    completed_date DATETIME2,
    status NVARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, in_progress, completed, cancelled
    priority NVARCHAR(50) DEFAULT 'medium', -- low, medium, high, urgent
    assigned_user_id INT,
    created_by INT,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (customer_id) REFERENCES dbo.customers(customer_id),
    FOREIGN KEY (contact_id) REFERENCES dbo.contacts(contact_id),
    FOREIGN KEY (order_id) REFERENCES dbo.orders(order_id),
    FOREIGN KEY (assigned_user_id) REFERENCES dbo.users(user_id),
    FOREIGN KEY (created_by) REFERENCES dbo.users(user_id),
    INDEX idx_activities_type (activity_type),
    INDEX idx_activities_customer (customer_id),
    INDEX idx_activities_contact (contact_id),
    INDEX idx_activities_status (status),
    INDEX idx_activities_assigned (assigned_user_id),
    INDEX idx_activities_date (activity_date)
);

-- =====================================================
-- Audit Logs Table
-- =====================================================
CREATE TABLE dbo.audit_logs (
    audit_id INT IDENTITY(1,1) PRIMARY KEY,
    table_name NVARCHAR(100) NOT NULL,
    record_id INT NOT NULL,
    action NVARCHAR(50) NOT NULL, -- INSERT, UPDATE, DELETE
    old_values NVARCHAR(MAX),
    new_values NVARCHAR(MAX),
    changed_by INT,
    changed_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    ip_address NVARCHAR(50),
    user_agent NVARCHAR(500),
    FOREIGN KEY (changed_by) REFERENCES dbo.users(user_id),
    INDEX idx_audit_table (table_name),
    INDEX idx_audit_record (record_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_date (changed_at),
    INDEX idx_audit_user (changed_by)
);

-- =====================================================
-- Insert Sample Data
-- =====================================================

-- Sample Users
INSERT INTO dbo.users (username, email, password_hash, first_name, last_name, role) VALUES
('admin', 'admin@crm.com', 'hashed_password_1', 'Admin', 'User', 'admin'),
('john.doe', 'john.doe@crm.com', 'hashed_password_2', 'John', 'Doe', 'sales_manager'),
('jane.smith', 'jane.smith@crm.com', 'hashed_password_3', 'Jane', 'Smith', 'sales_rep'),
('bob.wilson', 'bob.wilson@crm.com', 'hashed_password_4', 'Bob', 'Wilson', 'warehouse_manager');

-- Sample Warehouses
INSERT INTO dbo.warehouses (warehouse_code, warehouse_name, location, address, city, state, country, postal_code, manager_user_id) VALUES
('WH001', 'Main Warehouse', 'North District', '123 Industrial Blvd', 'New York', 'NY', 'USA', '10001', 4),
('WH002', 'West Coast Distribution', 'West District', '456 Commerce Ave', 'Los Angeles', 'CA', 'USA', '90001', 4);

-- Sample Suppliers
INSERT INTO dbo.suppliers (supplier_code, supplier_name, contact_person, email, phone, city, country) VALUES
('SUP001', 'Tech Components Inc', 'Michael Brown', 'michael@techcomp.com', '555-0101', 'San Francisco', 'USA'),
('SUP002', 'Global Electronics Ltd', 'Sarah Johnson', 'sarah@globalelec.com', '555-0102', 'Seattle', 'USA');

-- Sample Customers
INSERT INTO dbo.customers (customer_code, company_name, customer_type, industry, credit_limit, payment_terms, status, assigned_user_id, created_by) VALUES
('CUST001', 'Acme Corporation', 'enterprise', 'Manufacturing', 100000.00, 60, 'active', 2, 1),
('CUST002', 'TechStart Solutions', 'business', 'Technology', 50000.00, 30, 'active', 3, 1),
('CUST003', 'Retail Plus Inc', 'business', 'Retail', 75000.00, 45, 'active', 2, 1);

PRINT 'Database schema created successfully with sample data';
