from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.users import users, Roles
import sqlalchemy


class UsersRepository(DatabaseRepository):

    @staticmethod
    async def create(user: dict):
        query = users.insert().values(user)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_all():
        query = users.select()
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def get_by_chat_id(chat_id: str):
        query = sqlalchemy.select(users).where(users.c.chat_id == chat_id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_id(id: int):
        query = users.select().where(users.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)
