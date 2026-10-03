import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, ADMIN_ID
from products import PRODUCTS
from keyboards import main_menu, catalog_menu, product_menu

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

WELCOME = (
    "🌌 <b>Aether Visual</b>\n\n"
    "Добро пожаловать в официальный магазин визуалов <b>Aether Visual</b>!\n\n"
    "Выбирайте пункт меню ниже 👇"
)

ABOUT = (
    "✨ <b>О нас</b>\n\n"
    "Aether Visual — качественные визуалы для Minecraft.\n"
    "Постоянные обновления, поддержка и быстрый ответ в комментариях."
)

SUPPORT = (
    "💬 <b>Поддержка</b>\n\n"
    "По вопросам покупки и установки пишите администратору.\n"
    "Ответим в течение нескольких часов."
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(WELCOME, reply_markup=main_menu())


@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Используй кнопки меню или /start")


@dp.callback_query(F.data == "back_main")
async def back_main(call: CallbackQuery):
    await call.message.edit_text(WELCOME, reply_markup=main_menu())
    await call.answer()


@dp.callback_query(F.data == "about")
async def about(call: CallbackQuery):
    await call.message.edit_text(ABOUT, reply_markup=main_menu())
    await call.answer()


@dp.callback_query(F.data == "support")
async def support(call: CallbackQuery):
    await call.message.edit_text(SUPPORT, reply_markup=main_menu())
    await call.answer()


@dp.callback_query(F.data == "catalog")
async def catalog(call: CallbackQuery):
    if not PRODUCTS:
        await call.message.edit_text(
            "🛒 <b>Каталог</b>\n\nСкоро здесь появятся визуалы. Загляните позже!",
            reply_markup=main_menu(),
        )
    else:
        await call.message.edit_text("🛒 <b>Каталог визуалов</b>\n\nВыберите товар:", reply_markup=catalog_menu())
    await call.answer()


@dp.callback_query(F.data.startswith("buy:"))
async def buy(call: CallbackQuery):
    pid = call.data.split(":", 1)[1]
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not product:
        await call.answer("Товар не найден", show_alert=True)
        return
    text = (
        f"🎁 <b>{product['name']}</b>\n\n"
        f"{product['description']}\n\n"
        f"💰 Цена: <b>{product['price']}</b>"
    )
    await call.message.edit_text(text, reply_markup=product_menu(pid))
    await call.answer()


@dp.callback_query(F.data.startswith("order:"))
async def order(call: CallbackQuery):
    pid = call.data.split(":", 1)[1]
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    name = product["name"] if product else pid
    await call.answer()
    await bot.send_message(
        ADMIN_ID,
        f"🆕 Новый заказ!\n👤 {call.from_user.full_name} (@{call.from_user.username})\n📦 {name}",
    ) if ADMIN_ID else None
    await call.message.answer(
        f"✅ Заявка на <b>{name}</b> принята!\nАдминистратор свяжется с вами для оплаты."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
