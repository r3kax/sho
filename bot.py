from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    items = database.get_all_items()
    keyboard = InlineKeyboardMarkup()
    for i in items:
        keyboard.add(InlineKeyboardButton(text=i[1], callback_data=f"buy:{i[0]}"))
    await message.answer("Выберите товар для покупки:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("buy:"))
async def buy_callback(callback_query: types.CallbackQuery):
    product_id = callback_query.data.split(":")[1]
    item = database.get_item(product_id)
    if not item:
        await bot.answer_callback_query(callback_query.id, text="Товар не найден")
        return
    payload = f"{callback_query.from_user.id}:{product_id}"
    invoice_link = f"https://t.me/CryptoBot?start=invoice_payload_{payload}"
    await bot.send_message(callback_query.from_user.id, f"Оплатите товар по ссылке:\n{invoice_link}")
    await bot.answer_callback_query(callback_query.id)

if __name__ == "__main__":
    executor.start_polling(dp)