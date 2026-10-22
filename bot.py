import telebot
from telebot import types

TOKEN = '8970123408:AAFAL8CviT6c-eoh8Fi5kmSp-rQucq58cW0'
bot = telebot.TeleBot(TOKEN)

# ডামি ব্যালেন্স ডিকশনারি
user_balances = {}

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    # মেনু বাটন তৈরি
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_profile = types.KeyboardButton('👥 MY PROFILE')
    btn_deposit = types.KeyboardButton('💳 DEPOSIT')
    btn_support = types.KeyboardButton('👨‍💻 SUPPORT')
    btn_Buy = types.KeyboardButton('💸 Buy')
    btn_Sell = types.KeyboardButton('💰 Sell')
    markup.add(btn_profile, btn_deposit, btn_support, btn_Buy, btn_Sell)

    welcome_text = (
        "🎂 Welcome to Dollar Buy Sell Bot!\n"
        "আমাদের বটের মাধ্যমে আপনি নিরাপদে ও দ্রুত ডলার কেনাবেচা করতে পারবেন।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# বাটন ক্লিক ও প্রোফাইল হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    if user_id not in user_balances:
        user_balances[user_id] = 0.0
        
    balance = user_balances[user_id]

    if message.text == '👥 MY PROFILE':
        profile_text = (
            f"USER PROFILE\n\n"
            f"Name: {first_name}\n"
            f"User ID: {user_id}\n"
            f"Balance: {balance:.2f} BDT\n"
            f"Status: Active\n"
            f"Referral Link:\n"
            f"https://t.me/doller_buy_sell_bot?start={user_id}"
        )
        # এখানে parse_mode সরিয়ে দেওয়া হয়েছে যাতে কোনো এরর না আসে
        bot.send_message(message.chat.id, profile_text)

    elif message.text == '💳 DEPOSIT':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        
        btn_bkash = telebot.types.InlineKeyboardButton('📱 বিকাশ', callback_data='pay_bkash')
        btn_nagad = telebot.types.InlineKeyboardButton('📱 নগদ', callback_data='pay_nagad')
        btn_binance = telebot.types.InlineKeyboardButton('📱 বিনান্স', callback_data='pay_binance')
        
        markup.add(btn_bkash, btn_nagad, btn_binance)
        bot.send_message(message.chat.id, "💳 ডিপোজিট করার জন্য নিচে থেকে আপনার পেমেন্ট মেথড সিলেক্ট করুন:", reply_markup=markup)

    elif message.text == '💳 DEPOSIT':
        bot.send_message(message.chat.id, "💳 ডিপোজিট করতে অনুগ্রহ করে নিচের মাধ্যমে পেমেন্ট সম্পন্ন করুন:")

    elif message.text == '👨‍💻 SUPPORT':
        bot.send_message(message.chat.id, "👨‍💻 যে কোনো প্রয়োজনে আমাদের সাপোর্ট টিমের সাথে যোগাযোগ করুন: @teamyyt")

# বট রান করা
print("Bot is running...")
import os
from flask import Flask
import threading

app = Flask('__name__')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার চালু রাখা
t = threading.Thread(target=run_web)
t.start()

# বট অনবরত চালু রাখা

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def payment_method_selected(call):
    method = call.data.split('_')[1]
    
    if method == 'bkash':
        text = "📱 বিকাশ পার্সোনাল নম্বর: 01XXXXXXXXX\n\nউপরে দেওয়া নম্বরে ক্যাশ ইন বা সেন্ড মানি করে আপনার Transaction ID টি পাঠান।"
    elif method == 'nagad':
        text = "📱 নগদ পার্সোনাল নম্বর: 01XXXXXXXXX\n\nউপরে দেওয়া নম্বরে সেন্ড মানি করে আপনার Transaction ID টি পাঠান।"
    elif method == 'rocket':
        text = "📱 রকেট পার্সোনাল নম্বর: 01XXXXXXXXX\n\nউপরে দেওয়া নম্বরে সেন্ড মানি করে আপনার Transaction ID টি পাঠান।"
        
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

if __name__ == '__main__':
    bot.polling(none_stop=True, skip_pending=True)