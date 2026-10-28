import json
import os
import telebot

# আপনার বটের টোকেন এবং অ্যাডমিন আইডি
TOKEN = "8912797126:AAEo6jGLJzNelJtMM3t3iZ9FEDqlMmo8gl0"
ADMIN_ID = 7559861666

# আপনার চ্যানেলের চ্যাট আইডি এবং ইনভাইট লিংক
CHANNEL_ID = -1004343769999
CHANNEL_INVITE_LINK = "https://t.me/+8DV9O3hNpWtlMWM1"

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "keywords.json"

# ডাটা লোড ও সেভ করার ফাংশন
def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {"freeky": "✨ **আপনার ফ্রি কি (Free Key) বা পোস্ট এখানে থাকবে।**"}
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


# ১. /start কমান্ড হ্যান্ডলার (চ্যানেল চেক + মেইন মেনু বাটন)
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if not check_user_subscription(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_channel = telebot.types.InlineKeyboardButton("📢 **আমাদের চ্যানেলে জয়েন করুন**", url=CHANNEL_INVITE_LINK)
        btn_check = telebot.types.InlineKeyboardButton("🔄 **আবার চেক করুন**", callback_data="check_sub")
        markup.add(btn_channel)
        markup.add(btn_check)
        
        bot.reply_to(message, "❌ **দুঃখিত!** বটটি ব্যবহার করতে হলে প্রথমে অবশ্যই আমাদের চ্যানেলে জয়েন করতে হবে!\n\n👉 চ্যানেলে জয়েন করার পর নিচের **'আবার চেক করুন'** বাটনে ক্লিক করুন।", parse_mode="Markdown", reply_markup=markup)
        return

    send_main_menu(message)


# মূল মেনু দেখানোর ফাংশন
def send_main_menu(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    btn_freeky = telebot.types.InlineKeyboardButton("🎁 **ফ্রি কি (Free Key)**", callback_data="btn_freeky")
    btn_8ball = telebot.types.InlineKeyboardButton("🎱 **8 Ball Pool Hack**", callback_data="btn_8ball_pool")
    
    markup.add(btn_freeky, btn_8ball)
    
    welcome_text = (
        "👋 **স্বাগতম আমাদের বটে!**\n\n"
        "✨ নিচে দেওয়া অপশনগুলো থেকে আপনার পছন্দের বাটনটি বেছে নিন:"
    )
    
    if isinstance(message, telebot.types.CallbackQuery):
        bot.send_message(message.message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=markup)


# ২. সাবস্ক্রিপশন চেক কলব্যাক
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check_sub(call):
    user_id = call.from_user.id
    if check_user_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ ধন্যবাদ! আপনার সাবস্ক্রিপশন যাচাই সফল হয়েছে।")
        send_main_menu(call)
    else:
        bot.answer_callback_query(call.id, "❌ আপনি এখনো চ্যানেলে জয়েন করেননি!", show_alert=True)


# ৩. ইনলাইন বাটন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data in ["btn_freeky", "btn_8ball_pool", "os_android", "os_ios", "back_to_main"])
def handle_inline_buttons(call):
    chat_id = call.message.chat.id
    
    # ফ্রি কি বাটন চাপলে
    if call.data == "btn_freeky":
        data = load_data()
        free_code = data.get("freeky", "⚠️ এই মুহূর্তে কোনো ফ্রি কি সেট করা নেই।")
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, f"🔑 **ফ্রি কি তথ্য:**\n\n{free_code}", parse_mode="Markdown")

    # 8 Ball Pool Hack বাটন চাপলে (OS সিলেক্ট করার অপশন)
    elif call.data == "btn_8ball_pool":
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn_android = telebot.types.InlineKeyboardButton("🤖 **Android**", callback_data="os_android")
        btn_ios = telebot.types.InlineKeyboardButton("🍏 **iOS (Apple)**", callback_data="os_ios")
        btn_back = telebot.types.InlineKeyboardButton("🔙 **ফিরে যান**", callback_data="back_to_main")
        markup.add(btn_android, btn_ios)
        markup.add(btn_back)
        
        bot.edit_message_text("🎱 **8 Ball Pool Hack** সিলেক্ট করেছেন।\n\n📱 আপনার ডিভাইসটি কোন অপারেটিং সিস্টেমের তা সিলেক্ট করুন:", 
                              chat_id=chat_id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # অ্যান্ড্রয়েড ও আইওএস উভয়ের জন্য প্রাইস লিস্ট
    elif call.data in ["os_android", "os_ios"]:
        os_name = "🤖 **Android Version**" if call.data == "os_android" else "🍏 **iOS (Apple) Version**"
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🔙 **পেছনে যান**", callback_data="btn_8ball_pool"))
        
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

    # মূল মেনুতে ফিরে যাওয়ার জন্য
    elif call.data == "back_to_main":
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        btn_freeky = telebot.types.InlineKeyboardButton("🎁 **ফ্রি কি (Free Key)**", callback_data="btn_freeky")
        btn_8ball = telebot.types.InlineKeyboardButton("🎱 **8 Ball Pool Hack**", callback_data="btn_8ball_pool")
        markup.add(btn_freeky, btn_8ball)
        
        bot.edit_message_text("👋 **মূল মেনুতে স্বাগতম!**\n\n✨ নিচে দেওয়া অপশনগুলো থেকে বেছে নিন:", 
                              chat_id=chat_id, message_id=call.message.message_id, parse_mode="Markdown", reply_markup=markup)


# ৪. অ্যাডমিন কমান্ড: নতুন কোড সেট করার জন্য
@bot.message_handler(commands=['setcode'])
def set_new_code(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ দুঃখিত, এই কমান্ডটি শুধু অ্যাডমিন ব্যবহার করতে পারবেন!")
        return

    text_parts = message.text.split(maxsplit=2)
    if len(text_parts) < 3:
        bot.reply_to(message, "⚠️ **সঠিক নিয়মে লিখুন। যেমন:**\n`/setcode freeky আপনার_নতুন_কোড`", parse_mode="Markdown")
        return

    keyword = text_parts[1].lower()
    new_code_text = text_parts[2]

    data = load_data()
    data[keyword] = new_code_text
    save_data(data)

    bot.reply_to(message, f"✅ **সফল!** '{keyword}' কি-ওয়ার্ডের নতুন কোড সেট করা হয়েছে:\n\n{new_code_text}", parse_mode="Markdown")


# ৫. সাধারণ ইউজার টেক্সট হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def keyword_responder(message):
    user_id = message.from_user.id

    if not check_user_subscription(user_id):
        bot.reply_to(message, "❌ বট ব্যবহার করতে হলে প্রথমে আমাদের চ্যানেলে জয়েন করতে হবে! `/start` লিখে আবার চেষ্টা করুন।", parse_mode="Markdown")
        return

    user_text = message.text.strip().lower()
    data = load_data()

    if user_text in data:
        bot.reply_to(message, f"✨ **আপনার কাঙ্ক্ষিত তথ্য:**\n\n{data[user_text]}", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❓ দুঃখিত, এই কি-ওয়ার্ড দিয়ে কিছু পাওয়া যায়নি। অথবা মেনু দেখতে `/start` কমান্ড দিন।", parse_mode="Markdown")

# বট রান করার জন্য
if __name__ == '__main__':
    print("Bot is running with Dussehra Offer Price Lists & Buttons...")
    bot.infinity_polling()
