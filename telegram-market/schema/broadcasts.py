import sqlalchemy
from core.db import metadata


broadcasts = sqlalchemy.Table(
    "broadcasts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("text", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("picture_path", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("telegram_has", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("web_has", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("sent_at", sqlalchemy.DateTime, nullable=False),
)
