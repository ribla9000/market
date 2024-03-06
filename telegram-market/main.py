import asyncio
import logging
from aiogram import Bot, Dispatcher
from alembic import command
from alembic.config import Config
from core.db import database
from core.config import BOT_TOKEN
from handlers import start, cart, catalog, faq
from repository.dependencies import schedule_task_startup
from repository.scheduler_logic import ScheduleRepository


async def main():
    ScheduleRepository.scheduler = ScheduleRepository.initialize()
    bot = Bot(BOT_TOKEN)

    dispatcher = Dispatcher()
    dispatcher.include_router(router=start.router)
    dispatcher.include_router(router=cart.router)
    dispatcher.include_router(router=catalog.router)
    dispatcher.include_router(router=faq.router)

    loop = asyncio.get_event_loop()
    await loop.create_task(database.connect())
    await loop.create_task(schedule_task_startup())
    await loop.create_task(dispatcher.start_polling(bot))
    print("h")
    print("i")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    alembic_cfg = Config("./alembic.ini")
    command.upgrade(alembic_cfg, "head")
    asyncio.run(main())
