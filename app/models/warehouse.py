from datetime import datetime

class Warehouse:
    def __init__(self, warehouse_id=None, warehouse_code=None, warehouse_name=None,
                 location=None, address=None, city=None, state=None, country=None,
                 postal_code=None, phone=None, manager_user_id=None, capacity=None,
                 status='active', created_at=None, updated_at=None):
        self.warehouse_id = warehouse_id
        self.warehouse_code = warehouse_code
        self.warehouse_name = warehouse_name
        self.location = location
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.phone = phone
        self.manager_user_id = manager_user_id
        self.capacity = capacity
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'warehouse_id': self.warehouse_id,
            'warehouse_code': self.warehouse_code,
            'warehouse_name': self.warehouse_name,
            'location': self.location,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'phone': self.phone,
            'manager_user_id': self.manager_user_id,
            'capacity': self.capacity,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Warehouse(**data)
