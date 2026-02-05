#!/bin/bash

# Quick API Test Script
# Tests all endpoints and displays results

echo "=========================================="
echo "Testing CRM & Inventory API"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test health endpoint
echo -e "${BLUE}1. Testing Health Check${NC}"
curl -s http://localhost:5000/health | python -m json.tool
echo ""
echo ""

# Test customers list
echo -e "${BLUE}2. Testing GET /api/customers${NC}"
curl -s http://localhost:5000/api/customers | python -m json.tool
echo ""
echo ""

# Test single customer
echo -e "${BLUE}3. Testing GET /api/customers/1${NC}"
curl -s http://localhost:5000/api/customers/1 | python -m json.tool
echo ""
echo ""

# Test products list
echo -e "${BLUE}4. Testing GET /api/products${NC}"
curl -s http://localhost:5000/api/products | python -m json.tool
echo ""
echo ""

# Test single product
echo -e "${BLUE}5. Testing GET /api/products/1${NC}"
curl -s http://localhost:5000/api/products/1 | python -m json.tool
echo ""
echo ""

# Test orders list
echo -e "${BLUE}6. Testing GET /api/orders${NC}"
curl -s http://localhost:5000/api/orders | python -m json.tool
echo ""
echo ""

# Test single order
echo -e "${BLUE}7. Testing GET /api/orders/1${NC}"
curl -s http://localhost:5000/api/orders/1 | python -m json.tool
echo ""
echo ""

echo -e "${GREEN}=========================================="
echo "All tests completed!"
echo -e "==========================================${NC}"
