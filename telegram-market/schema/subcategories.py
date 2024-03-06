import sqlalchemy
from core.db import metadata


subcategories = sqlalchemy.Table(
    "subcategories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
)
