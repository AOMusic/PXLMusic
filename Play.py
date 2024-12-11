import os
import youtube_dl
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import InputMediaAudio

# Function to search and play song from YouTube with an ad after playback
def play(update: Update, context: CallbackContext):
    song = ' '.join(context.args)  # Get the song name from user input
    if not song:
        update.message.reply_text("Please provide the song name to play.")
        return
    
    update.message.reply_text(f"Searching for '{song}' on YouTube...")

    # YouTube-dl options to download the audio
    ydl_opts = {
        'format': 'bestaudio/best', 
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor', 
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'extractaudio': True,
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save audio to downloads folder
    }

    # Search on YouTube and download audio
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(f"ytsearch:{song}", download=False)
            video_url = info_dict['entries'][0]['url']  # Get URL of the first search result
            audio_file = ydl.prepare_filename(info_dict['entries'][0])  # Prepare the audio file path
            
            # Download audio file
            ydl.download([f"ytsearch:{song}"])
            update.message.reply_text(f"Now playing '{song}' 🎶 Enjoy the music!")

            # Send the audio file
            with open(audio_file, 'rb') as f:
                update.message.reply_audio(audio=f)

            # Show Ad after the song has been played
            update.message.reply_text(
                "🎉 Enjoyed the music? Check out this special offer from our sponsor!\n"
                "Get 30% off on your first subscription to Spotify with this link: [Affiliate Link]"
            )

            # Clean up downloaded file after sending
            os.remove(audio_file)

        except Exception as e:
            update.message.reply_text(f"Error: Could not play the song. {str(e)}")

# Start command to welcome the user
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to Music Bot! Type /play <song_name> to play a song."
    )

# Main function to set up the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    # Add handlers for the bot commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", play))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
