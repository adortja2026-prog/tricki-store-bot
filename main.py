import json
import os
import telebot
from flask import Flask, request

# আপনার টেলিগ্রাম বট টোকেন এবং অ্যাডমিন আইডি
TOKEN = "8912797126:AAF6EFSQZU-tySXsGl1t__AAT-7oAc2MDp8"
ADMIN_ID = 7559861666

# আপনার চ্যানেলের চ্যাট আইডি এবং ইনভাইট লিংক
CHANNEL_ID = -1004343769999
CHANNEL_INVITE_LINK = "https://t.me/+8DV9O3hNpWtlMWM1"

# আপনার রেন্ডার অ্যাপের আসল পাবলিক লিংক এখানে বসানো হলো
RENDER_URL = "https://tricki-store-bot.onrender.com"

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "keywords.json"

app = Flask(__name__)

# ডাটা লোড ও সেভ করার ফাংশন
def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {"freeky": "✨ Your Free Key or post will appear here."}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ইউজার চ্যানেলে জয়েন আছে কিনা চেক করার ফাংশন
def check_user_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Error checking subscription: {e}")
    return False


# ১. /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if not check_user_subscription(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_channel = telebot.types.InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_INVITE_LINK)
        btn_check = telebot.types.InlineKeyboardButton("🔄 Check Again", callback_data="check_sub")
        markup.add(btn_channel)
        markup.add(btn_check)
        
        bot.reply_to(message, "❌ **Sorry!** To use this bot, you must join our channel first!\n\n👉 After joining the channel, click the **'Check Again'** button below.", parse_mode="Markdown", reply_markup=markup)
        return

    send_main_menu_message(message)


def send_main_menu_message(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_freeky = telebot.types.InlineKeyboardButton("🎁 Free Key", callback_data="btn_freeky")
    btn_8ball = telebot.types.InlineKeyboardButton("🎱 8 Ball Pool Hack", callback_data="btn_8ball_pool")
    markup.add(btn_freeky, btn_8ball)
    
    welcome_text = (
        "🎉 **Congratulations!**\n"
        "✅ **You have successfully joined the channel and now you can use this bot!**\n\n"
        "✨ Choose your preferred option from the buttons below:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)


def edit_to_main_menu(call):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_freeky = telebot.types.InlineKeyboardButton("🎁 Free Key", callback_data="btn_freeky")
    btn_8ball = telebot.types.InlineKeyboardButton("🎱 8 Ball Pool Hack", callback_data="btn_8ball_pool")
    markup.add(btn_freeky, btn_8ball)
    
    welcome_text = (
        "🎉 **Congratulations!**\n"
        "✅ **Subscription verified successfully! You can now use the bot.**\n\n"
        "✨ Choose an option below:"
    )
    bot.edit_message_text(welcome_text, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)


# ২. সাবস্ক্রিপশন চেক কলব্যাক
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check_sub(call):
    user_id = call.from_user.id
    if check_user_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ Verified successfully!")
        edit_to_main_menu(call)
    else:
        bot.answer_callback_query(call.id, "❌ You haven't joined the channel yet! Please join first.", show_alert=True)


# ৩. ইনলাইন বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data in ["btn_freeky", "btn_8ball_pool", "os_android", "os_ios", "back_to_main"])
def handle_inline_buttons(call):
    chat_id = call.message.chat.id
    
    if call.data == "btn_freeky":
        data = load_data()
        free_code = data.get("freeky", "⚠️ No free key is currently set.")
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, f"🔑 **Free Key Information:**\n\n{free_code}", parse_mode="Markdown")

    elif call.data == "btn_8ball_pool":
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn_android = telebot.types.InlineKeyboardButton("🤖 Android", callback_data="os_android")
        btn_ios = telebot.types.InlineKeyboardButton("🍏 iOS (Apple)", callback_data="os_ios")
        btn_back = telebot.types.InlineKeyboardButton("🔙 Go Back", callback_data="back_to_main")
        markup.add(btn_android, btn_ios)
        markup.add(btn_back)
        
        bot.edit_message_text("🎱 You selected **8 Ball Pool Hack**.\n\n📱 Please select your device operating system:", 
                              chat_id=chat_id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data in ["os_android", "os_ios"]:
        os_name = "🤖 **Android Version**" if call.data == "os_android" else "🍏 **iOS (Apple) Version**"
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔙 Go Back", callback_data="btn_8ball_pool"))
        
        price_text = (
            f"🎉 **Dussehra Special Offer ({os_name})** 🎁\n\n"
            "This Dussehra, enjoy some extra days with every subscription at no additional cost!\n\n"
            "🎁 Buy a 3-day subscription, get 1 free day — **4 days in total. - 6$**\n"
            "🎁 Buy a 7-day subscription, get 3 free days — **10 days in total. - 10$**\n"
            "🎁 Buy a 15-day subscription, get 5 free days — **20 days in total. - 17$**\n"
            "🎁 Buy a 30-day subscription, get 10 free days — **40 days in total. - 30$**\n\n"
            "⏳ **Offer is available for a limited time.**\n\n"
            "🛒 **To purchase a key, contact our authorized sellers: @Adorkuro**"
        )
        
        bot.edit_message_text(price_text, chat_id=chat_id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "back_to_main":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn_freeky = telebot.types.InlineKeyboardButton("🎁 Free Key", callback_data="btn_freeky")
        btn_8ball = telebot.types.InlineKeyboardButton("🎱 8 Ball Pool Hack", callback_data="btn_8ball_pool")
        markup.add(btn_freeky, btn_8ball)
        
        bot.edit_message_text("🎉 **Welcome back to the main menu!**\n\n✨ Choose an option below:", 
                              chat_id=chat_id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)


# ৪. অ্যাডমিন কমান্ড: নতুন কোড সেট করার জন্য
@bot.message_handler(commands=['setcode'])
def set_new_code(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Sorry, this command can only be used by the admin!")
        return

    text_parts = message.text.split(maxsplit=2)
    if len(text_parts) < 3:
        bot.reply_to(message, "⚠️ **Use the correct format. Example:**\n`/setcode freeky your_new_code`", parse_mode="Markdown")
        return

    keyword = text_parts[1].lower()
    new_code_text = text_parts.2 if len(text_parts) > 2 else ""

    data = load_data()
    data[keyword] = new_code_text
    save_data(data)

    bot.reply_to(message, f"✅ **Success!** New code set for keyword '{keyword}':\n\n{new_code_text}", parse_mode="Markdown")


# ৫. সাধারণ ইউজার টেক্সট হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def keyword_responder(message):
    user_id = message.from_user.id

    if not check_user_subscription(user_id):
        bot.reply_to(message, "❌ To use the bot, you must join our channel first! Type `/start` and try again.", parse_mode="Markdown")
        return

    user_text = message.text.strip().lower()
    data = load_data()

    if user_text in data:
        bot.reply_to(message, f"✨ **Your requested information:**\n\n{data[user_text]}", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❓ Sorry, nothing found with this keyword. Or type `/start` to view the menu.", parse_mode="Markdown")


# ফ্লাস্ক ওয়েবਹੁক রুট (Webhook Route)
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid Data", 403

@app.route('/')
def index():
    return "Bot is running with Webhook!"


if __name__ == '__main__':
    # ওয়েবਹੁক অটো সেটআপ করা
    bot.remove_webhook()
    bot.set_webhook(url=f'{RENDER_URL}/{TOKEN}')
    
    app.run(host='0.0.0.0', port=8080)
