from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

# List of Ads
ads = [
    "🎧 Check out our sponsor: [Product 1] - Best Music Streaming App! 🎶",
    "🎧 Don't miss out on [Product 2] - The best headphones for music lovers! 🎧",
    "🎧 Want unlimited music? Try [Product 3] today! 🎶"
]

def show_ad():
    """Randomly select an ad from the list."""
    return random.choice(ads)

# Function to start the bot
def start(update: Update, context: CallbackContext):
    # Show an ad when user starts the bot
    ad_text = show_ad()
    update.message.reply_text(ad_text)
    
    # Welcome message
    update.message.reply_text("Welcome to the Music Bot! Use /play <song_name> to play music.")

# Function to play music with text ads
def play(update: Update, context: CallbackContext):
    song_query = ' '.join(context.args)  # The song name or URL
    if song_query == '':
        update.message.reply_text('Please provide a song name or URL using /play <song_name>')
        return
    
    # Search and play the music (your music logic goes here)
    update.message.reply_text(f"Searching and playing: {song_query}")

    # Show a text ad before playing music
    ad_text = show_ad()
    update.message.reply_text(ad_text)

# Main function to set up the bot
def main():
    # Replace with your bot's token
    token = "YOUR_BOT_TOKEN"

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Handler for the /start command
    dp.add_handler(CommandHandler("start", start))

    # Handler for the /play command
    dp.add_handler(CommandHandler("play", play))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
