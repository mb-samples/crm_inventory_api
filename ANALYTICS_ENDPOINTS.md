# Analytics & Reporting API Endpoints

## Overview

Complete set of advanced analytics and reporting endpoints covering all operations from `advanced_data_layer.py`.

## 🎯 Available Analytics Endpoints

### 1. Customer Analytics
**GET** `/api/analytics/customers`

Comprehensive customer analytics with order history, revenue, and payment statistics.

**Query Parameters:**
- `customer_id` (integer, optional): Filter by specific customer
- `start_date` (date, optional): Start date for analysis
- `end_date` (date, optional): End date for analysis

**Response Fields:**
- `customer_id`, `company_name`, `customer_type`
- `total_orders`, `total_revenue`, `avg_order_value`
- `total_invoices`, `total_paid`, `outstanding_balance`
- `last_order_date`, `last_payment_date`

**Example:**
```bash
curl "http://localhost:5000/api/analytics/customers?customer_id=1"
```

---

### 2. Inventory Status Report
**GET** `/api/analytics/inventory-status`

Comprehensive inventory status across all warehouses with reorder alerts.

**Response Fields:**
- `product_id`, `product_name`, `warehouse_name`
- `quantity_on_hand`, `quantity_reserved`, `quantity_available`
- `reorder_level`, `stock_status` (REORDER_NEEDED, LOW_STOCK, ADEQUATE)
- `supplier_name`, `last_stock_check`

**Example:**
```bash
curl http://localhost:5000/api/analytics/inventory-status
```

---

### 3. Sales Performance by Period
**GET** `/api/analytics/sales-performance`

Sales performance metrics grouped by time period.

**Query Parameters:**
- `period` (string, optional): Time grouping - `day`, `week`, `month`, `quarter`, `year` (default: month)
- `start_date` (date, optional): Start date
- `end_date` (date, optional): End date

**Response Fields:**
- `period`, `total_orders`, `unique_customers`
- `gross_revenue`, `total_discounts`, `net_revenue`
- `avg_order_value`, `cancelled_orders`
- `paid_amount`, `unpaid_amount`

**Example:**
```bash
curl "http://localhost:5000/api/analytics/sales-performance?period=quarter"
```

---

### 4. Product Performance Analysis
**GET** `/api/analytics/product-performance`

Top performing products with sales metrics and profitability.

**Query Parameters:**
- `top_n` (integer, optional): Number of top products (default: 20)

**Response Fields:**
- `product_id`, `product_name`, `category`
- `times_ordered`, `total_quantity_sold`, `total_revenue`
- `total_cost`, `gross_profit`, `profit_margin_pct`
- `unique_customers`, `last_ordered_date`

**Example:**
```bash
curl "http://localhost:5000/api/analytics/product-performance?top_n=10"
```

---

### 5. Order Fulfillment Metrics
**GET** `/api/analytics/order-fulfillment`

Order fulfillment and shipping performance metrics.

**Query Parameters:**
- `start_date` (date, optional): Start date
- `end_date` (date, optional): End date

**Response Fields:**
- `order_status`, `order_count`
- `avg_days_to_ship`, `avg_days_to_deliver`
- `on_time_deliveries`, `late_deliveries`
- `avg_shipping_cost`, `warehouse_name`

**Example:**
```bash
curl http://localhost:5000/api/analytics/order-fulfillment
```

---

### 6. Customer Segmentation
**GET** `/api/analytics/customer-segmentation`

Customers segmented by value and activity behavior.

**Response Fields:**
- `customer_id`, `company_name`, `customer_type`
- `order_count`, `lifetime_value`, `avg_order_value`
- `days_since_last_order`, `outstanding_balance`
- `value_segment` (VIP, High Value, Medium Value, Low Value)
- `activity_segment` (Active, At Risk, Dormant, Inactive)

**Example:**
```bash
curl http://localhost:5000/api/analytics/customer-segmentation
```

---

### 7. Payment Collection Report
**GET** `/api/analytics/payment-collection`

Accounts receivable and payment collection metrics.

**Response Fields:**
- `customer_id`, `company_name`, `credit_limit`
- `total_invoices`, `total_invoiced`, `total_collected`
- `total_outstanding`, `overdue_invoices`, `overdue_amount`
- `avg_days_to_payment`, `credit_status` (GOOD, WARNING, CRITICAL)

**Example:**
```bash
curl http://localhost:5000/api/analytics/payment-collection
```

---

### 8. Warehouse Utilization
**GET** `/api/analytics/warehouse-utilization`

Warehouse capacity and utilization metrics.

**Response Fields:**
- `warehouse_id`, `warehouse_name`, `location`
- `capacity`, `unique_products`, `total_units_stored`
- `utilization_pct`, `orders_fulfilled`, `shipments_sent`
- `manager_name`

**Example:**
```bash
curl http://localhost:5000/api/analytics/warehouse-utilization
```

---

### 9. User Activity Summary
**GET** `/api/analytics/user-activity`

CRM activity summary by user with completion rates.

**Query Parameters:**
- `start_date` (date, optional): Start date
- `end_date` (date, optional): End date

**Response Fields:**
- `user_id`, `username`, `full_name`, `role`
- `activity_type`, `total_activities`
- `completed_activities`, `pending_activities`
- `completion_rate_pct`, `avg_days_to_complete`
- `unique_customers_contacted`

**Example:**
```bash
curl http://localhost:5000/api/analytics/user-activity
```

---

### 10. Supplier Performance
**GET** `/api/analytics/supplier-performance`

Supplier performance metrics and ratings.

**Response Fields:**
- `supplier_id`, `supplier_name`, `rating`
- `products_supplied`, `inventory_locations`
- `total_units_in_stock`, `total_units_sold`
- `total_sales_value`, `avg_profit_per_unit`
- `last_restock_date`

**Example:**
```bash
curl http://localhost:5000/api/analytics/supplier-performance
```

---

### 11. Revenue Forecast
**GET** `/api/analytics/revenue-forecast`

Revenue forecast based on historical trends.

**Query Parameters:**
- `months_ahead` (integer, optional): Forecast period (default: 3)

**Response Fields:**
- `month`, `revenue`, `order_count`
- `avg_order_value`, `moving_avg_3month`
- `growth_rate_pct`

**Example:**
```bash
curl "http://localhost:5000/api/analytics/revenue-forecast?months_ahead=6"
```

---

## 🧪 Testing

### Quick Test All Endpoints
```bash
python test_analytics.py
```

### Test Individual Endpoint
```bash
curl http://localhost:5000/api/analytics/customer-segmentation | python -m json.tool
```

### Test with Parameters
```bash
# Customer analytics for specific customer
curl "http://localhost:5000/api/analytics/customers?customer_id=1"

# Sales by quarter
curl "http://localhost:5000/api/analytics/sales-performance?period=quarter"

# Top 10 products
curl "http://localhost:5000/api/analytics/product-performance?top_n=10"
```

---

## 📊 Use Cases

### Business Intelligence
- **Customer Segmentation**: Identify VIP customers and at-risk accounts
- **Sales Performance**: Track revenue trends and growth rates
- **Product Performance**: Identify best sellers and profit margins

### Operations Management
- **Inventory Status**: Monitor stock levels and reorder alerts
- **Warehouse Utilization**: Optimize warehouse capacity
- **Order Fulfillment**: Track shipping performance and delays

### Financial Management
- **Payment Collection**: Monitor accounts receivable and overdue payments
- **Revenue Forecast**: Predict future revenue based on trends
- **Supplier Performance**: Evaluate supplier value and profitability

### Sales & CRM
- **Customer Analytics**: Understand customer behavior and lifetime value
- **User Activity**: Track sales team performance and completion rates

---

## 🎨 Swagger UI

All analytics endpoints are fully documented in Swagger UI:

**Access:** http://localhost:5000/apidocs/

Navigate to the **Analytics** section to:
- View detailed parameter descriptions
- See response schemas
- Test endpoints interactively with "Try it out"
- View example responses

---

## 📈 Response Format

All analytics endpoints return JSON arrays or objects:

**List Response:**
```json
[
  {
    "field1": "value1",
    "field2": 123,
    "field3": 45.67
  },
  ...
]
```

**Success Status:** `200 OK`

---

## 🔍 Data Insights

### Customer Segmentation Insights
- **VIP Customers**: Lifetime value ≥ $100,000
- **High Value**: Lifetime value ≥ $50,000
- **Medium Value**: Lifetime value ≥ $10,000
- **Low Value**: Lifetime value < $10,000

### Activity Segments
- **Active**: Last order ≤ 30 days ago
- **At Risk**: Last order 31-90 days ago
- **Dormant**: Last order 91-180 days ago
- **Inactive**: Last order > 180 days ago

### Stock Status
- **REORDER_NEEDED**: Available ≤ reorder level
- **LOW_STOCK**: Available ≤ 1.5× reorder level
- **ADEQUATE**: Available > 1.5× reorder level

### Credit Status
- **CRITICAL**: Overdue > 80% of credit limit
- **WARNING**: Overdue > 50% of credit limit
- **GOOD**: Overdue ≤ 50% of credit limit

---

## 🚀 Integration Examples

### Python
```python
import requests

# Get customer segmentation
response = requests.get('http://localhost:5000/api/analytics/customer-segmentation')
segments = response.json()

# Filter VIP customers
vip_customers = [c for c in segments if c['value_segment'] == 'VIP']
print(f"VIP Customers: {len(vip_customers)}")

# Get inventory alerts
response = requests.get('http://localhost:5000/api/analytics/inventory-status')
inventory = response.json()

# Find items needing reorder
reorder_needed = [i for i in inventory if i['stock_status'] == 'REORDER_NEEDED']
print(f"Items to reorder: {len(reorder_needed)}")
```

### JavaScript
```javascript
// Fetch sales performance
fetch('http://localhost:5000/api/analytics/sales-performance?period=month')
  .then(response => response.json())
  .then(data => {
    console.log('Monthly Sales:', data);
    const totalRevenue = data.reduce((sum, month) => sum + month.net_revenue, 0);
    console.log('Total Revenue:', totalRevenue);
  });
```

### cURL with jq
```bash
# Get top 5 products by revenue
curl -s http://localhost:5000/api/analytics/product-performance?top_n=5 | \
  jq '.[] | {name: .product_name, revenue: .total_revenue}'

# Count customers by segment
curl -s http://localhost:5000/api/analytics/customer-segmentation | \
  jq 'group_by(.value_segment) | map({segment: .[0].value_segment, count: length})'
```

---

## 📝 Notes

- All endpoints return mock data for testing
- Date parameters accept YYYY-MM-DD format
- Numeric parameters are validated for reasonable ranges
- Response times are optimized for large datasets
- All endpoints support CORS for frontend integration

---

**Last Updated:** February 5, 2026  
**API Version:** 1.0.0  
**Status:** ✅ All 15 endpoints operational
