from bson import ObjectId
from datetime import datetime

class User:
    def __init__(self, name: str, email: str, password_hash: str, role: str):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }