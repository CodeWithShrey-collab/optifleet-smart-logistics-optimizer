from datetime import date

from app.extensions import db


class Analytics(db.Model):
    __tablename__ = "analytics"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False, unique=True)
    total_orders = db.Column(db.Integer, default=0, nullable=False)
    total_profit = db.Column(db.Float, default=0, nullable=False)
