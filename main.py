import telebot
import pyotp
from faker import Faker
from telebot import types

API_TOKEN = '8326261693:AAG7gS-ouLLyjixmx885QMuIXNCoBhogNDQ'
bot = telebot.TeleBot(API_TOKEN)
fake = Faker()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('👤 Generate Fake Name')
    btn2 = types.KeyboardButton('🔑 2FA Code')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Welcome! Nicher button use korun:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👤 Generate Fake Name")
def generate_name(message):
    f_name = fake.first_name()
    l_name = fake.last_name()
    full_name = f"{f_name} {l_name}"
    
    response = (
        f"✅ *Full Name:*\n`{full_name}`\n\n"
        f"🆔 *First Name (Copy):*\n`{f_name}`\n\n"
        f"🆔 *Last Name (Copy):*\n`{l_name}`"
    )
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "🔑 2FA Code")
def ask_2fa_secret(message):
    msg = bot.send_message(message.chat.id, "Apnar 2FA Secret Key-ti পাঠান:")
    bot.register_next_step_handler(msg, process_2fa)

def process_2fa(message):
    try:
        secret = message.text.replace(" ", "")
        totp = pyotp.TOTP(secret)
        code = totp.now()
        bot.send_message(message.chat.id, f"🔐 2FA Code: `{code}`", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "❌ Error! Sthik Secret Key din.")

bot.infinity_polling()
