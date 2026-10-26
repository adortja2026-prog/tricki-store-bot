import os
import telebot

# টোকেন এনভায়রনমেন্ট ভেরিয়েবল থেকে নেওয়া হচ্ছে
# সেট করার নিয়ম:
#   Linux/Mac: export BOT_TOKEN="আপনার_টোকেন"
#   Windows (CMD): set BOT_TOKEN=আপনার_টোকেন
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN সেট করা হয়নি!")

bot = telebot.TeleBot(TOKEN)


# /start কমান্ডের জন্য রেসপন্স
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "স্বাগতম! Tricki Store-এ আপনাকে স্বাগতম। আজ আপনাকে কীভাবে সাহায্য করতে পারি?",
    )


# /help কমান্ডের জন্য রেসপন্স
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "/start - বট শুরু করুন\n/help - সাহায্য দেখুন")


# সাধারণ টেক্সট মেসেজের উত্তর (নতুন কমান্ড হ্যান্ডলার এর উপরে রাখবেন)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(
        message,
        f"আপনার বার্তাটি পেয়েছি: '{message.text}'. খুব শীঘ্রই আমাদের স্টোরের পণ্যগুলো দেখতে পাবেন!",
    )


# বট চালু করার কোড
if __name__ == '__main__':
    print('Bot is running...')
    bot.infinity_polling()
