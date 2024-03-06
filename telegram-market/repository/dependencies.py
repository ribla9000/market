import datetime
from repository.scheduler_logic import ScheduleRepository
from repository.database.broadcasts import BroadcastsRepository
from repository.database.users import UsersRepository, Roles
from aiogram import Bot
from core.config import BOT_TOKEN


async def send_message(broadcast: dict, user: dict):
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=user["chat_id"],
            text=broadcast["text"]
        )
    except Exception as e:
        print(str(e))


async def schedule_broadcasts():
    broadcasts = await BroadcastsRepository.get_all_scheduled()
    users = await UsersRepository.get_all()
    scheduler = ScheduleRepository.scheduler

    for broadcast in broadcasts:
        for user in users:
            if user["role"] != Roles.USER:
                continue

            ScheduleRepository.add_task(
                scheduler=scheduler,
                callback=send_message,
                task_type="5sec",
                user=user,
                broadcast=broadcast,
            )


async def schedule_task_startup():
    await schedule_broadcasts()
    scheduler = ScheduleRepository.scheduler
    ScheduleRepository.add_task(
        scheduler=scheduler,
        callback=schedule_broadcasts,
        task_type="5min",
    )



