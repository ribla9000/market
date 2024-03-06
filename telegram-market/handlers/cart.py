import uuid
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from core.config import ARROW_RIGHT, ARROW_LEFT, BACK_BUTTON_TEXT, MAIN_BUTTON_TEXT, START_MENU
from repository.tools import keyboard_cols, ErrorLoggingMiddleware
from repository.yoo_invoices import YooServiceRepository
from repository.database.cart_items import CartItemsRepository
from repository.database.user_cart import UserCartRepository
from repository.database.users import UsersRepository
from repository.database.products import ProductsRepository
from handlers.start import main_menu


router = Router()
router.message.middleware(ErrorLoggingMiddleware())


@router.callback_query(F.data.startswith("cart_open"))
async def cart_open(callback: CallbackQuery, page: int = 1):
    chat_id = str(callback.from_user.id)
    data = callback.data.split(",")
    _page = page if len(data) < 2 else int(data[1])
    user = await UsersRepository.get_by_chat_id(chat_id=chat_id)
    cart_items = await CartItemsRepository.get_by_chat_id(chat_id=chat_id, page=_page)

    if len(cart_items) == 0:
        return await callback.answer(
            text="Sorry, you don't have any requested items"
        )
    else:
        await callback.answer()

    items_in_cart = len(cart_items)
    reply = (f"@{user['username']}\n"
             f"uniq-identifier: <code>{user['chat_id']}</code>\n"
             f"Total products: {items_in_cart}\n"
             f"Total amount of all products in cart: %AMOUNT%\n"
             f"Total cost: <b>%COST%</b>"
             f"<pre language=\"c++\">Page={_page}</pre>")

    keyboard = []
    total_cost = 0
    total_amount = 0
    for item in cart_items:
        product = await ProductsRepository.get_by_id(item["product_id"])
        button = InlineKeyboardButton(text=product["name"], callback_data=f"item_in_cart,{product['id']},{_page}")

        if product["discount"] > 0:
            total_cost += int(product["price"] - (product["price"] * (product["discount"] / 100)))
        else:
            total_cost += item["amount"] * (product["price"]//100)

        total_amount += item["amount"]
        keyboard.append(button)

    keyboard = keyboard_cols(keyboard, 2)
    purchase_button = InlineKeyboardButton(text="Purchase 💲", callback_data="purchase")
    keyboard.append([purchase_button])
    back_button = InlineKeyboardButton(text=MAIN_BUTTON_TEXT, callback_data=START_MENU[0])

    if items_in_cart > 5:
        keyboard.append([InlineKeyboardButton(text=ARROW_RIGHT, callback_data=f"cart_open,{_page + 1}")])
    if _page > 1:
        keyboard.append([InlineKeyboardButton(text=ARROW_LEFT, callback_data=f"cart_open,{_page - 1}")])
    keyboard.append([back_button])

    reply = reply.replace("%AMOUNT%", f"{total_amount}")
    reply = reply.replace("%COST%", f"{total_cost}")
    await callback.message.edit_text(
        text=reply,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("item_in_cart"))
async def item_in_cart(callback: CallbackQuery):

    await callback.answer()
    chat_id = str(callback.from_user.id)
    data = callback.data.split(",")
    product_id = int(data[1])
    product = await ProductsRepository.get_by_id(product_id)
    page = data[2]
    user_cart = await UserCartRepository.get_by_chat_id(chat_id=chat_id)

    if user_cart is None:
        user = await UsersRepository.get_by_chat_id(chat_id=chat_id)
        hash = uuid.uuid4()
        cart_values = {"user_id": user["id"], "cart_hash": str(hash)}
        user_cart_id = await UserCartRepository.create(cart_values)
    else:
        user_cart_id = user_cart["id"]

    remove_button = InlineKeyboardButton(
        text="Remove ❌",
        callback_data=f"remove_item_from_cart,{product_id},{user_cart_id}"
    )
    back_button = InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=f"cart_open,{page}")
    main_button = InlineKeyboardButton(text=MAIN_BUTTON_TEXT, callback_data=START_MENU[0])
    if product['discount'] > 0:
        total_price = int(product["price"] - (product["price"] * (product["discount"] / 100)))
        price_string = f"<b>{total_price}</b> ❗️⚠️❗️"
    else:
        total_price = int(product['price'] / 100)
        price_string = f"<b>{total_price}</b>"

    reply = (f"{product['name']}\n"
             f"description: {product['description']}\n"
             f"article: <code>{product['article']}</code>\n"
             f"discount: {product['discount']}%"
             f"price: {price_string}")

    keyboard = [
        [remove_button],
        [back_button],
        [main_button]
    ]
    return await callback.message.edit_text(
        text=reply,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("remove_item_from_cart"))
async def remove_item_from_cart(callback: CallbackQuery):
    await callback.answer()
    chat_id = str(callback.from_user.id)
    cart = await UserCartRepository.get_by_chat_id(chat_id=chat_id)
    products_in_cart = await CartItemsRepository.get_by_cart_id(cart_id=cart["id"])
    amount_products = len(products_in_cart)
    data = callback.data.split(",")
    product_id = int(data[1])
    page = int(data[2])
    await CartItemsRepository.remove_from_cart(product_id=product_id, cart_id=cart['id'])

    if amount_products == 1:
        return await main_menu(callback=callback)

    return await cart_open(callback=callback, page=page)


@router.callback_query(F.data.startswith("purchase"))
async def buy_items_in_cart(callback: CallbackQuery):
    chat_id = str(callback.from_user.id)
    user_cart = await UserCartRepository.get_by_chat_id(chat_id=chat_id)
    cart_items = await CartItemsRepository.get_by_cart_id(cart_id=user_cart["id"])

    if len(cart_items) == 0:
        return await callback.answer(text="Sorry, your cart is empty, don't purchase an air! :)")
    else:
        await callback.answer()

    total_items = 0
    money_value = 0
    for item in cart_items:
        total_items += item["amount"]
        product = await ProductsRepository.get_by_id(id=item["product_id"])

        if product['discount'] > 0:
            money_value += int(product["price"] - (product["price"] * (product["discount"] / 100))) * item["amount"]
        else:
            money_value += int((product['price'] // 100) * item["amount"])

    reply = (f"Unique invoice id: {user_cart['cart_hash']}\n"
             f"items in cart: {len(cart_items)}\n"
             f"total items: {total_items}")
    invoice = await YooServiceRepository.create_invoice(
        money_value=str(money_value),
        description=reply,
        test=True,
        invoice_unique=user_cart['cart_hash'],
        user_cart_id=user_cart["id"]
    )
    confirm_button = InlineKeyboardButton(
        text="Confirm ✅",
        url=invoice["confirmation"]["confirmation_url"],
        callback_data=START_MENU[0]
    )
    main_button = InlineKeyboardButton(text=MAIN_BUTTON_TEXT, callback_data=START_MENU[0])
    keyboard = [
        [confirm_button],
        [main_button]
    ]
    return await callback.message.edit_text(
        text=reply,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
