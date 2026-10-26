import os
import telebot
from telebot import types

# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = "8912797126:AAFmdn7oJEZdbZ1FzOQocrYKrvORF8LUqOE"
bot = telebot.TeleBot(TOKEN)

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


# /start কমান্ড হ্যান্ডলার (ইনলাইন বাটন সহ)
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id

  if check_user_subscription(user_id):
    # যদি আগে থেকেই জয়েন করা থাকে
    bot.reply_to(
        message,
        "🎉 **Welcome to Tricki Store!**\n\n"
        "You are already a member of our channels. How can I help you today?",
        parse_mode="Markdown",
    )
  else:
    # যদি জয়েন করা না থাকে, তবে বাটনসহ মেসেজ পাঠাবে
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_channel_1 = types.InlineKeyboardButton(
        "📢 Join Channel 1", url=INVITE_LINK_1
    )
    btn_channel_2 = types.InlineKeyboardButton(
        "📢 Join Channel 2", url=INVITE_LINK_2
    )
    btn_check = types.InlineKeyboardButton(
        "🔄 Check Membership", callback_data="check_sub"
    )

    markup.add(btn_channel_1, btn_channel_2, btn_check)

    warning_text = (
        "⚠️ **Must Be Join To Channels!**\n\n"
        "To use this bot, you must join our 2 private channels first.\n"
        "Click the buttons below to join, then click the **Check Membership**"
        " button."
    )
    bot.send_message(
        message.chat.id, warning_text, reply_markup=markup, parse_mode="Markdown"
    )


# "Check Membership" বাটনে ক্লিক করলে যা কাজ করবে
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
  user_id = call.from_user.id

  if check_user_subscription(user_id):
    # যদি দুটোতেই জয়েন করা থাকে
    bot.answer_callback_query(call.id, "✅ Verification Successful!")
    bot.send_message(
        call.message.chat.id,
        "🎉 **Thank you for joining both channels!**\n\n"
        "Now you can use the bot. How can I help you today?",
        parse_mode="Markdown",
    )
  else:
    # যদি দুটো বা যেকোনো একটিতে বাদ থাকে
    bot.answer_callback_query(
        call.id,
        "❌ You haven't joined both channels yet!",
        show_alert=True,
    )


# সাধারণ টেক্সট মেসেজের উত্তর
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  user_id = message.from_user.id

  if not check_user_subscription(user_id):
    bot.reply_to(
        message,
        "⚠️ Please join our private channels first and verify via /start!",
    )
    return

  bot.reply_to(
      message,
      f"I received your message: '{message.text}'. You will be able to view"
      " our store products very soon!",
  )


# বট চালু করার কোড
if __name__ == "__main__":
  print("Bot is running...")
  bot.infinity_polling()
