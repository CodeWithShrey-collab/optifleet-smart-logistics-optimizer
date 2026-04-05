from datetime import datetime

from app.extensions import db


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    truck_name = db.Column(db.String(120), nullable=False, unique=True)
    capacity = db.Column(db.Float, nullable=False)
    current_load = db.Column(db.Float, default=0, nullable=False)
    status = db.Column(db.String(50), default="available", nullable=False, index=True)
    location = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def update_from_dict(self, data):
        for field in ("truck_name", "capacity", "current_load", "status", "location"):
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            "id": self.id,
            "truck_name": self.truck_name,
            "capacity": self.capacity,
            "current_load": self.current_load,
            "status": self.status,
            "location": self.location,
        }
