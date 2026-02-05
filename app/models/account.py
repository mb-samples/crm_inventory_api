from datetime import datetime

class Account:
    def __init__(self, account_id=None, customer_id=None, account_number=None,
                 account_name=None, account_type=None, status='active',
                 billing_address=None, shipping_address=None, phone=None, email=None,
                 created_at=None, updated_at=None):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.account_name = account_name
        self.account_type = account_type
        self.status = status
        self.billing_address = billing_address
        self.shipping_address = shipping_address
        self.phone = phone
        self.email = email
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'customer_id': self.customer_id,
            'account_number': self.account_number,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'status': self.status,
            'billing_address': self.billing_address,
            'shipping_address': self.shipping_address,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Account(**data)
