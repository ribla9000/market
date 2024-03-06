import sqlalchemy
from core.db import metadata


products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("subcategory_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("article", sqlalchemy.String, nullable=False, default=sqlalchemy.text("uuid_generate_v4()")),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("picture_path", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("telegram_has", sqlalchemy.Boolean, nullable=False, default=sqlalchemy.sql.false()),
    sqlalchemy.Column("web_has", sqlalchemy.Boolean, nullable=False, default=sqlalchemy.sql.false()),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("price", sqlalchemy.BigInteger, nullable=False), # value = 100 is equal to 1$
    sqlalchemy.Column("discount",
                      sqlalchemy.Integer,
                      sqlalchemy.CheckConstraint("discount >= 0 AND discount <= 100"),
                      nullable=False,
                      default=0
                      ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, default=sqlalchemy.func.now()),
    sqlalchemy.Column("is_visible", sqlalchemy.Boolean, nullable=False, default=sqlalchemy.sql.true()),
)
