import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application,
CommandHandler,
CallbackQueryHandler,
ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
INSTAGRAM_URL = "https://www.instagram.com/a_m_trails/"
CATALOG_URL = os.getenv("CATALOG_URL", "")
MANAGER_URL = os.getenv("MANAGER_URL", "")

logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
level=logging.INFO,
)
logger = logging.getLogger(name)

WELCOME_TEXT = (
"🚵 Добро пожаловать в AMTrails!\n\n"
"Магазин велосипедных запчастей и компонентов.\n"
"Поможем подобрать комплектующие для твоего велосипеда.\n\n"
"Выбирай нужный раздел:"
)

def main_menu():
rows = []

if CATALOG_URL:
    rows.append([
        InlineKeyboardButton("🛒 Каталог товаров", url=CATALOG_URL)
    ])
else:
    rows.append([
        InlineKeyboardButton("🛒 Каталог товаров", callback_data="catalog")
    ])

rows.extend([
    [InlineKeyboardButton("🔥 Новинки", callback_data="new_items")],
    [InlineKeyboardButton("💬 Связаться с менеджером", callback_data="manager")],
    [InlineKeyboardButton("📸 Наш Instagram", url=INSTAGRAM_URL)],
])

return InlineKeyboardMarkup(rows)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
WELCOME_TEXT,
reply_markup=main_menu()
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"Нажми /start, чтобы открыть главное меню AMTrails."
)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

if query.data == "catalog":
    text = (
        "🛒 Каталог AMTrails пока настраивается. "
        "Напиши нам, и мы поможем подобрать нужную деталь."
    )

elif query.data == "new_items":
    text = (
        "🔥 Раздел новинок скоро появится. "
        "Следи за обновлениями в нашем Instagram!"
    )

elif query.data == "manager":
    if MANAGER_URL:
        await query.message.reply_text(
            "💬 Связаться с менеджером:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "Написать менеджеру", url=MANAGER_URL
                )]
            ])
        )
        return

    text = (
        "💬 Контакт менеджера ещё не добавлен. "
        "Напиши нам в Instagram: @a_m_trails"
    )

elif query.data == "home":
    await query.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu()
    )
    return

else:
    text = "Выбери раздел в меню."

await query.message.reply_text(
    text,
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "⬅️ В главное меню", callback_data="home"
        )]
    ])
)
def main():
if not BOT_TOKEN:
raise RuntimeError(
"Не задан BOT_TOKEN в переменных окружения Railway."
)

application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CallbackQueryHandler(buttons))

logger.info("AMTrails bot is starting...")

application.run_polling(drop_pending_updates=True)
if name == "main":
main()
