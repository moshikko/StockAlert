import sqlite3

conn = sqlite3.connect("watchlist.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    lang TEXT DEFAULT 'he'
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS watchlist (
    user_id INTEGER,
    ticker TEXT,
    PRIMARY KEY (user_id, ticker)
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS alerts (
    user_id INTEGER,
    ticker TEXT,
    target_price REAL,
    direction TEXT,
    PRIMARY KEY (user_id, ticker)
)""")

conn.commit()

def add_user(user_id, lang='he'):
    cur.execute("INSERT OR IGNORE INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang))
    conn.commit()

def update_user_lang(user_id, lang):
    cur.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()

def get_user_lang(user_id):
    cur.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    return row[0] if row else "he"

def add_to_watchlist(user_id, ticker):
    cur.execute("INSERT OR IGNORE INTO watchlist (user_id, ticker) VALUES (?, ?)", (user_id, ticker))
    conn.commit()

def remove_from_watchlist(user_id, ticker):
    cur.execute("DELETE FROM watchlist WHERE user_id = ? AND ticker = ?", (user_id, ticker))
    conn.commit()

def get_watchlist(user_id):
    cur.execute("SELECT ticker FROM watchlist WHERE user_id = ?", (user_id,))
    return [row[0] for row in cur.fetchall()]

def set_alert(user_id, ticker, target_price, direction):
    cur.execute("INSERT OR REPLACE INTO alerts (user_id, ticker, target_price, direction) VALUES (?, ?, ?, ?)",
                (user_id, ticker, target_price, direction))
    conn.commit()

def get_all_alerts():
    cur.execute("SELECT user_id, ticker, target_price, direction FROM alerts")
    return cur.fetchall()

def get_alerts_for_user(user_id):
    cur.execute("SELECT ticker, target_price, direction FROM alerts WHERE user_id = ?", (user_id,))
    return cur.fetchall()

def remove_alert(user_id, ticker):
    cur.execute("DELETE FROM alerts WHERE user_id = ? AND ticker = ?", (user_id, ticker))
    conn.commit()
