from telegram.ext import CommandHandler, CallbackContext
from telegram import Update

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to our bot!")
    update.message.reply_text("Type /help for more information.")

start_handler = CommandHandler('start', start_command)
