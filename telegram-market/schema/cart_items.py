import sqlalchemy
from core.db import metadata


cart_items = sqlalchemy.Table(
    "cart_items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_cart_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Integer, nullable=False, default=0)
)
