import sqlalchemy
from core.db import metadata


faq = sqlalchemy.Table(
    "faq",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("question", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("answer", sqlalchemy.Integer, nullable=False),
)
