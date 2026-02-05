from datetime import datetime

class Contact:
    def __init__(self, contact_id=None, customer_id=None, account_id=None,
                 first_name=None, last_name=None, title=None, department=None,
                 email=None, phone=None, mobile=None, is_primary=False,
                 status='active', notes=None, created_at=None, updated_at=None):
        self.contact_id = contact_id
        self.customer_id = customer_id
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.department = department
        self.email = email
        self.phone = phone
        self.mobile = mobile
        self.is_primary = is_primary
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'contact_id': self.contact_id,
            'customer_id': self.customer_id,
            'account_id': self.account_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'title': self.title,
            'department': self.department,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'is_primary': self.is_primary,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Contact(**data)
