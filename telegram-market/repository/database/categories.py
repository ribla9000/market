from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.categories import categories
import sqlalchemy


class CategoriesRepository(DatabaseRepository):

    @staticmethod
    async def create(cart: dict):
        query = categories.insert().values(cart)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_by_id(id: int):
        query = categories.select().where(categories.c.id == id)
        return get_values(await DatabaseRepository.fetch_one(query))

    @staticmethod
    async def get_all():
        query = categories.select()
        return get_values(await DatabaseRepository.fetch_all(query))
