from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.faq import faq


class FAQRepository(DatabaseRepository):

    @staticmethod
    async def create(values: dict):
        query = faq.insert().values(values)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_all():
        query = faq.select()
        return get_values(await DatabaseRepository.fetch_all(query))

    @staticmethod
    async def get_by_id(id: int):
        query = faq.select().where(faq.c.id == id)
        return get_values(await DatabaseRepository.fetch_one(query))
