import sqlalchemy
from core.db import metadata


yoo_invoices = sqlalchemy.Table(
    "yoo_invoices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("service_id", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("cart_id", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("value", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("currency", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("paid", sqlalchemy.Boolean, nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, default=sqlalchemy.func.now()),
)
