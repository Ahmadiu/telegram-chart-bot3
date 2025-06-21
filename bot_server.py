import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
from io import BytesIO

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

def analyze_image_and_respond(image_bytes):
    # تحليل الصورة (مكان التحليل الحقيقي)
    return "📈 شراء عند 195.4
📉 بيع عند 208.6"

def handle_message(update: Update, context):
    if update.message.photo:
        file = update.message.photo[-1].get_file()
        image_bytes = BytesIO()
        file.download(out=image_bytes)
        image_bytes.seek(0)

        result = analyze_image_and_respond(image_bytes.read())
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="أرسل صورة الشارت فقط ✅")

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, use_context=True)
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.process_update(update)
    return "OK"