import os
import telebot

# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = "8912797126:AAFmdn7oJEZdbZ1FzOQocrYKrvORF8LUqOE"
bot = telebot.TeleBot(TOKEN)

# আপনার দুটি প্রাইভেট চ্যানেলের আইডি
CHANNEL_1 = -1003980643287
CHANNEL_2 = -1004351359406


# ব্যবহারকারী চ্যানেলগুলোতে জয়েন করেছে কিনা তা চেক করার ফাংশন
def check_user_subscription(user_id):
  try:
    # প্রথম চ্যানেল চেক
    chat_member_1 = bot.get_chat_member(CHANNEL_1, user_id)
    # দ্বিতীয় চ্যানেল চেক
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


# /start কমান্ড হ্যান্ডলার (সম্পূর্ণ ইংরেজিতে)
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id

  is_subscribed = check_user_subscription(user_id)

  if not is_subscribed:
    warning_text = (
        "⚠️ **Access Denied!**\n\n"
        "To use this bot, you must join our private channels first.\n"
        "Please join both private channels using your invite links, then"
        " send the /start command again."
    )
    bot.reply_to(message, warning_text, parse_mode="Markdown")
  else:
    welcome_text = (
        "🎉 **Welcome to Tricki Store!**\n\n"
        "Thank you for joining our channels. How can I help you today?"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")


# সাধারণ টেক্সট মেসেজের উত্তর (সম্পূর্ণ ইংরেজিতে)
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  user_id = message.from_user.id

  if not check_user_subscription(user_id):
    bot.reply_to(
        message,
        "⚠️ Please join our private channels first to use the bot!\nThen"
        " type /start again.",
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
