from repository.db import DatabaseRepository
from repository.tools import get_values
from schema.yoo_invoices import yoo_invoices
import sqlalchemy


class YooInvoicesRepository(DatabaseRepository):

    @staticmethod
    async def create(invoice: dict):
        print(invoice)
        query = yoo_invoices.insert().values(invoice)
        return await DatabaseRepository.execute(query)
