from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.subcategories import subcategories
import sqlalchemy


class SubCategoriesRepository(DatabaseRepository):

    @staticmethod
    async def create(cart: dict):
        query = subcategories.insert().values(cart)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_by_id(id: int):
        query = subcategories.select().where(subcategories.c.id == id)
        return get_values(await DatabaseRepository.fetch_one(query))

    @staticmethod
    async def get_all():
        query = subcategories.select()
        return get_values(await DatabaseRepository.fetch_all(query))

    @staticmethod
    async def get_by_category_id(category_id: int):
        query = subcategories.select().where(subcategories.c.category_id == category_id)
        return get_values(await DatabaseRepository.fetch_all(query))
