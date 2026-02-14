import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

# ТВОЙ ТОКЕН ОТ BOTFATHER — ВСТАВЬ СЮДА
BOT_TOKEN = 8235229862:AAExmbHY2Osdn9VoInVktAM61sxexR9pvWw

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню при /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Тарифы 💰", callback_data="tariffs"),
            InlineKeyboardButton(text="Купить подписку 🛒", callback_data="buy"),
        ],
        [
            InlineKeyboardButton(text="Мой аккаунт 👤", callback_data="account"),
            InlineKeyboardButton(text="Поддержка ❓", url="t.me/твой_ник"),  # ← замени на свой ник
        ],
    ])

    await message.answer(
        "Добро пожаловать в Arctic VPN! 🌐\n"
        "Быстрый и безопасный WireGuard VPN без логов.\n\n"
        "Выбери действие ниже 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# Обработка нажатий на кнопки
@dp.callback_query(F.data == "tariffs")
async def tariffs_handler(callback: types.CallbackQuery):
    text = (
        "<b>Тарифы Arctic VPN:</b>\n\n"
        "• 1 день — 49 ₽\n"
        "• 1 месяц — 199 ₽\n"
        "• 3 месяца — 499 ₽\n"
        "• Год — 1499 ₽\n\n"
        "Оплата через TON / USDT (мгновенно и без комиссии)"
    )
    await callback.message.answer(text)
    await callback.answer()

@dp.callback_query(F.data == "buy")
async def buy_handler(callback: types.CallbackQuery):
    # Ссылка на оплату — создай инвойс в @CryptoBot и вставь сюда
    payment_link = "https://t.me/CryptoBot?start=pay_xxxxxxxx"  # ← замени на свою ссылку

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить 199 ₽ (1 месяц)", url=payment_link)],
        [InlineKeyboardButton(text="Вернуться в меню", callback_data="back")],
    ])

    await callback.message.answer(
        "Выбери тариф и оплати:\n"
        "После оплаты напиши мне — вышлю конфиг WireGuard",
        reply_markup=keyboard
    )
    await callback.answer()

@dp.callback_query(F.data == "account")
async def account_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        "Твоя подписка: пока нет активной\n"
        "Чтобы купить — нажми «Купить подписку»"
    )
    await callback.answer()

@dp.callback_query(F.data == "back")
async def back_handler(callback: types.CallbackQuery):
    await start_handler(callback.message)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
