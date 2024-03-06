import aiohttp
from core.config import YANDEX_AUTH, BOT_LINK
from repository.database.yoo_invoices import YooInvoicesRepository


class YooServiceRepository:

    @staticmethod
    async def create_invoice(money_value: str, user_cart_id: int, description: str, invoice_unique: str = None, test: bool = False):
        print(money_value)
        url = "https://api.yookassa.ru/v3/payments"
        headers = {
            "Idempotence-Key": f"{invoice_unique}",
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        auth = aiohttp.BasicAuth(login=YANDEX_AUTH[0], password=YANDEX_AUTH[1])
        invoice_data = {
            "amount": {
                "value": money_value,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": BOT_LINK
            },
            "capture": True,
            "description": description,
            "test": test
        }

        try:

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=invoice_data, headers=headers, auth=auth) as response:
                    response = await response.json()
                    invoice = {
                        "service_id": response["id"],
                        "cart_id": user_cart_id,
                        "status": response["status"],
                    }
                    invoice_id = await YooInvoicesRepository.create(
                        invoice=invoice
                    )
                    return response

        except Exception as e:
            print(str(e))
