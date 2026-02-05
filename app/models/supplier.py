from datetime import datetime

class Supplier:
    def __init__(self, supplier_id=None, supplier_code=None, supplier_name=None,
                 contact_person=None, email=None, phone=None, address=None,
                 city=None, state=None, country=None, postal_code=None,
                 payment_terms=30, tax_id=None, rating=None, status='active',
                 created_at=None, updated_at=None):
        self.supplier_id = supplier_id
        self.supplier_code = supplier_code
        self.supplier_name = supplier_name
        self.contact_person = contact_person
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.payment_terms = payment_terms
        self.tax_id = tax_id
        self.rating = rating
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'supplier_id': self.supplier_id,
            'supplier_code': self.supplier_code,
            'supplier_name': self.supplier_name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'payment_terms': self.payment_terms,
            'tax_id': self.tax_id,
            'rating': float(self.rating) if self.rating else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Supplier(**data)
