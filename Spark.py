import telebot
from PIL import Image
import io
import requests

BOT_TOKEN = "7923799645:AAHzFiXqT2SQ1ud4xk72T1CRzNhR_WRYwJI"
API_URL = "https://chart-analyzer.mahmoudyhia18.repl.co/analyze"  # عدّله حسب رابط مشروعك الجديد

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(msg, "أرسل صورة شارت، وسأحللها لك تلقائيًا 📈")

@bot.message_handler(content_types=['photo'])
def handle_photo(msg):
    file_id = msg.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    # تحويل الصورة إلى Bytes وإرسالها إلى API
    img = Image.open(io.BytesIO(downloaded)).convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    try:
        res = requests.post(API_URL, files={'image': buffer})
        if res.status_code == 200:
            bot.reply_to(msg, f"📊 تحليل الشارت:\n{res.text}")
        else:
            bot.reply_to(msg, "❌ حدث خطأ أثناء التحليل.")
    except Exception as e:
        bot.reply_to(msg, f"❌ خطأ تقني: {str(e)}")

bot.infinity_polling()