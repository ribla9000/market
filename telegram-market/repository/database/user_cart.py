from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.user_cart import user_cart
from schema.users import users
import sqlalchemy


class UserCartRepository(DatabaseRepository):

    @staticmethod
    async def create(cart: dict):
        query = user_cart.insert().values(cart)
        result = await DatabaseRepository.execute(query)
        return result


    @staticmethod
    async def get_by_chat_id(chat_id: str):
        query = user_cart.select().where(
            users.c.chat_id == chat_id,
            user_cart.c.user_id == users.c.id,
            user_cart.c.is_bought == False
        )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_id(id: int):
        query = user_cart.select().where(user_cart.c.id == id)
        return get_values(await DatabaseRepository.fetch_one(query))
