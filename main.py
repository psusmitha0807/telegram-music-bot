from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

# Telegram bot constants
TOKEN: Final = '7867623752:AAF06dn82w5ZrMQ7lFND0KLbaFQIo3zgpvg'
BOT_USERNAME: Final = '@isusi8bot'

# Function to download audio from YouTube
def download_audio(song_name: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': f'{song_name}.mp3',
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries']
        
        if not search_results:
            return None
        
        # Download the first search result
        ydl.download([search_results[0]['webpage_url']])
        return f"{song_name}.mp3"

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, thanks for chatting with me! I am a music recommender bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I can recommend music. Type the name of a song or artist, and I\'ll help!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')

# Responses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    chat_id = update.message.chat.id


    if 'play' in text.lower():
        song_name = text.lower().replace('play', '').strip()
        
        if song_name:
            await update.message.reply_text(f"Searching and downloading the song: {song_name}...")
            audio_file = download_audio(song_name)
            
            if audio_file:
                await context.bot.send_audio(chat_id=chat_id, audio=open(audio_file, 'rb'))
                os.remove(audio_file)  # Remove the file after sending
            else:
                await update.message.reply_text("Sorry, I couldn't find or download that song.")
        else:
            await update.message.reply_text("Please provide the name of a song to play.")
    else:
        response = 'I do not understand what you wrote. You can ask me to recommend music by typing "play [song name]".'
        await update.message.reply_text(response)

# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('polling....')
    app.run_polling(poll_interval=3)