import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = "8912797126:AAFmdn7oJEZdbZ1FzOQocrYKrvORF8LUqOE"
bot = telebot.TeleBot(TOKEN)

# আপনার নিজের টেলিগ্রাম আইডি এখানে দিন (স্ট্যাট দেখার জন্য)
ADMIN_ID = 123456789  # <--- এখানে আপনার আসল টেলিগ্রাম ইউজার আইডি বসাবেন

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

# আপনার চ্যানেলের ইনভাইট লিঙ্ক
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
    return False


# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id

  # ইউজার বট স্টার্ট করলেই তার আইডি ফাইলে সেভ হবে
  save_user(user_id)

  if check_user_subscription(user_id):
    bot.reply_to(
        message,
        "🎉 **Welcome back to 𝟖 𝐁𝐚𝐥𝐥 𝐏𝐨𝐨𝐥 Hacker!** 🎱\n\n"
        "✨ **You are already verified and ready to go!** How can I help you"
        " today? 🚀",
        parse_mode="Markdown",
    )
  else:
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel = types.InlineKeyboardButton(
        "📢 Join Our Official Channel 🚀", url=INVITE_LINK
    )
    btn_check = types.InlineKeyboardButton(
        "🔄 Check Membership ✅", callback_data="check_sub"
    )

    markup.add(btn_channel, btn_check)

    warning_text = (
        "⚠️ **Access Denied! Must Join Channel!** 🔒\n\n"
        "To use this bot, you **must join** our official channel first! 🛑\n\n"
        "👉 Click the button below to join, then click the **Check Membership**"
        " button! 👇"
    )
    bot.send_message(
        message.chat.id, warning_text, reply_markup=markup, parse_mode="Markdown"
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


# "Check Membership" বাটনে ক্লিক করলে যা কাজ করবে
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
  user_id = call.from_user.id

  if check_user_subscription(user_id):
    success_text = (
        "🎉 **Verification Successful! Thank you for joining!** 🔥\n\n"
        "✨ **You can now use the bot freely.** Type **Free key** or **8 ball"
        " pool hack** to explore! 🛍️"
    )
    try:
      bot.edit_message_text(
          chat_id=call.message.chat.id,
          message_id=call.message.message_id,
          text=success_text,
      )
    except Exception as e:
      print(f"Error editing message: {e}")

    bot.answer_callback_query(call.id, "✅ Verified Successfully! 🎉")
  else:
    bot.answer_callback_query(
        call.id,
        "❌ You haven't joined the channel yet! Please join first.",
        show_alert=True,
    )


# Android, iOS এবং Back বাটন ক্লিক হ্যান্ডলার
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


# বট ইনবক্সে কোনো ফাইল আপলোড করলে তার File ID বের করে দেওয়ার হ্যান্ডলার
@bot.message_handler(content_types=["document"])
def get_file_id(message):
  file_name = message.document.file_name
  file_id = message.document.file_id
  bot.reply_to(
      message,
      f"📂 **File Name:** {file_name}\n\n🔑 **File ID:**\n`{file_id}`",
      parse_mode="Markdown",
  )


# সাধারণ টেক্সট মেসেজ, Free key এবং ফাইল পাঠানোর হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  user_id = message.from_user.id
  text = message.text.strip().lower()

  if not check_user_subscription(user_id):
    bot.reply_to(
        message,
        "⚠️ **Please join our channel first and verify via /start!** 🛑",
        parse_mode="Markdown",
    )
    return

  # ইউজার "free key", "free" বা "key" লিখলে
  if text in ["free key", "free", "key"]:
    my_secret_key = "KURO-ECWM35-2NDYZY-MANP9J"

    bot.reply_to(
        message,
        f"🔑 **Here is your Free Key:**\n`{my_secret_key}`\n\n📦 **Sending your"
        " APK files now...** 👇",
        parse_mode="Markdown",
    )

  # -------------------------------------------------------------
  # [গুরুত্বপূর্ণ]: ফাইলের আইডি পাওয়ার পর নিচের কোটেশনের ভেতর বসাবেন
  # -------------------------------------------------------------
    file_id_1 = "YOUR_FIRST_FILE_ID_HERE"  # প্রথম ফাইলের আইডি এখানে বসাবেন
    file_id_2 = "YOUR_SECOND_FILE_ID_HERE"  # দ্বিতীয় ফাইলের আইডি এখানে বসাবেন

    try:
      bot.send_document(
          message.chat.id,
          file_id_1,
          caption="🤖 **Android Mod APK 1**",
          parse_mode="Markdown",
      )
      bot.send_document(
          message.chat.id,
          file_id_2,
          caption="🤖 **Android Mod APK 2**",
          parse_mode="Markdown",
      )
    except Exception as e:
      print(f"Error sending documents: {e}")
      bot.send_message(
          message.chat.id,
          "⚠️ Files are currently being updated. Please try again later!",
      )

  # ইউজার "8 ball pool hack" বা সম্পর্কিত কিছু লিখলে Android ও iOS বাটন দেখাবে
  elif "8 ball pool" in text or "hack" in text:
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
        f"💬 I received your message: *'{message.text}'*\n📦 Type **8 ball"
        " pool hack** or **Free key**! ✨",
        parse_mode="Markdown",
    )


# __main__ ব্লক
if __name__ == "__main__":
  server_thread = Thread(target=run_web)
  server_thread.start()

  print("Bot and Web Server are running...")
  bot.infinity_polling()
