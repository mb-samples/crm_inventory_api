"""Customer model"""
from datetime import datetime

class Customer:
    def __init__(self, customer_id=None, customer_code=None, company_name=None, 
                 customer_type=None, email=None, phone=None, website=None,
                 billing_address=None, shipping_address=None, city=None, 
                 state=None, country=None, postal_code=None, tax_id=None,
                 credit_limit=None, payment_terms=None, status='active',
                 created_at=None, updated_at=None):
        self.customer_id = customer_id
        self.customer_code = customer_code
        self.company_name = company_name
        self.customer_type = customer_type
        self.email = email
        self.phone = phone
        self.website = website
        self.billing_address = billing_address
        self.shipping_address = shipping_address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.tax_id = tax_id
        self.credit_limit = credit_limit
        self.payment_terms = payment_terms
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'customer_code': self.customer_code,
            'company_name': self.company_name,
            'customer_type': self.customer_type,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'billing_address': self.billing_address,
            'shipping_address': self.shipping_address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'tax_id': self.tax_id,
            'credit_limit': float(self.credit_limit) if self.credit_limit else None,
            'payment_terms': self.payment_terms,
            'status': self.status,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        return Customer(**data)
