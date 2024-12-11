from telegram.ext import Updater, CommandHandler, MessageHandler
from ads import send_ads

TOKEN = "YOUR_BOT_TOKEN"

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, send_ads))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
