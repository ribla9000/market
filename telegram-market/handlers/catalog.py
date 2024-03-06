import uuid
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, FSInputFile, InputFile
from core.config import BACK_BUTTON_TEXT, MAIN_BUTTON_TEXT, ARROW_RIGHT, ARROW_LEFT, START_MENU, STATIC_PICS
from repository.tools import keyboard_cols, ErrorLoggingMiddleware, download_image
from repository.database.users import UsersRepository
from repository.database.user_cart import UserCartRepository
from repository.database.products import ProductsRepository
from repository.database.categories import CategoriesRepository
from repository.database.subcategories import SubCategoriesRepository
from repository.database.cart_items import CartItemsRepository


router = Router(name="catalog")
router.message.middleware(ErrorLoggingMiddleware())


@router.callback_query(F.data == "categories_open")
async def categories_open(callback: CallbackQuery):
    await callback.answer()
    categories = await CategoriesRepository.get_all()
    reply = "Choose the <b>category</b> of products"

    if len(categories) == 0:
        return await callback.answer(
            text="Sorry, no categories now. Come later :)",
            cache_time=2
        )

    back_button = InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[0])
    keyboard = [InlineKeyboardButton(
        text=cat["name"],
        callback_data=f"subcategories_open,{cat['id']}")
        for cat in categories
    ]
    keyboard = keyboard_cols(keyboard, 3)
    keyboard = keyboard
    keyboard.append([back_button])

    return await callback.message.edit_text(
        text=reply,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode="html",
    )


@router.callback_query(F.data.startswith("subcategories_open"))
async def subcategories_open(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(",")
    reply = "Choose the subcategory: "
    category_id = int(data[1])
    subcategories = await SubCategoriesRepository.get_by_category_id(category_id=category_id)

    if len(subcategories) == 0:
        return await callback.answer(
            text="Sorry, no subcategories now. Come later :)",
            cache_time=2
        )

    back_button = InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="categories_open")
    keyboard = [InlineKeyboardButton(
        text=subcat["name"],
        callback_data=f"catalog_open,{subcat['id']}")
        for subcat in subcategories
    ]
    keyboard = keyboard_cols(keyboard, 3)
    keyboard = keyboard
    keyboard.append([back_button])

    try:
        return await callback.message.edit_text(text=reply,reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    except:
        pass
    try:
        return await callback.bot.send_message(chat_id=str(callback.from_user.id), text=reply)
    except Exception as e:
        print(str(e))


@router.callback_query(F.data.startswith("catalog_open"))
async def catalog_open(callback: CallbackQuery, page: int = 1):
    chat_id = str(callback.from_user.id)
    data = callback.data.split(",")
    subcategory_id = int(data[1])
    _page = page if len(data) < 3 else int(data[2])
    products = await ProductsRepository.get_all_visible(subcategory_id=subcategory_id, page=_page)
    subcategory = await SubCategoriesRepository.get_by_id(id=subcategory_id)
    category = await CategoriesRepository.get_by_id(id=subcategory["category_id"])
    reply = (f"You are at <code>{category['name']}/{subcategory['name']}</code>\n\n"
             f"The list of products:\n")

    if len(products) == 0:
        return await callback.answer(
            text="Sorry, no products now. Come later :)",
            cache_time=2
        )

    await callback.answer()
    keyboard = []
    media_group = []
    ind = 0
    for product in products:
        ind += 1

        if product['discount'] > 0:
            total_price = int(product["price"] - (product["price"] * (product["discount"] / 100)))
            price_string = f"<b>{total_price}</b> ❗️⚠️❗️"
        else:
            total_price = int(product['price'] // 100)
            price_string = f"<b>{total_price}</b>"

        product_info = (
                f"{ind}. {product['name']}\n"
                f"description: {product['description'][:52]}...\n"
                f"article: <code>{product['article']}</code>\n"
                f"price: {price_string}\n\n"
        )
        reply += product_info

        if product["picture_path"] is None:
            product["picture_path"] = "unknown.jpg"
        elif product["picture_path"] is not None and product["telegram_has"] is False:
            product["picture_path"] = await download_image(product["picture_path"])
            await ProductsRepository.update(id=product["id"], values={"telegram_has": True})

        file = FSInputFile(STATIC_PICS + product["picture_path"])
        media_group.append( InputMediaPhoto(media=file, caption=product_info, parse_mode="html"))
        button = InlineKeyboardButton(
            text=product["name"],
            callback_data=f"product_in_catalog_open,{product['id']},{subcategory_id},{_page}"
        )
        keyboard.append(button)

    back_button = InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=f"subcategories_open,{category['id']}")
    keyboard = keyboard_cols(keyboard, 3)
    if len(products) > 5:
        keyboard.append([InlineKeyboardButton(text=ARROW_RIGHT, callback_data=f"catalog_open,{subcategory_id},{_page+1}")])
    if _page > 1:
        keyboard.append([InlineKeyboardButton(text=ARROW_LEFT, callback_data=f"catalog_open,{subcategory_id},{_page-1}")])
    keyboard.append([back_button])

    await callback.message.delete()
    try:
        await callback.bot.send_media_group(
            chat_id=chat_id,
            media=media_group
        )
    except Exception as e:
        print(str(e))
    await callback.bot.send_message(
        text="Choose the product or list the page\n" + reply,
        parse_mode="html",
        chat_id=chat_id,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("product_in_catalog_open"))
async def product_in_catalog_open(callback: CallbackQuery, amount: int = 1):
    data = callback.data.split(",")
    product_id = int(data[1])
    subcategory_id = int(data[2])
    products_page = data[3]
    _amount = int(data[4]) if len(data) > 4 else amount

    if _amount > 9:
        await callback.answer(text="You can't take more than 9. Sorry :)")
        _amount = 9
    elif _amount < 1:
        await callback.answer(text="You can't take less than 1. Sorry :)")
        _amount = 1
    else:
        await callback.answer()

    chat_id = str(callback.from_user.id)
    product = await ProductsRepository.get_by_id(product_id)

    if product["picture_path"] is None:
        product["picture_path"] = "unknown.jpg"
    elif product["picture_path"] is not None and product["telegram_has"] is False:
        product["picture_path"] = await download_image(product["picture_path"])
        await ProductsRepository.update(id=product["id"], values={"telegram_has": True})

    if product['discount'] > 0:
        total_price = int(product["price"] - (product["price"] * (product["discount"] / 100)))
        price_string = f"<b>{total_price}</b> ❗️⚠️❗️"
    else:
        total_price = int(product['price'] / 100)
        price_string = f"<b>{total_price}</b>"

    reply = (f"{product['name']}\n"
             f"description: {product['description']}\n"
             f"article: <code>{product['article']}</code>\n"
             f"price: {price_string}")

    back_button = InlineKeyboardButton(
        text=BACK_BUTTON_TEXT,
        callback_data=f"catalog_open,{subcategory_id},{products_page}"
    )
    plus_button = InlineKeyboardButton(
        text="Add",
        callback_data=f"product_in_catalog_open,{product_id},{subcategory_id},{products_page},{_amount + 1}"
    )
    minus_button = InlineKeyboardButton(
        text="Remove",
        callback_data=f"product_in_catalog_open,{product_id},{subcategory_id},{products_page},{_amount + 1}"
    )
    amount_button = InlineKeyboardButton(
        text=f"{_amount}",
        callback_data="NONE"
    )
    add_to_cart_button = InlineKeyboardButton(
        text="Add to 🛒",
        callback_data=f"product_in_catalog_add,{product_id},{_amount},{subcategory_id},{products_page}"
    )
    main_menu_button = InlineKeyboardButton(text=MAIN_BUTTON_TEXT, callback_data=START_MENU[0])
    keyboard = [
        [add_to_cart_button],
        [plus_button, amount_button, minus_button],
        [back_button],
        [main_menu_button]
    ]

    file = FSInputFile(STATIC_PICS + product["picture_path"])
    if len(data) > 4:
        try:
            return await callback.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        except Exception as e:
            print(str(e))
            pass
    try:
        return await callback.bot.send_photo(
            chat_id=chat_id,
            photo=file,
            caption=reply,
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )
    except Exception as e:
        print(str(e))


@router.callback_query(F.data.startswith("product_in_catalog_add"))
async def product_in_catalog_add(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(",")
    chat_id = str(callback.from_user.id)
    product_id = int(data[1])
    amount = int(data[2])
    subcategory_id = int(data[3])
    products_page = int(data[4])
    product = await ProductsRepository.get_by_id(id=product_id)
    user = await UsersRepository.get_by_chat_id(chat_id=chat_id)
    cart = await UserCartRepository.get_by_chat_id(chat_id=chat_id)

    if cart is None:
        hash = uuid.uuid4()
        cart_values = {"user_id": user["id"], "cart_hash": str(hash)}
        user_cart_id = await UserCartRepository.create(cart_values)
    else:
        user_cart_id = cart["id"]

    cart_item_values = {
        "user_cart_id": user_cart_id,
        "product_id": product_id,
        "amount": amount
    }
    cart_item_id = await CartItemsRepository.create(cart_item_values)
    to_cart_button = InlineKeyboardButton(text="To cart", callback_data="cart_open")
    to_shopping_button = InlineKeyboardButton(
        text="Shopping",
        callback_data=f"catalog_open,{subcategory_id},{products_page}"
    )
    main_menu_button = InlineKeyboardButton(text=MAIN_BUTTON_TEXT, callback_data=START_MENU[0])

    keyboard = [
        [to_shopping_button],
        [to_cart_button],
        [main_menu_button]
    ]

    reply = (f"Congrats! You have added <i>x{amount}</i>:\n"
             f"<b>{product['name']}</b> to your cart!")

    await callback.message.delete()
    await callback.bot.send_message(
        chat_id=chat_id,
        text=reply,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )