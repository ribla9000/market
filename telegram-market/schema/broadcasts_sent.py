import sqlalchemy
from core.db import metadata


broadcasts_sent = sqlalchemy.Table(
    "broadcasts_sent",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("broadcast_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, default=sqlalchemy.func.now()),
)
