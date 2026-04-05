from datetime import datetime

from app.extensions import db


class SearchLog(db.Model):
    __tablename__ = "search_logs"

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(255), nullable=False, unique=True)
    frequency = db.Column(db.Integer, default=0, nullable=False)
    last_searched_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
