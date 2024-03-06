import sqlalchemy
from core.db import metadata
import uuid


def generate_uuid():
    return str(uuid.uuid4())


user_cart = sqlalchemy.Table(
    "user_cart",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("cart_hash", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("is_bought", sqlalchemy.Boolean, nullable=False, default=sqlalchemy.sql.false())
)
