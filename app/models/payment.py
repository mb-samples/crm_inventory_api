from datetime import datetime

class Payment:
    def __init__(self, payment_id=None, payment_number=None, invoice_id=None,
                 customer_id=None, payment_date=None, payment_method=None,
                 payment_amount=None, reference_number=None, payment_status='completed',
                 notes=None, processed_by=None, created_at=None, updated_at=None):
        self.payment_id = payment_id
        self.payment_number = payment_number
        self.invoice_id = invoice_id
        self.customer_id = customer_id
        self.payment_date = payment_date or datetime.now()
        self.payment_method = payment_method
        self.payment_amount = payment_amount
        self.reference_number = reference_number
        self.payment_status = payment_status
        self.notes = notes
        self.processed_by = processed_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'payment_id': self.payment_id,
            'payment_number': self.payment_number,
            'invoice_id': self.invoice_id,
            'customer_id': self.customer_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method,
            'payment_amount': float(self.payment_amount) if self.payment_amount else None,
            'reference_number': self.reference_number,
            'payment_status': self.payment_status,
            'notes': self.notes,
            'processed_by': self.processed_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Payment(**data)
