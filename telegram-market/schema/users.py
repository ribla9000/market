import sqlalchemy
from core.db import metadata


class Roles:
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("role", sqlalchemy.String, nullable=False, server_default=Roles.USER),
    sqlalchemy.Column("address", sqlalchemy.String, nullable=True)
)
