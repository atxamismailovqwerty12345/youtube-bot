import os
import asyncio
import yt_dlp

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8748768050:AAGH11u3GkKCOY9lSH30r3UUuCr6fT1zX9o")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube(url: str) -> str:
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "format": "best",
        "noplaylist": True,
        "quiet": True,
        "retries": 3,
        "socket_timeout": 30,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "tv"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправь YouTube ссылку 🎥")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Это не YouTube ❌")
        return

    await update.message.reply_text("Скачиваю... ⏳")

    try:
        file_path = await asyncio.to_thread(download_youtube, url)

        with open(file_path, "rb") as f:
            await update.message.reply_video(video=f)

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"Ошибка ❌\n{e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
