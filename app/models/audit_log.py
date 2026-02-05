from datetime import datetime

class AuditLog:
    def __init__(self, audit_id=None, table_name=None, record_id=None,
                 action=None, old_values=None, new_values=None,
                 changed_by=None, changed_at=None, ip_address=None, user_agent=None):
        self.audit_id = audit_id
        self.table_name = table_name
        self.record_id = record_id
        self.action = action
        self.old_values = old_values
        self.new_values = new_values
        self.changed_by = changed_by
        self.changed_at = changed_at or datetime.now()
        self.ip_address = ip_address
        self.user_agent = user_agent

    def to_dict(self):
        return {
            'audit_id': self.audit_id,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'action': self.action,
            'old_values': self.old_values,
            'new_values': self.new_values,
            'changed_by': self.changed_by,
            'changed_at': self.changed_at.isoformat() if self.changed_at else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }

    @staticmethod
    def from_dict(data):
        return AuditLog(**data)
