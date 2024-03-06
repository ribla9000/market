from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.products import products
import sqlalchemy


class ProductsRepository(DatabaseRepository):

    @staticmethod
    async def create(cart: dict):
        query = products.insert().values(cart)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_by_id(id: int):
        query = products.select().where(products.c.id == id)
        return get_values(await DatabaseRepository.fetch_one(query))

    @staticmethod
    async def get_all_visible(subcategory_id: int, page: int = 1, limit: int = 6):
        query = (products
                 .select()
                 .where(products.c.is_visible == True, products.c.subcategory_id == subcategory_id)
                 .limit(limit)
                 .offset((page-1) * limit)
                 )
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def update(id: int, values: dict):
        query = products.update().values(values).where(products.c.id == id)
        await DatabaseRepository.execute(query)
