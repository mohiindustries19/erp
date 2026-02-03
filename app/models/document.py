"""Document storage (DB-backed).

Stores small-to-medium documents inside Postgres so they remain available on
Railway/Docker even when the container filesystem is ephemeral.
"""

from __future__ import annotations

from datetime import datetime

from app import db


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=True, index=True)

    original_filename = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(150), nullable=True)

    data = db.Column(db.LargeBinary, nullable=False)

    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    uploader = db.relationship('User', foreign_keys=[uploaded_by])

    def __repr__(self) -> str:
        return f'<Document {self.id} {self.title!r}>'
