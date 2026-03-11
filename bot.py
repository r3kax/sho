from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
import database

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    items = database.get_all_items()
    text = "Добро пожаловать! Список товаров:\n\n"
    for i in items:
        text += f"{i[0]}: {i[1]}\n"
    text += "\nЧтобы купить, напишите /buy <id товара>"
    await message.answer(text)

@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Использование: /buy <id товара>")
        return
    product_id = args[1]
    item = database.get_item(product_id)
    if not item:
        await message.answer("Товар не найден")
        return
    payload = f"{message.from_user.id}:{product_id}"
    invoice_link = f"https://t.me/CryptoBot?start=invoice_payload_{payload}"
    await message.answer(f"Оплатите товар по ссылке:\n{invoice_link}")

if __name__ == "__main__":
    executor.start_polling(dp)