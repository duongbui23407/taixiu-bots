import telebot
import json
import os

TOKEN = "7427700531:AAHMOxRzaG3-th5ixUWuXE7as3jYnnlS7K4"
bot = telebot.TeleBot(TOKEN)

KEYS_PATH = os.path.join(os.path.dirname(__file__), "keys.json")

def load_keys():
    if not os.path.exists(KEYS_PATH):
        print("⚠️ Chưa có file keys.json. Hãy tạo file này trước.")
        return []
    try:
        with open(KEYS_PATH, "r") as f:
            data = json.load(f)
            return data.get("keys", [])
    except Exception as e:
        print("❌ Lỗi khi đọc keys.json:", e)
        return []

def calculate_probabilities(md5_str):
    if len(md5_str) != 32:
        return None, "❌ Mã MD5 không hợp lệ. Vui lòng nhập đủ 32 ký tự."
    last5 = md5_str[-5:]
    total = sum(int(c, 16) for c in last5)
    tai = total
    xiu = 80 - total
    tai_p = round(tai / 80 * 100, 2)
    xiu_p = round(xiu / 80 * 100, 2)
    should_play = "🎯 Tài" if tai_p > xiu_p else "🎯 Xỉu"
    return {
        "md5": md5_str,
        "last5": last5,
        "total": total,
        "tai_percent": tai_p,
        "xiu_percent": xiu_p,
        "should_play": should_play
    }, None

active_users = {}

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "🔑 Vui lòng gửi key để xác thực:")

@bot.message_handler(func=lambda message: True)
def process(message):
    user_id = message.chat.id
    text = message.text.strip()
    if user_id not in active_users:
        keys = load_keys()
        if text in keys:
            active_users[user_id] = True
            bot.send_message(user_id, "✅ Xác thực thành công! Gửi mã MD5 để phân tích.")
            print(f"[+] Người dùng {user_id} xác thực thành công với key: {text}")
        else:
            bot.send_message(user_id, "❌ Key không hợp lệ. Vui lòng thử lại.")
    else:
        result, error = calculate_probabilities(text)
        if error:
            bot.send_message(user_id, error)
        else:
            bot.send_message(user_id, (
                f"🔍 Mã MD5: `{result['md5']}`\n"
                f"🧩 5 ký tự cuối: `{result['last5']}`\n"
                f"➕ Tổng: `{result['total']}`\n\n"
                f"📊 Xác suất:\n"
                f"🔴 Tài: `{result['tai_percent']}%`\n"
                f"🔵 Xỉu: `{result['xiu_percent']}%`\n\n"
                f"🎲 Dự đoán xúc xắc: {result['should_play']}\n"
                f"💡 Tỉ lệ ăn cao: {max(result['tai_percent'], result['xiu_percent'])}%\n"
                f"✅ Nên đánh: {result['should_play']}"
            ), parse_mode="Markdown")

bot.polling()
