# Quick Reference Card

## 🚀 Server Access

```
API Server:  http://localhost:5000
Swagger UI:  http://localhost:5000/apidocs/
API Spec:    http://localhost:5000/apispec.json
```

## 📊 Analytics Endpoints (11 total)

```bash
# Customer Analytics
GET /api/analytics/customers
GET /api/analytics/customer-segmentation

# Inventory & Warehouse
GET /api/analytics/inventory-status
GET /api/analytics/warehouse-utilization

# Sales & Products
GET /api/analytics/sales-performance
GET /api/analytics/product-performance
GET /api/analytics/revenue-forecast

# Operations
GET /api/analytics/order-fulfillment
GET /api/analytics/user-activity
GET /api/analytics/supplier-performance

# Financial
GET /api/analytics/payment-collection
```

## 🧪 Quick Tests

```bash
# Test all analytics endpoints
python test_analytics.py

# Test all basic endpoints
python test_endpoints.py

# Full validation
python validate_api.py

# Quick curl test
curl http://localhost:5000/api/analytics/customer-segmentation | python -m json.tool
```

## 📖 Documentation

- `COMPLETE_API_SUMMARY.md` - Overview & statistics
- `ANALYTICS_ENDPOINTS.md` - Analytics reference
- `API_DOCUMENTATION.md` - Full API docs
- `SWAGGER_GUIDE.md` - Swagger usage

## ✅ Status

- **Total Endpoints**: 39
- **Test Pass Rate**: 100%
- **Server Status**: ✅ Running
- **Documentation**: ✅ Complete
