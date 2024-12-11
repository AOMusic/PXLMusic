import logging
from telegram.ext import CallbackContext
from telegram import Update

logging.basicConfig(level=logging.INFO)

def send_ads(update: Update, context: CallbackContext):
    ads_text = "Yeh ads hai!"
    update.message.reply_text(ads_text)
