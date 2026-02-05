"""Product model"""
from datetime import datetime

class Product:
    def __init__(self, product_id=None, product_code=None, product_name=None,
                 description=None, category=None, brand=None, unit_of_measure=None,
                 unit_price=None, cost_price=None, weight=None, dimensions=None,
                 barcode=None, sku=None, reorder_level=None, reorder_quantity=None,
                 status='active', created_at=None, updated_at=None):
        self.product_id = product_id
        self.product_code = product_code
        self.product_name = product_name
        self.description = description
        self.category = category
        self.brand = brand
        self.unit_of_measure = unit_of_measure
        self.unit_price = unit_price
        self.cost_price = cost_price
        self.weight = weight
        self.dimensions = dimensions
        self.barcode = barcode
        self.sku = sku
        self.reorder_level = reorder_level
        self.reorder_quantity = reorder_quantity
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_code': self.product_code,
            'product_name': self.product_name,
            'description': self.description,
            'category': self.category,
            'brand': self.brand,
            'unit_of_measure': self.unit_of_measure,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'cost_price': float(self.cost_price) if self.cost_price else None,
            'weight': float(self.weight) if self.weight else None,
            'dimensions': self.dimensions,
            'barcode': self.barcode,
            'sku': self.sku,
            'reorder_level': self.reorder_level,
            'reorder_quantity': self.reorder_quantity,
            'status': self.status,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        return Product(**data)
