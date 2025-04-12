from apscheduler.schedulers.background import BackgroundScheduler
from stock_api import get_current_price
from database import get_all_alerts, remove_alert, get_watchlist
from collections import defaultdict
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
price_cache = defaultdict(lambda: None)

def check_alerts():
    alerts = get_all_alerts()
    for user_id, ticker, target_price, direction in alerts:
        current = get_current_price(ticker)
        if current is None:
            continue
        if direction == "above" and current > target_price:
            bot.send_message(chat_id=user_id, text=f"{ticker} is above {target_price}: now {current}")
            remove_alert(user_id, ticker)
        elif direction == "below" and current < target_price:
            bot.send_message(chat_id=user_id, text=f"{ticker} is below {target_price}: now {current}")
            remove_alert(user_id, ticker)

def check_watchlist_changes():
    all_users = set(user_id for user_id, _, _, _ in get_all_alerts())
    for user_id in all_users:
        tickers = get_watchlist(user_id)
        for ticker in tickers:
            current = get_current_price(ticker)
            if current is None:
                continue
            prev = price_cache[ticker]
            if prev:
                percent_change = ((current - prev) / prev) * 100
                if abs(percent_change) >= 5:
                    bot.send_message(chat_id=user_id,
                        text=f"{ticker} changed {round(percent_change, 2)}%: now {current}")
            price_cache[ticker] = current

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_alerts, "interval", minutes=5)
    scheduler.add_job(check_watchlist_changes, "interval", minutes=10)
    scheduler.start()
