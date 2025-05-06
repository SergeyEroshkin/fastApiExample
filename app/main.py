from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("API_KEY")
DEBUG_MODE = os.getenv("DEBUG") == "True"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
bot = Bot(token=API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на FastAPI!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы написали: {update.message.text}")


async def setup_bot():
    application = Application.builder().token(API_KEY).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Установка вебхука
    await application.bot.set_webhook(WEBHOOK_URL)
    return application


# FastAPI endpoint для вебхука
@app.post("/webhook")
async def webhook(request: Request):
    application = await setup_bot()
    update_data = await request.json()
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}


# Запуск сервера (если файл запущен напрямую)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)