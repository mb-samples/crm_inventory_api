from datetime import datetime

class Invoice:
    def __init__(self, invoice_id=None, invoice_number=None, order_id=None,
                 customer_id=None, invoice_date=None, due_date=None,
                 subtotal=None, tax_amount=0.0, total_amount=None,
                 amount_paid=0.0, amount_due=None, invoice_status='draft',
                 payment_terms=30, notes=None, created_by=None,
                 created_at=None, updated_at=None):
        self.invoice_id = invoice_id
        self.invoice_number = invoice_number
        self.order_id = order_id
        self.customer_id = customer_id
        self.invoice_date = invoice_date or datetime.now()
        self.due_date = due_date
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.total_amount = total_amount
        self.amount_paid = amount_paid
        self.amount_due = amount_due if amount_due is not None else (total_amount - amount_paid if total_amount else 0)
        self.invoice_status = invoice_status
        self.payment_terms = payment_terms
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'invoice_id': self.invoice_id,
            'invoice_number': self.invoice_number,
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'subtotal': float(self.subtotal) if self.subtotal else None,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0.0,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'amount_paid': float(self.amount_paid) if self.amount_paid else 0.0,
            'amount_due': float(self.amount_due) if self.amount_due else None,
            'invoice_status': self.invoice_status,
            'payment_terms': self.payment_terms,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Invoice(**data)
