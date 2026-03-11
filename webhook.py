from fastapi import FastAPI, Request
from aiogram import Bot
import database
from config import BOT_TOKEN

app = FastAPI()
bot = Bot(BOT_TOKEN)

@app.post("/crypto")
async def crypto_webhook(request: Request):
    data = await request.json()
    if data.get("update_type") == "invoice_paid":
        payload = data["payload"]
        user_id, product_id = payload.split(":")
        item = database.get_item(product_id)
        if item:
            await bot.send_message(int(user_id), f"✅ Оплата прошла!\nВаш товар:\n{item[2]}")
    return {"ok": True}