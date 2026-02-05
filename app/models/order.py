"""Order model"""
from datetime import datetime

class Order:
    def __init__(self, order_id=None, order_number=None, customer_id=None,
                 order_date=None, required_date=None, shipped_date=None,
                 status='pending', total_amount=None, tax_amount=None,
                 discount_amount=None, shipping_cost=None, payment_status='unpaid',
                 shipping_address=None, billing_address=None, notes=None,
                 created_at=None, updated_at=None):
        self.order_id = order_id
        self.order_number = order_number
        self.customer_id = customer_id
        self.order_date = order_date or datetime.now()
        self.required_date = required_date
        self.shipped_date = shipped_date
        self.status = status
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.shipping_cost = shipping_cost
        self.payment_status = payment_status
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'order_number': self.order_number,
            'customer_id': self.customer_id,
            'order_date': self.order_date.isoformat() if isinstance(self.order_date, datetime) else self.order_date,
            'required_date': self.required_date.isoformat() if isinstance(self.required_date, datetime) else self.required_date,
            'shipped_date': self.shipped_date.isoformat() if isinstance(self.shipped_date, datetime) else self.shipped_date,
            'status': self.status,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'tax_amount': float(self.tax_amount) if self.tax_amount else None,
            'discount_amount': float(self.discount_amount) if self.discount_amount else None,
            'shipping_cost': float(self.shipping_cost) if self.shipping_cost else None,
            'payment_status': self.payment_status,
            'shipping_address': self.shipping_address,
            'billing_address': self.billing_address,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        return Order(**data)
