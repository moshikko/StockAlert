from telegram.ext import Application, CommandHandler
from config import TELEGRAM_BOT_TOKEN
from handlers import start, add_stock, remove_stock, show_watchlist, alert, show_alerts, set_lang
from scheduler import start_scheduler

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_stock))
    app.add_handler(CommandHandler("remove", remove_stock))
    app.add_handler(CommandHandler("watchlist", show_watchlist))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("alerts", show_alerts))
    app.add_handler(CommandHandler("lang", set_lang))

    start_scheduler()
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
