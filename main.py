import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = "8912797126:AAFmdn7oJEZdbZ1FzOQocrYKrvORF8LUqOE"
bot = telebot.TeleBot(TOKEN)

# রেন্ডারের ফ্লাস্ক ওয়েব সার্ভার (পোর্ট প্রবলেম ফিক্স করার জন্য)
app = Flask("")


@app.route("/")
def home():
  return "Bot is active and running!"


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# আপনার দুটি প্রাইভেট চ্যানেলের আইডি
CHANNEL_1 = -1003980643287
CHANNEL_2 = -1004351359406

# আপনার প্রাইভেট চ্যানেল দুটির ইনভাইট লিঙ্ক
INVITE_LINK_1 = "https://t.me/+iLQtJsjlFYQ4Mzhl"
INVITE_LINK_2 = "https://t.me/+HbHhchqJLcdhNzM1"


# ব্যবহারকারী চ্যানেলগুলোতে জয়েন করেছে কিনা তা চেক করার ফাংশন
def check_user_subscription(user_id):
  try:
    chat_member_1 = bot.get_chat_member(CHANNEL_1, user_id)
    chat_member_2 = bot.get_chat_member(CHANNEL_2, user_id)

    valid_status = ["creator", "administrator", "member"]

    if (
        chat_member_1.status in valid_status
        and chat_member_2.status in valid_status
    ):
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

  if check_user_subscription(user_id):
    bot.reply_to(
        message,
        "🎉 **Welcome back to Tricki Store!** 🛍️\n\n"
        "✨ **You are already verified and ready to go!** How can I help you"
        " today? 🚀",
        parse_mode="Markdown",
    )
  else:
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel_1 = types.InlineKeyboardButton(
        "📢 Join Channel 1 🚀", url=INVITE_LINK_1
    )
    btn_channel_2 = types.InlineKeyboardButton(
        "📢 Join Channel 2 🚀", url=INVITE_LINK_2
    )
    btn_check = types.InlineKeyboardButton(
        "🔄 Check Membership ✅", callback_data="check_sub"
    )

    markup.add(btn_channel_1, btn_channel_2, btn_check)

    warning_text = (
        "⚠️ **Access Denied! Must Join Channels!** 🔒\n\n"
        "To use this bot, you **must join** our 2 private channels first! 🛑\n\n"
        "👉 Click the buttons below to join both channels, then click the"
        " **Check Membership** button! 👇"
    )
    bot.send_message(
        message.chat.id, warning_text, reply_markup=markup, parse_mode="Markdown"
    )


# "Check Membership" বাটনে ক্লিক করলে যা কাজ করবে
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
  user_id = call.from_user.id

  if check_user_subscription(user_id):
    success_text = (
        "🎉 **Verification Successful! Thank you for joining both channels!**"
        " 🔥\n\n"
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
        "❌ You haven't joined both channels yet! Please join first.",
        show_alert=True,
    )


# Android এবং iOS বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(
    func=lambda call: call.data in ["price_android", "price_ios"]
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
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=android_price_text,
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
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ios_price_text,
        parse_mode="Markdown",
    )

  bot.answer_callback_query(call.id)


# সাধারণ টেক্সট মেসেজ, Free key এবং 8 Ball Pool Hack হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  user_id = message.from_user.id
  text = message.text.strip().lower()

  if not check_user_subscription(user_id):
    bot.reply_to(
        message,
        "⚠️ **Please join our private channels first and verify via /start!** 🛑",
        parse_mode="Markdown",
    )
    return

  # ইউজার "free key" লিখলে
  if text == "free key":
    my_secret_key = "KURO-ECWM35-2NDYZY-MANP9J"
    bot.reply_to(
        message,
        f"🔑 **Here is your Free Key:**\n`{my_secret_key}`\n\n✨ *Enjoy your"
        " product!* 🛍️",
        parse_mode="Markdown",
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


# বট এবং ওয়েব সার্ভার একসাথে চালু করার কোড
if __name__ == "__main__":
  server_thread = Thread(target=run_web)
  server_thread.start()

  print("Bot and Web Server are running...")
  bot.infinity_polling()
