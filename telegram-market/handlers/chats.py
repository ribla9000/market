from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from repository.database.broadcasts import BroadcastsRepository
from core.config import BOT_TOKEN


async def check_subscription(channel_chat_id: str, user_chat_id: int, bot: Bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_chat_id, user_id=user_chat_id)
        return member.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False


async def send_broadcast(to_send: dict):
    bot = Bot(BOT_TOKEN)
