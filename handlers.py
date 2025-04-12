from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import (
    add_user, add_to_watchlist, remove_from_watchlist, get_watchlist,
    set_alert, get_alerts_for_user, update_user_lang, get_user_lang
)

MAIN_MENU = ReplyKeyboardMarkup(
    [["/add", "/remove"], ["/watchlist", "/alerts"], ["/alert", "/lang en/he"]],
    resize_keyboard=True
)

LANG_TEXTS = {
    "he": {
        "start": "ברוך הבא לבוט מעקב מניות! השתמש בתפריט או פקודות: /add /remove /watchlist /alert",
        "add_success": "{} נוסף לרשימת המעקב שלך.",
        "remove_success": "{} הוסר מהרשימה.",
        "empty_watchlist": "רשימת המעקב שלך ריקה.",
        "watchlist_header": "רשימת המעקב שלך:",
        "alert_set": "התראה נקבעה: {} {} {}",
        "alert_usage": "שימוש: /alert TICKER ABOVE|BELOW PRICE",
        "alerts_none": "אין התראות פעילות.",
        "alerts_list": "התראות פעילות:",
        "lang_set": "השפה עודכנה ל-{}"
    },
    "en": {
        "start": "Welcome to Share Monitor Bot! Use menu or commands: /add /remove /watchlist /alert",
        "add_success": "{} added to your watchlist.",
        "remove_success": "{} removed from your watchlist.",
        "empty_watchlist": "Your watchlist is empty.",
        "watchlist_header": "Your watchlist:",
        "alert_set": "Alert set: {} {} {}",
        "alert_usage": "Usage: /alert TICKER ABOVE|BELOW PRICE",
        "alerts_none": "No active alerts.",
        "alerts_list": "Active alerts:",
        "lang_set": "Language updated to {}"
    }
}

def get_text(user_id, key):
    lang = get_user_lang(user_id)
    return LANG_TEXTS.get(lang, LANG_TEXTS["he"])[key]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    await update.message.reply_text(get_text(user_id, "start"), reply_markup=MAIN_MENU)

async def add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        return
    ticker = context.args[0].upper()
    add_to_watchlist(user_id, ticker)
    await update.message.reply_text(get_text(user_id, "add_success").format(ticker))

async def remove_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        return
    ticker = context.args[0].upper()
    remove_from_watchlist(user_id, ticker)
    await update.message.reply_text(get_text(user_id, "remove_success").format(ticker))

async def show_watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tickers = get_watchlist(user_id)
    if tickers:
        await update.message.reply_text(get_text(user_id, "watchlist_header") + "\n" + "\n".join(tickers))
    else:
        await update.message.reply_text(get_text(user_id, "empty_watchlist"))

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if len(context.args) != 3:
        return await update.message.reply_text(get_text(user_id, "alert_usage"))

    ticker = context.args[0].upper()
    direction = context.args[1].lower()
    try:
        price = float(context.args[2])
    except ValueError:
        return await update.message.reply_text(get_text(user_id, "alert_usage"))

    if direction not in ["above", "below"]:
        return await update.message.reply_text(get_text(user_id, "alert_usage"))

    set_alert(user_id, ticker, price, direction)
    await update.message.reply_text(get_text(user_id, "alert_set").format(ticker, direction, price))

async def show_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    alerts = get_alerts_for_user(user_id)
    if not alerts:
        return await update.message.reply_text(get_text(user_id, "alerts_none"))
    
    msg = get_text(user_id, "alerts_list") + "\n"
    for ticker, price, direction in alerts:
        msg += f"{ticker} - {direction} {price}\n"
    await update.message.reply_text(msg)

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args or context.args[0] not in ["he", "en"]:
        return
    lang = context.args[0]
    update_user_lang(user_id, lang)
    await update.message.reply_text(get_text(user_id, "lang_set").format(lang.upper()))
