from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import database
from config import ADMIN_PASSWORD

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    items = database.get_all_items()
    html = "<h2>Товары</h2><ul>"
    for i in items:
        html += f"<li>{i[0]} | {i[1]} | {i[2]}</li>"
    html += "</ul>"
    html += """
    <h3>Добавить товар</h3>
    <form action="/add" method="post">
        <input name="password" placeholder='Пароль'><br>
        <input name="name" placeholder='Название товара'><br>
        <input name="content" placeholder='Содержимое (логин:пароль)'><br>
        <button type="submit">Добавить</button>
    </form>
    """
    return html

@app.post("/add")
async def add_item(name: str = Form(...), content: str = Form(...), password: str = Form(...)):
    if password != ADMIN_PASSWORD:
        return {"ok": False, "error": "Неверный пароль"}
    database.add_item(name, content)
    return {"ok": True, "message": "Товар добавлен"}