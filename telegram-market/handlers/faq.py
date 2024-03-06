from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, FSInputFile, InputFile
from core.config import BACK_BUTTON_TEXT, MAIN_BUTTON_TEXT, ARROW_RIGHT, ARROW_LEFT, START_MENU, STATIC_PICS
from repository.database.faq import FAQRepository
from repository.tools import keyboard_cols, ErrorLoggingMiddleware


router = Router(name="catalog")
router.message.middleware(ErrorLoggingMiddleware())


@router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):
    try:
        await callback.answer()
        reply = "You are in FAQㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        faqs = await FAQRepository.get_all()

        keyboard = [InlineKeyboardButton(text=faq["question"], callback_data=f"faq_open,{faq['id']}")
                    for faq in faqs
        ]
        keyboard = keyboard_cols(keyboard, 2)
        back_button = InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[0])
        keyboard.append([back_button])

        return await callback.message.edit_text(
            text=reply,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    except Exception as e:
        print(str(e))


@router.callback_query(F.data.startswith("faq_open"))
async def faq_answer(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(",")
    faq_id = int(data[1])
    _faq = await FAQRepository.get_by_id(id=faq_id)
    reply = (f"Question: <b>{_faq['question']}</b>\n\n"
             f"Answer: <i>{_faq['answer']}</i>")

    keyboard = [
        [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="faq")],
        [InlineKeyboardButton(text=MAIN_BUTTON_TEXT, callback_data=START_MENU[0])]
    ]

    return await callback.message.edit_text(
        text=reply,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

