import telebot
import requests

BOT_TOKEN = '7644704042:AAFlzIg5HgXOCuYZd7zEE5uPbbXtRdI5POI'
CHANNEL_1 = '@birdvpn1'
CHANNEL_2 = '@rahimavazzadeh'

bot = telebot.TeleBot(BOT_TOKEN)

def is_user_member(user_id):
    try:
        status1 = bot.get_chat_member(CHANNEL_1, user_id).status
        status2 = bot.get_chat_member(CHANNEL_2, user_id).status
        return status1 in ['member', 'administrator', 'creator'] and status2 in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_user_member(message.from_user.id):
        bot.reply_to(message, "سلام 👋 لینک پست اینستاگرام رو برام بفرست تا برات دانلودش کنم.")
    else:
        bot.reply_to(message, "⛔️ برای استفاده از ربات، اول باید عضو این دو کانال بشی:\n\n"
                              "📢 " + CHANNEL_1 + "\n"
                              "📢 " + CHANNEL_2 + "\n\n"
                              "وقتی عضو شدی، دوباره /start رو بزن.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not is_user_member(message.from_user.id):
        bot.reply_to(message, "⛔️ اول باید عضو کانالا بشی:\n" + CHANNEL_1 + "\n" + CHANNEL_2)
        return

    if 'instagram.com' not in message.text:
        bot.reply_to(message, "لطفاً یه لینک اینستاگرام معتبر بفرست 📎")
        return

    try:
        api_url = f"https://api.telegraminsta.com/dl?link={message.text}"
        r = requests.get(api_url).json()
        bot.send_message(message.chat.id, "🔽 لینک دانلود:\n" + r['url'])
    except:
        bot.reply_to(message, "❌ مشکلی پیش اومد، لطفاً دوباره امتحان کن.")

bot.infinity_polling()
