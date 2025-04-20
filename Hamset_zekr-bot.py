import os
import json
import time
import threading
import random
import telebot
from datetime import datetime
from telebot import types

# تهيئة البوت باستخدام التوكن الخاص بك
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

# قائمة الأذكار الروحانية
SPIRITUAL_REMINDERS = [
    "سبحان الله وبحمده، سبحان الله العظيم",
    "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير",
    "اللهم صل على محمد وعلى آل محمد كما صليت على إبراهيم وعلى آل إبراهيم إنك حميد مجيد",
    "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
    "سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر",
    "لا حول ولا قوة إلا بالله العلي العظيم",
    "اللهم إني أسألك العفو والعافية في الدنيا والآخرة",
    "حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم",
    "اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت",
    "رب اغفر لي وتب علي إنك أنت التواب الرحيم"
]

# الفترات الزمنية المتاحة (بالثواني)
TIME_INTERVALS = {
    "15min": 15 * 60,
    "30min": 30 * 60,
    "60min": 60 * 60
}

# مسار ملف تخزين المشتركين
SUBSCRIBERS_FILE = "subscribers.json"

# هيكل بيانات المشتركين
subscribers = {}

# تحميل المشتركين من الملف
def load_subscribers():
    global subscribers
    if os.path.exists(SUBSCRIBERS_FILE):
        try:
            with open(SUBSCRIBERS_FILE, 'r', encoding='utf-8') as file:
                subscribers = json.load(file)
        except Exception as e:
            print(f"خطأ في تحميل ملف المشتركين: {e}")
            subscribers = {}
    else:
        subscribers = {}

# حفظ المشتركين في الملف
def save_subscribers():
    with open(SUBSCRIBERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(subscribers, file, ensure_ascii=False, indent=4)

# إضافة مشترك جديد
def add_subscriber(user_id, interval):
    user_id = str(user_id)  # تحويل المعرف إلى نص للتخزين في JSON
    subscribers[user_id] = {
        "interval": interval,
        "last_reminder_time": int(time.time())
    }
    save_subscribers()

# حذف مشترك
def remove_subscriber(user_id):
    user_id = str(user_id)
    if user_id in subscribers:
        del subscribers[user_id]
        save_subscribers()
        return True
    return False

# التحقق من وجود مشترك
def is_subscribed(user_id):
    return str(user_id) in subscribers

# تغيير الفترة الزمنية للمشترك
def change_interval(user_id, interval):
    user_id = str(user_id)
    if user_id in subscribers:
        subscribers[user_id]["interval"] = interval
        save_subscribers()
        return True
    return False

# الحصول على ذكر عشوائي
def get_random_reminder():
    return random.choice(SPIRITUAL_REMINDERS)

# رسالة الترحيب وإظهار القائمة الرئيسية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("الاشتراك في الأذكار ✨")
    btn2 = types.KeyboardButton("إلغاء الاشتراك ❌")
    btn3 = types.KeyboardButton("تغيير الفترة الزمنية ⏱")
    btn4 = types.KeyboardButton("ذكر عشوائي 🌟")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "أهلاً بك في بوت الأذكار الروحانية 🕌\n\n"
        "يمكنك الاشتراك للحصول على أذكار دورية بالفترة التي تناسبك.\n"
        "اختر من القائمة أدناه:",
        reply_markup=markup
    )

# معالجة طلب الاشتراك
@bot.message_handler(func=lambda message: message.text == "الاشتراك في الأذكار ✨")
def subscription_handler(message):
    if is_subscribed(message.chat.id):
        bot.send_message(message.chat.id, "أنت مشترك بالفعل في خدمة الأذكار. يمكنك تغيير الفترة الزمنية إذا أردت.")
        return
    
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btn1 = types.KeyboardButton("كل ربع ساعة")
    btn2 = types.KeyboardButton("كل نصف ساعة")
    btn3 = types.KeyboardButton("كل ساعة")
    btn4 = types.KeyboardButton("العودة للقائمة الرئيسية")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "اختر الفترة الزمنية المناسبة لاستلام الأذكار:",
        reply_markup=markup
    )

# معالجة اختيار الفترة الزمنية
@bot.message_handler(func=lambda message: message.text in ["كل ربع ساعة", "كل نصف ساعة", "كل ساعة"])
def interval_handler(message):
    interval_map = {
        "كل ربع ساعة": "15min",
        "كل نصف ساعة": "30min",
        "كل ساعة": "60min"
    }
    
    interval = interval_map[message.text]
    add_subscriber(message.chat.id, interval)
    
    # إعادة القائمة الرئيسية
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("الاشتراك في الأذكار ✨")
    btn2 = types.KeyboardButton("إلغاء الاشتراك ❌")
    btn3 = types.KeyboardButton("تغيير الفترة الزمنية ⏱")
    btn4 = types.KeyboardButton("ذكر عشوائي 🌟")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id, 
        f"تم اشتراكك بنجاح! ستصلك الأذكار {message.text}",
        reply_markup=markup
    )

# معالجة طلب إلغاء الاشتراك
@bot.message_handler(func=lambda message: message.text == "إلغاء الاشتراك ❌")
def unsubscribe_handler(message):
    if not is_subscribed(message.chat.id):
        bot.send_message(message.chat.id, "أنت غير مشترك في خدمة الأذكار حاليًا.")
        return
    
    if remove_subscriber(message.chat.id):
        bot.send_message(message.chat.id, "تم إلغاء اشتراكك بنجاح.")
    else:
        bot.send_message(message.chat.id, "حدث خطأ أثناء إلغاء الاشتراك. الرجاء المحاولة مرة أخرى.")

# معالجة طلب تغيير الفترة الزمنية
@bot.message_handler(func=lambda message: message.text == "تغيير الفترة الزمنية ⏱")
def change_interval_handler(message):
    if not is_subscribed(message.chat.id):
        bot.send_message(message.chat.id, "أنت غير مشترك في خدمة الأذكار حاليًا. يرجى الاشتراك أولاً.")
        return
    
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btn1 = types.KeyboardButton("كل ربع ساعة")
    btn2 = types.KeyboardButton("كل نصف ساعة")
    btn3 = types.KeyboardButton("كل ساعة")
    btn4 = types.KeyboardButton("العودة للقائمة الرئيسية")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "اختر الفترة الزمنية الجديدة لاستلام الأذكار:",
        reply_markup=markup
    )

# معالجة طلب ذكر عشوائي
@bot.message_handler(func=lambda message: message.text == "ذكر عشوائي 🌟")
def random_reminder_handler(message):
    reminder = get_random_reminder()
    bot.send_message(message.chat.id, f"✨ {reminder} ✨")

# معالجة طلب العودة للقائمة الرئيسية
@bot.message_handler(func=lambda message: message.text == "العودة للقائمة الرئيسية")
def back_to_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("الاشتراك في الأذكار ✨")
    btn2 = types.KeyboardButton("إلغاء الاشتراك ❌")
    btn3 = types.KeyboardButton("تغيير الفترة الزمنية ⏱")
    btn4 = types.KeyboardButton("ذكر عشوائي 🌟")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "القائمة الرئيسية:",
        reply_markup=markup
    )

# وظيفة إرسال الأذكار الدورية للمشتركين
def send_reminders():
    while True:
        current_time = int(time.time())
        
        for user_id, user_data in list(subscribers.items()):
            interval_seconds = TIME_INTERVALS[user_data["interval"]]
            last_reminder_time = user_data["last_reminder_time"]
            
            if current_time - last_reminder_time >= interval_seconds:
                try:
                    reminder = get_random_reminder()
                    bot.send_message(int(user_id), f"🕌 ذكر روحاني لك: \n\n✨ {reminder} ✨")
                    subscribers[user_id]["last_reminder_time"] = current_time
                    save_subscribers()
                except Exception as e:
                    print(f"خطأ في إرسال الذكر للمستخدم {user_id}: {e}")
        
        # تقليل استهلاك المعالج
        time.sleep(10)

# تحميل المشتركين عند بدء البوت
load_subscribers()

# بدء خيط لإرسال الأذكار
reminder_thread = threading.Thread(target=send_reminders)
reminder_thread.daemon = True
reminder_thread.start()

# معلومات إضافية للمستخدم
print("تم تشغيل بوت الأذكار الروحانية!")
print("اضغط على Ctrl+C لإيقاف البوت")

# تشغيل البوت
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"حدث خطأ في تشغيل البوت: {e}")
