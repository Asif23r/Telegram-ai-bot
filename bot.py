import telebot
import openai

# ==== CONFIGURATION ====
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
OWNER_ID = 123456789  # replace with your Telegram user ID
# ========================

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hey! I’m your friendly AI chatbot. Ask me anything!")

# Broadcast command (Only for Owner)
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != OWNER_ID:
        return bot.reply_to(message, "⛔️ You are not allowed to use this command.")
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        return bot.reply_to(message, "⚠️ Usage: /broadcast Your message here")
    
    sent_count = 0
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 Broadcast:\n{text}")
            sent_count += 1
        except:
            pass
    bot.reply_to(message, f"✅ Sent to {sent_count} users.")

# Store user IDs
users = set()

# AI Chat response
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    users.add(message.chat.id)

    prompt = message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, f"🤖 {reply}")
    except Exception as e:
        bot.reply_to(message, "❌ Sorry, I couldn't process that.")

# Start polling
bot.infinity_polling()