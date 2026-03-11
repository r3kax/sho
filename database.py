import sqlite3

conn = sqlite3.connect("shop.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    content TEXT
)
""")
conn.commit()

def add_item(name, content):
    cursor.execute("INSERT INTO items (name, content) VALUES (?, ?)", (name, content))
    conn.commit()

def get_item(item_id):
    cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
    return cursor.fetchone()

def get_all_items():
    cursor.execute("SELECT * FROM items")
    return cursor.fetchall()