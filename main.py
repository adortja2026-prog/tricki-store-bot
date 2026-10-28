import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = "8912797126:AAFmdn7oJEZdbZ1FzOQocrYKrvORF8LUqOE"
bot = telebot.TeleBot(TOKEN)

# আপনার নিজের টেলিগ্রাম আইডি এখানে দিন (স্ট্যাট দেখার জন্য)
ADMIN_ID = 123456789  # <--- আপনার আসল টেলিগ্রাম ইউজার আইডি এখানে দেবেন

# রেন্ডারের ফ্লাস্ক ওয়েব সার্ভার (পোর্ট প্রবলেম ফিক্স করার জন্য)
app = Flask("")


@app.route("/")
def home():
  return "Bot is active and running!"


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# আপনার চ্যানেলের সঠিক আইডি
CHANNEL_ID = -1004343769999

# আপনার আসল চ্যানেলের ইনভাইট লিঙ্ক (এখানে অন্য কোনো লিংক নেই)
INVITE_LINK = "https://t.me/+8DV9O3hNpWtlMWM1"


# ইউজারের আইডি ফাইলে সেভ করার ফাংশন
def save_user(user_id):
  if not os.path.exists("users.txt"):
    with open("users.txt", "w") as f:
      pass

  with open("users.txt", "r") as f:
    users = f.read().splitlines()

  if str(user_id) not in users:
    with open("users.txt", "a") as f:
      f.write(str(user_id) + "\n")


# মোট ইউজারের সংখ্যা দেখার ফাংশন
def get_total_users():
  if not os.path.exists("users.txt"):
    return 0
  with open("users.txt", "r") as f:
    return len(f.read().splitlines())


# ব্যবহারকারী চ্যানেলটিতে জয়েন করেছে কিনা তা চেক করার ফাংশন
def check_user_subscription(user_id):
  try:
    chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
    valid_status = ["creator", "administrator", "member"]

    if chat_member.status in valid_status:
      return True
    else:
      return False
  except Exception as e:
    print(f"Error checking subscription: {e}")
    # কোনো কারণে এরর আসলে সাময়িকভাবে পাস করার জন্য True রাখতে পারেন
    return True


# মেনু বাটন তৈরি করার ফাংশন
def get_main_menu_keyboard():
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn_free = types.KeyboardButton("🎁 Free Key / Hack")
  btn_paid = types.KeyboardButton("🎱 8 Ball Pool Hack")
  markup.add(btn_free, btn_paid)
  return markup


# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id
  save_user(user_id)

  bot.send_message(
      message.chat.id,
      "🎉 **Welcome back to 𝟖 𝐁𝐚𝐥𝐥 𝐏𝐨𝐨𝐥 𝐇𝐚𝐜𝐤𝐞𝐫!** 🎱\n\n"
      "✨ Choose an option from the menu below: 👇",
      reply_markup=get_main_menu_keyboard(),
      parse_mode="Markdown",
  )


# অ্যাডমিন স্ট্যাটাস দেখার জন্য /stats কমান্ড
@bot.message_handler(commands=["stats"])
def bot_stats(message):
  if message.from_user.id == ADMIN_ID:
    total = get_total_users()
    bot.reply_to(
        message,
        f"📊 **Bot Statistics:**\n\n👥 Total Unique Users: **{total}**",
        parse_mode="Markdown",
    )
  else:
    bot.reply_to(message, "❌ You are not authorized to use this command!")


# Android, iOS এবং Back বাটন ইনলাইন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(
    func=lambda call: call.data in ["price_android", "price_ios", "back_to_menu"]
)
def handle_device_selection(call):
  if call.data == "price_android":
    android_price_text = (
        "🤖 **Android Version - Price List** 📱\n\n"
        "✨ Features: Mod Menu, Anti-Ban, Extended Line.\n\n"
        "🎁 **Pricing:**\n"
        "• 3 Days + 1 Day Free (4 Days) — $6\n"
        "• 7 Days + 3 Days Free (10 Days) — $10\n"
        "• 15 Days + 5 Days Free (20 Days) — $17\n"
        "• 30 Days + 10 Days Free (40 Days) — $30\n\n"
        "🛒 To purchase a key, contact our authorized seller: @Adorkuro"
    )
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        "🔙 Back to Menu", callback_data="back_to_menu"
    )
    markup.add(btn_back)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=android_price_text,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data == "price_ios":
    ios_price_text = (
        "🎉 𝗗𝘂𝘀𝘀𝗲𝗵𝗿𝗮 𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝗢𝗳𝗳𝗲𝗿 🎁\n\n"
        "This Dussehra, enjoy some extra days with every subscription at no"
        " additional cost!\n\n"
        "🎁 Buy a 3-day subscription, get 1 free day — 4 days in total. - 6$\n"
        "🎁 Buy a 7-day subscription, get 3 free days — 10 days in total. -"
        " 10$\n"
        "🎁 Buy a 15-day subscription, get 5 free days — 20 days in total. -"
        " 17$\n"
        "🎁 Buy a 30-day subscription, get 10 free days — 40 days in total. -"
        " 30$\n\n"
        "⏳ Offer is available for a limited time.\n\n"
        "🛒 To purchase a key, contact our authorized seller: @Adorkuro"
    )
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(
        "🔙 Back to Menu", callback_data="back_to_menu"
    )
    markup.add(btn_back)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ios_price_text,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data == "back_to_menu":
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_android = types.InlineKeyboardButton(
        "🤖 Android", callback_data="price_android"
    )
    btn_ios = types.InlineKeyboardButton(
        "🍏 iOS (Special Offer)", callback_data="price_ios"
    )
    markup.add(btn_android, btn_ios)

    menu_text = "🎱 **Choose your device platform to view the price list:** 👇"

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=menu_text,
        reply_markup=markup,
        parse_mode="Markdown",
    )

  bot.answer_callback_query(call.id)


# সাধারণ টেক্সট মেসেজ ও মেনু বাটনের হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  text = message.text.strip()

  # ইউজার যখন নিচের মেনু থেকে "🎁 Free Key / Hack" এ ক্লিক করবে
  if text == "🎁 Free Key / Hack":
    my_secret_key = "KURO-ECWM35-2NDYZY-MANP9J"
    bot.reply_to(
        message,
        f"🔑 **Here is your Free Key:**\n`{my_secret_key}`\n\n✨ *Enjoy your"
        " product!* 🛍️",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown",
    )

  # ইউজার যখন নিচের মেনু থেকে "🎱 8 Ball Pool Hack" এ ক্লিক করবে
  elif (
      text == "🎱 8 Ball Pool Hack"
      or "8 ball pool" in text.lower()
      or "hack" in text.lower()
  ):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_android = types.InlineKeyboardButton(
        "🤖 Android", callback_data="price_android"
    )
    btn_ios = types.InlineKeyboardButton(
        "🍏 iOS (Special Offer)", callback_data="price_ios"
    )
    markup.add(btn_android, btn_ios)

    bot.reply_to(
        message,
        "🎱 **Choose your device platform to view the price list:** 👇",
        reply_markup=markup,
        parse_mode="Markdown",
    )

  else:
    bot.reply_to(
        message,
        "💬 Please choose an option from the menu below! 👇",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown",
    )


if __name__ == "__main__":
  server_thread = Thread(target=run_web)
  server_thread.start()

  print("Bot and Web Server are running...")
  bot.infinity_polling()
