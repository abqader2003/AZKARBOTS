import json
import os
import asyncio
import nest_asyncio
import random
from telegram import ReplyKeyboardMarkup, Update, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# تطبيق nest_asyncio لتجنب مشاكل التزامن في بيئات مثل Pella
nest_asyncio.apply()

# توكن البوت - يمكنك تغييره
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# قائمة الأذكار
azkar = [
    "سبحان الله وبحمده، سبحان الله العظيم",
    "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير",
    "اللهم صل على محمد وعلى آل محمد كما صليت على إبراهيم وعلى آل إبراهيم إنك حميد مجيد",
    "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
    "لا حول ولا قوة إلا بالله العلي العظيم",
    "سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر",
    "اللهم إني أسألك العفو والعافية في الدنيا والآخرة",
    "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي",
    "اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت",
    "حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم"
]

# أسماء ملفات المشتركين
QUARTER_HOUR_FILE = 'quarter_hour_subscribers.json'
HALF_HOUR_FILE = 'half_hour_subscribers.json'
HOUR_FILE = 'hour_subscribers.json'

# إنشاء المجلدات اللازمة
def ensure_directories():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/subscribers"):
        os.makedirs("data/subscribers")

# قراءة المشتركين من ملف
def load_subscribers(file_name):
    file_path = f'data/subscribers/{file_name}'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# حفظ المشتركين في ملف
def save_subscribers(subscribers, file_name):
    file_path = f'data/subscribers/{file_name}'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(subscribers, file, ensure_ascii=False, indent=4)

# إرسال ذكر عشوائي للمشتركين
async def send_scheduled_zikr(app, file_name, time_type):
    subscribers = load_subscribers(file_name)
    if not subscribers:
        print(f"لا يوجد مشتركين في {time_type}")
        return
    
    random_zikr = random.choice(azkar)
    current_time = datetime.now().strftime("%H:%M")
    
    print(f"جاري إرسال ذكر {time_type} في الساعة {current_time} إلى {len(subscribers)} مشترك...")
    
    for user_id in subscribers:
        try:
            await app.bot.send_message(
                chat_id=user_id,
                text=f"🕌 *ذكر الساعة {current_time}*\n\n{random_zikr}",
                parse_mode='Markdown'
            )
            print(f"تم إرسال الذكر إلى المستخدم {user_id}")
        except Exception as e:
            print(f"خطأ في إرسال الذكر للمستخدم {user_id}: {e}")

# إنشاء لوحة المفاتيح الرئيسية
def build_main_keyboard():
    keyboard = [
        [KeyboardButton("🕒 ذكر الربع ساعة")],
        [KeyboardButton("🕒 ذكر النصف ساعة")],
        [KeyboardButton("🕒 ذكر الساعة")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# إنشاء لوحة مفاتيح فرعية للاشتراك
def build_subscription_keyboard(subscription_type):
    keyboard = [
        [KeyboardButton("✅ اشتراك")],
        [KeyboardButton("❌ إلغاء الاشتراك")],
        [KeyboardButton("🔙 رجوع للقائمة")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# معالج أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    first_name = update.effective_user.first_name
    
    await update.message.reply_text(
        f"السلام عليكم {first_name}! 🌙\n\n"
        "مرحبًا بك في بوت الأذكار الروحاني.\n"
        "اختر من القائمة أدناه طريقة استلام الأذكار.",
        reply_markup=build_main_keyboard()
    )

# معالج الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التحقق من وجود الرسالة
    if not update.message or not update.message.text:
        return
    
    user_id = update.effective_chat.id
    text = update.message.text
    
    # معالجة اختيارات القائمة الرئيسية
    if text == "🕒 ذكر الربع ساعة":
        context.user_data["current_subscription"] = "quarter"
        await update.message.reply_text(
            "*ذكر كل ربع ساعة*\n\n"
            "هذه الخدمة تقوم بإرسال ذكر روحاني عشوائي كل ربع ساعة.\n"
            "الأوقات: 6:00، 6:15، 6:30، 6:45، 7:00، وهكذا...\n\n"
            "هل ترغب في الاشتراك؟",
            reply_markup=build_subscription_keyboard("quarter"),
            parse_mode='Markdown'
        )
    
    elif text == "🕒 ذكر النصف ساعة":
        context.user_data["current_subscription"] = "half"
        await update.message.reply_text(
            "*ذكر كل نصف ساعة*\n\n"
            "هذه الخدمة تقوم بإرسال ذكر روحاني عشوائي كل نصف ساعة.\n"
            "الأوقات: 6:00، 6:30، 7:00، 7:30، وهكذا...\n\n"
            "هل ترغب في الاشتراك؟",
            reply_markup=build_subscription_keyboard("half"),
            parse_mode='Markdown'
        )
    
    elif text == "🕒 ذكر الساعة":
        context.user_data["current_subscription"] = "hour"
        await update.message.reply_text(
            "*ذكر كل ساعة*\n\n"
            "هذه الخدمة تقوم بإرسال ذكر روحاني عشوائي كل ساعة.\n"
            "الأوقات: 6:00، 7:00، 8:00، وهكذا...\n\n"
            "هل ترغب في الاشتراك؟",
            reply_markup=build_subscription_keyboard("hour"),
            parse_mode='Markdown'
        )
    
    # معالجة عمليات الاشتراك
    elif text == "✅ اشتراك" and "current_subscription" in context.user_data:
        subscription_type = context.user_data["current_subscription"]
        
        if subscription_type == "quarter":
            file_name = QUARTER_HOUR_FILE
            time_desc = "ربع ساعة"
        elif subscription_type == "half":
            file_name = HALF_HOUR_FILE
            time_desc = "نصف ساعة"
        else:  # hour
            file_name = HOUR_FILE
            time_desc = "ساعة"
        
        # قراءة المشتركين وإضافة المستخدم الحالي
        subscribers = load_subscribers(file_name)
        user_id_str = str(user_id)
        
        if user_id_str in subscribers:
            await update.message.reply_text(
                f"أنت مشترك بالفعل في خدمة الأذكار كل {time_desc}.",
                reply_markup=build_subscription_keyboard(subscription_type)
            )
        else:
            subscribers.append(user_id_str)
            save_subscribers(subscribers, file_name)
            await update.message.reply_text(
                f"✅ تم اشتراكك بنجاح في خدمة الأذكار كل {time_desc}.\n\n"
                "ستصلك الأذكار في الأوقات المحددة إن شاء الله.",
                reply_markup=build_subscription_keyboard(subscription_type)
            )
    
    # معالجة عمليات إلغاء الاشتراك
    elif text == "❌ إلغاء الاشتراك" and "current_subscription" in context.user_data:
        subscription_type = context.user_data["current_subscription"]
        
        if subscription_type == "quarter":
            file_name = QUARTER_HOUR_FILE
            time_desc = "ربع ساعة"
        elif subscription_type == "half":
            file_name = HALF_HOUR_FILE
            time_desc = "نصف ساعة"
        else:  # hour
            file_name = HOUR_FILE
            time_desc = "ساعة"
        
        # قراءة المشتركين وإزالة المستخدم الحالي
        subscribers = load_subscribers(file_name)
        user_id_str = str(user_id)
        
        if user_id_str in subscribers:
            subscribers.remove(user_id_str)
            save_subscribers(subscribers, file_name)
            await update.message.reply_text(
                f"❌ تم إلغاء اشتراكك في خدمة الأذكار كل {time_desc}.",
                reply_markup=build_subscription_keyboard(subscription_type)
            )
        else:
            await update.message.reply_text(
                f"أنت غير مشترك في خدمة الأذكار كل {time_desc}.",
                reply_markup=build_subscription_keyboard(subscription_type)
            )
    
    # العودة للقائمة الرئيسية
    elif text == "🔙 رجوع للقائمة":
        if "current_subscription" in context.user_data:
            del context.user_data["current_subscription"]
        await update.message.reply_text(
            "القائمة الرئيسية",
            reply_markup=build_main_keyboard()
        )
    
    # رسالة افتراضية لأي مدخلات أخرى
    else:
        await update.message.reply_text(
            "🤔 عذرًا، لم أفهم الأمر.\n"
            "يرجى اختيار إحدى الخيارات من القائمة.",
            reply_markup=build_main_keyboard()
        )

# جدولة الرسائل
def schedule_messages(app, scheduler):
    # جدولة الأذكار كل ربع ساعة
    for minute in ['00', '15', '30', '45']:
        scheduler.add_job(
            send_scheduled_zikr,
            trigger='cron',
            hour='*',
            minute=minute,
            id=f"quarter_hour_{minute}",
            replace_existing=True,
            args=[app, QUARTER_HOUR_FILE, "الربع ساعة"]
        )
        print(f"تمت جدولة ذكر الربع ساعة في الدقيقة {minute}")
    
    # جدولة الأذكار كل نصف ساعة
    for minute in ['00', '30']:
        scheduler.add_job(
            send_scheduled_zikr,
            trigger='cron',
            hour='*',
            minute=minute,
            id=f"half_hour_{minute}",
            replace_existing=True,
            args=[app, HALF_HOUR_FILE, "النصف ساعة"]
        )
        print(f"تمت جدولة ذكر النصف ساعة في الدقيقة {minute}")
    
    # جدولة الأذكار كل ساعة
    scheduler.add_job(
        send_scheduled_zikr,
        trigger='cron',
        hour='*',
        minute='00',
        id="hour_00",
        replace_existing=True,
        args=[app, HOUR_FILE, "الساعة"]
    )
    print("تمت جدولة ذكر الساعة")

# معالج الأخطاء
async def error_handler(update, context):
    print(f"حدث خطأ: {context.error}")

# الدالة الرئيسية
async def main():
    # التأكد من وجود المجلدات اللازمة
    ensure_directories()
    
    # إنشاء تطبيق البوت
    app = ApplicationBuilder().token(TOKEN).build()
    
    # إضافة معالج الأخطاء
    app.add_error_handler(error_handler)
    
    # إنشاء المجدول
    scheduler = AsyncIOScheduler()
    
    # إضافة معالجات الأوامر والرسائل
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # جدولة الرسائل
    schedule_messages(app, scheduler)
    scheduler.start()
    
    print("🚀 البوت قيد التشغيل...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
