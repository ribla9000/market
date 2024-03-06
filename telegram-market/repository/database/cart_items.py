from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.user_cart import user_cart
from schema.cart_items import cart_items
from schema.users import users
import sqlalchemy


class CartItemsRepository(DatabaseRepository):

    @staticmethod
    async def create(cart: dict):
        query = cart_items.insert().values(cart)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_by_chat_id(chat_id: str, limit: int = 6, page: int = 1):
        try:
            query = cart_items.select().where(
                users.c.chat_id == chat_id,
                user_cart.c.user_id == users.c.id,
                user_cart.c.is_bought == False,
                cart_items.c.user_cart_id == user_cart.c.id
            ).limit(limit).offset((page-1)*limit)
            return get_values(await DatabaseRepository.fetch_all(query))
        except Exception as e:
            print(str(e))

    @staticmethod
    async def get_by_id(id: int):
        query = cart_items.select().where(cart_items.c.id == id)
        return get_values(await DatabaseRepository.fetch_one(query))

    @staticmethod
    async def remove_from_cart(cart_id: int, product_id: int):
        print(cart_id, product_id)
        query = cart_items.delete().where(cart_items.c.user_cart_id == cart_id, cart_items.c.product_id == product_id)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_by_cart_id(cart_id: int):
        query = cart_items.select().where(cart_items.c.user_cart_id == cart_id)
        return get_values(await DatabaseRepository.fetch_all(query))