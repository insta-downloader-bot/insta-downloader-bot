import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '7644704042:AAFlzIg5HgXOCuYZd7zEE5uPbbXtRdI5POI'
CHANNEL_1 = '@birdvpn1'
CHANNEL_2 = '@rahimavazzadeh'

bot = telebot.TeleBot(BOT_TOKEN)

# تابع چک عضویت
def is_user_member(user_id):
    try:
        status1 = bot.get_chat_member(CHANNEL_1, user_id).status
        status2 = bot.get_chat_member(CHANNEL_2, user_id).status
        return status1 in ['member', 'administrator', 'creator'] and status2 in ['member', 'administrator', 'creator']
    except:
        return False

# دکمه‌های شیشه‌ای کانال‌ها
def join_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("📢 عضویت در کانال ۱", url=f"https://t.me/{CHANNEL_1[1:]}"),
        InlineKeyboardButton("📢 عضویت در کانال ۲", url=f"https://t.me/{CHANNEL_2[1:]}"),
        InlineKeyboardButton("✅ عضویت زدم، برو بریم!", callback_data="check_membership")
    )
    return markup

# استارت
@bot.message_handler(commands=['start'])
def start(message):
    if is_user_member(message.from_user.id):
        bot.send_message(message.chat.id, "👋 سلام! لینک پست یا استوری یا ریلز اینستاگرام رو بفرست تا برات دانلود کنم 📥")
    else:
        bot.send_message(
            message.chat.id,
            "⛔ برای استفاده از ربات باید اول عضو دو کانال زیر بشی:",
            reply_markup=join_keyboard()
        )

# بررسی عضویت بعد از زدن دکمه "عضویت زدم"
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_membership(call):
    if is_user_member(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ عضویت تأیید شد!")
        bot.send_message(call.message.chat.id, "حالا لینک اینستا رو بفرست تا برات دانلود کنم 🌟")
    else:
        bot.answer_callback_query(call.id, "❌ هنوز عضو نشدی یا تلگرامت دیر آپدیته.")

# هندل همه لینک‌ها
@bot.message_handler(func=lambda message: True)
def handle_link(message):
    if not is_user_member(message.from_user.id):
        bot.send_message(message.chat.id, "⛔ اول عضو دو کانال شو:", reply_markup=join_keyboard())
        return

    if "instagram.com" not in message.text:
        bot.send_message(message.chat.id, "❌ لطفاً یک لینک معتبر اینستاگرام بفرست.")
        return

    bot.send_chat_action(message.chat.id, "upload_video")
    try:
        res = requests.post(
            "https://igram.io/api/ajaxSearch",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "Mozilla/5.0"
            },
            data={"q": message.text.strip()}
        )

        json_data = res.json()
        medias = json_data['data']['medias']

        for media in medias:
            url = media['url']
            if '.mp4' in url:
                bot.send_video(message.chat.id, url)
            else:
                bot.send_photo(message.chat.id, url)

    except Exception as e:
        bot.send_message(message.chat.id, "❌ متأسفم، مشکلی پیش اومد یا لینک مشکل داشت.")

bot.infinity_polling()

