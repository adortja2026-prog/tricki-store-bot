import os
import telebot

# আপনার টেলিগ্রাম বটের টোকেন এখানে বসানো হলো
TOKEN = "8912797126:AAFmdn7oJEZdbZ1FzOQocrYKrvORF8LUqOE"
bot = telebot.TeleBot(TOKEN)


# /start কমান্ডের জন্য রেসপন্স
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(
      message,
      "স্বাগতম! Tricki Store-এ আপনাকে স্বাগতম। আজ আপনাকে কীভাবে সাহায্য করতে"
      " পারি?",
  )


# সাধারণ টেক্সট মেসেজের উত্তর দেওয়ার জন্য
@bot.message_handler(func=lambda message: True)
def echo_all(message):
  bot.reply_to(
      message,
      f"আপনার বার্তাটি পেয়েছি: '{message.text}'. খুব শীঘ্রই আমাদের স্টোরের পণ্যগুলো"
      " দেখতে পাবেন!",
  )


# বট চালু করার কোড
if __name__ == '__main__':
  print('Bot is running...')
  bot.infinity_polling()
