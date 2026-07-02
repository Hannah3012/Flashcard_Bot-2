from bot.handlers import start,conv, list
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import Update
from config import BOT_TOKEN

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv)
    app.add_handler(CommandHandler('list',list))
    app.run_polling(allowed_updates = Update.ALL_TYPES)

if __name__ == "__main__":
    main()

