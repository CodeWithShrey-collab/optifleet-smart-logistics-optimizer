from datetime import datetime

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    package_name = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False)
    priority = db.Column(db.Integer, default=1, nullable=False)
    source = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    delivery_start = db.Column(db.DateTime, nullable=False)
    delivery_end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def update_from_dict(self, data):
        for field in (
            "customer_name",
            "package_name",
            "weight",
            "profit",
            "priority",
            "source",
            "destination",
            "delivery_start",
            "delivery_end",
            "status",
        ):
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "package_name": self.package_name,
            "weight": self.weight,
            "profit": self.profit,
            "priority": self.priority,
            "source": self.source,
            "destination": self.destination,
            "delivery_start": self.delivery_start.isoformat(),
            "delivery_end": self.delivery_end.isoformat(),
            "status": self.status,
        }
