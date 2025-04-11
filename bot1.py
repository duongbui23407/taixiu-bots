import telebot
import json
import os

TOKEN = "7533530454:AAFRLM4_09LCJaXBSf5yLlv9cgpyMzWc0vk"
bot = telebot.TeleBot(TOKEN)

KEYS_PATH = os.path.join(os.path.dirname(__file__), "keys.json")

if not os.path.exists(KEYS_PATH):
    with open(KEYS_PATH, "w") as f:
        json.dump({"keys": []}, f)

def load_keys():
    try:
        with open(KEYS_PATH, "r") as f:
            data = json.load(f)
            return data.get("keys", [])
    except Exception as e:
        print("❌ Lỗi khi đọc file keys.json:", e)
        return []

def save_keys(keys):
    try:
        with open(KEYS_PATH, "w") as f:
            json.dump({"keys": keys}, f, indent=2)
    except Exception as e:
        print("❌ Lỗi khi ghi keys.json:", e)

@bot.message_handler(commands=["add"])
def add_key(message):
    key = message.text.replace("/add", "").strip()
    keys = load_keys()
    if key and key not in keys:
        keys.append(key)
        save_keys(keys)
        bot.send_message(message.chat.id,
                         f"✅ Đã thêm key: `{key}`",
                         parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id,
                         "❌ Key đã tồn tại hoặc không hợp lệ.")

@bot.message_handler(commands=["del"])
def del_key(message):
    key = message.text.replace("/del", "").strip()
    keys = load_keys()
    if key in keys:
        keys.remove(key)
        save_keys(keys)
        bot.send_message(message.chat.id,
                         f"🗑️ Đã xóa key: `{key}`",
                         parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ Key không tồn tại.")

@bot.message_handler(commands=["list"])
def list_keys(message):
    keys = load_keys()
    if keys:
        bot.send_message(message.chat.id,
                         "📋 Danh sách key:
" + "\n".join(keys))
    else:
        bot.send_message(message.chat.id, "📭 Không có key nào.")

print("🚀 Bot 1 (quản lý key) đang chạy...")
bot.polling()
