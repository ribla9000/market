from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from core.config import REPLY_TO_USER, REPLY_TO_NOTSUBSCRIBED, START_MENU, BACK_BUTTON_TEXT, CHANNEL_CHAT_ID, CHANNEL_NAME
from repository.database.users import UsersRepository
from repository.tools import ErrorLoggingMiddleware
from handlers.chats import check_subscription
from typing import Union


router = Router()
router.message.middleware(ErrorLoggingMiddleware())


async def create_user(message: Message) -> int:
    chat_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_values = {
        "name": (first_name if first_name is not None else "") + (last_name if last_name is not None else ""),
        "username": message.from_user.username,
        "chat_id": chat_id
    }
    user_id = await UsersRepository.create(user_values)
    return user_id


async def start_menu(message: Union[Message, None] = None, callback: Union[CallbackQuery, None] = None):
    chat_id = str(message.from_user.id if message is not None else callback.from_user.id)
    bot = callback.bot if callback is not None else message.bot
    is_sub = await check_subscription(channel_chat_id=CHANNEL_CHAT_ID, user_chat_id=int(chat_id), bot=bot)
    user = await UsersRepository.get_by_chat_id(chat_id=chat_id)
    if user is None:
        user_id = await create_user(message)
        user = await UsersRepository.get_by_id(id=user_id)

    if not is_sub:
        reply = REPLY_TO_NOTSUBSCRIBED.replace("%CHANNEL%", CHANNEL_NAME)
        if message is not None:
            return await message.answer(
                text=reply,
                parse_mode="html",
            )
        else:
            return await callback.message.edit_text(
                text=reply,
                parse_mode="html"
            )

    my_room_button = InlineKeyboardButton(text="My room 🏠", callback_data="my_room")
    shopping_cart_button = InlineKeyboardButton(text="Cart 🛒", callback_data="cart_open")
    catalog_button = InlineKeyboardButton(text="Catalog 📦", callback_data="categories_open")
    faq_button = InlineKeyboardButton(text="FAQ ⚠️", callback_data="faq")
    keyboard = [
        [catalog_button, shopping_cart_button],
        [my_room_button],
        [faq_button]
    ]

    if message is not None:
        return await message.answer(
            text=REPLY_TO_USER.replace("%USERNAME%", user["name"]),
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    else:
        return await callback.message.edit_text(
            text=REPLY_TO_USER.replace("%USERNAME%", user["name"]),
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )


@router.message(Command("start"))
async def start_on_command(message: Message):
    return await start_menu(message=message)


@router.callback_query(F.data == START_MENU[0])
async def main_menu(callback: CallbackQuery):
    return await start_menu(callback=callback)


@router.callback_query(F.data == "my_room")
async def my_room(callback: CallbackQuery):
    await callback.answer()
    chat_id = str(callback.from_user.id)
    user = await UsersRepository.get_by_chat_id(chat_id)
    reply = f"You are in your cabinet, @{user['username']}"
    change_delivery_button = InlineKeyboardButton(text="Change address 📭", callback_data="change_address")
    my_purchases_button = InlineKeyboardButton(text="My purchases 💰", callback_data="my_purchases")
    back_button = InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[0])
    keyboard = [
        [change_delivery_button],
        [my_purchases_button],
        [back_button]
    ]

    return await callback.message.edit_text(
        text=reply,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
