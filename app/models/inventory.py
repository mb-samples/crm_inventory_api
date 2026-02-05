from datetime import datetime

class Inventory:
    def __init__(self, inventory_id=None, product_id=None, warehouse_id=None,
                 quantity_on_hand=0, quantity_reserved=0, quantity_available=None,
                 bin_location=None, last_stock_check=None, last_restock_date=None,
                 created_at=None, updated_at=None):
        self.inventory_id = inventory_id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.quantity_on_hand = quantity_on_hand
        self.quantity_reserved = quantity_reserved
        self.quantity_available = quantity_available if quantity_available is not None else (quantity_on_hand - quantity_reserved)
        self.bin_location = bin_location
        self.last_stock_check = last_stock_check
        self.last_restock_date = last_restock_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'inventory_id': self.inventory_id,
            'product_id': self.product_id,
            'warehouse_id': self.warehouse_id,
            'quantity_on_hand': self.quantity_on_hand,
            'quantity_reserved': self.quantity_reserved,
            'quantity_available': self.quantity_available,
            'bin_location': self.bin_location,
            'last_stock_check': self.last_stock_check.isoformat() if self.last_stock_check else None,
            'last_restock_date': self.last_restock_date.isoformat() if self.last_restock_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Inventory(**data)
