from datetime import datetime

class Activity:
    def __init__(self, activity_id=None, activity_type=None, subject=None,
                 description=None, customer_id=None, contact_id=None, order_id=None,
                 activity_date=None, due_date=None, completed_date=None,
                 status='pending', priority='medium', assigned_user_id=None,
                 created_by=None, created_at=None, updated_at=None):
        self.activity_id = activity_id
        self.activity_type = activity_type
        self.subject = subject
        self.description = description
        self.customer_id = customer_id
        self.contact_id = contact_id
        self.order_id = order_id
        self.activity_date = activity_date or datetime.now()
        self.due_date = due_date
        self.completed_date = completed_date
        self.status = status
        self.priority = priority
        self.assigned_user_id = assigned_user_id
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'activity_type': self.activity_type,
            'subject': self.subject,
            'description': self.description,
            'customer_id': self.customer_id,
            'contact_id': self.contact_id,
            'order_id': self.order_id,
            'activity_date': self.activity_date.isoformat() if self.activity_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'status': self.status,
            'priority': self.priority,
            'assigned_user_id': self.assigned_user_id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        return Activity(**data)
