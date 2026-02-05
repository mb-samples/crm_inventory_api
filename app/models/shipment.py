from datetime import datetime

class Shipment:
    def __init__(self, shipment_id=None, shipment_number=None, order_id=None,
                 warehouse_id=None, carrier=None, tracking_number=None,
                 shipment_date=None, estimated_delivery=None, actual_delivery=None,
                 shipment_status='preparing', shipping_cost=None, weight=None,
                 notes=None, created_by=None, created_at=None, updated_at=None):
        self.shipment_id = shipment_id
        self.shipment_number = shipment_number
        self.order_id = order_id
        self.warehouse_id = warehouse_id
        self.carrier = carrier
        self.tracking_number = tracking_number
        self.shipment_date = shipment_date or datetime.now()
        self.estimated_delivery = estimated_delivery
        self.actual_delivery = actual_delivery
        self.shipment_status = shipment_status
        self.shipping_cost = shipping_cost
        self.weight = weight
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'shipment_id': self.shipment_id,
            'shipment_number': self.shipment_number,
            'order_id': self.order_id,
            'warehouse_id': self.warehouse_id,
            'carrier': self.carrier,
            'tracking_number': self.tracking_number,
            'shipment_date': self.shipment_date.isoformat() if self.shipment_date else None,
            'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            'actual_delivery': self.actual_delivery.isoformat() if self.actual_delivery else None,
            'shipment_status': self.shipment_status,
            'shipping_cost': float(self.shipping_cost) if self.shipping_cost else None,
            'weight': float(self.weight) if self.weight else None,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Shipment(**data)
