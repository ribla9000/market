from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.broadcasts import broadcasts
from schema.broadcasts_sent import broadcasts_sent
from schema.users import users
import sqlalchemy
from sqlalchemy.orm import aliased, load_only
import datetime


class BroadcastsRepository(DatabaseRepository):

    @staticmethod
    async def create(cart: dict):
        query = broadcasts.insert().values(cart)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_all_scheduled():
        now = datetime.datetime.now()
        query = (broadcasts.select().order_by(sqlalchemy.desc(broadcasts.c.sent_at))
                 .where(broadcasts.c.sent_at >= now))
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def make_sent(broadcast_id: int, user_id: int):
        query = broadcasts_sent.insert().values(broadcast_id=broadcast_id, user_id=user_id)
        return await DatabaseRepository.execute(query)