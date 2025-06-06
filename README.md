# بوت الأذكار اليومية - صدقة جارية

بوت تيليجرام روحاني يرسل أذكارًا دينية بشكل دوري للمشتركين. استثمر في آخرتك من خلال المساهمة في نشر الذكر وتذكير الناس بالله عز وجل.

## 🌙 وصف البوت

بوت الأذكار اليومية يقوم بإرسال أذكار روحانية قصيرة بشكل عشوائي من قائمة محفوظة مسبقًا. يمكن للمستخدم اختيار الفترة الزمنية التي يرغب في استلام الأذكار خلالها:

- كل ربع ساعة
- كل ثلث ساعة (اختياري)
- كل نصف ساعة
- كل ساعة

## 📱 استخدام البوت

يمكنك تجربة البوت مباشرة من خلال الرابط التالي:
[https://t.me/Azkar_daily_bot](https://t.me/Azkar_daily_bot)

### خطوات الاستخدام:

1. افتح رابط البوت أو ابحث عن `@Azkar_daily_bot` في تيليجرام
2. اضغط على زر "ابدأ" أو أرسل `/start`
3. اختر نوع التذكير الذي تفضله من القائمة
4. اضغط على زر "✅ اشتراك" للاشتراك في الخدمة
5. بإمكانك إلغاء الاشتراك في أي وقت بالضغط على "❌ إلغاء الاشتراك"

## 🖥️ تشغيل البوت على منصة Pella

### المتطلبات الأساسية:

قبل البدء، تأكد من وجود الملفات التالية:
- `bot.py` (الملف الرئيسي للبوت)
- `requirements.txt` (قائمة المكتبات المطلوبة)

### خطوات التشغيل:

1. قم بإنشاء حساب على [منصة Pella](https://pella.app) إذا لم يكن لديك حساب
2. اضغط على "New Project" لإنشاء مشروع جديد
3. اختر "Telegram Bot" كنوع المشروع
4. قم بتحميل الملفات التالية:
   - `bot.py`
   - `requirements.txt`
5. أضف توكن البوت الخاص بك في ملف `bot.py` (يمكنك الحصول عليه من [@BotFather](https://t.me/BotFather))
6. اضغط على "Deploy" لتشغيل البوت

### مميزات تشغيل البوت على Pella:

- تشغيل متواصل على مدار الساعة
- تحديثات تلقائية في حال وجود تعديلات
- مراقبة أداء البوت واستخدامه
- سهولة التعامل مع المشاكل وتصحيحها

## ⚙️ إضافة ميزة "ذكر كل ثلث ساعة" (اختياري)

إذا أردت إضافة خيار "ذكر كل ثلث ساعة" (كل 20 دقيقة)، يمكنك اتباع الخطوات التالية:

1. افتح ملف `bot.py` في محرر النصوص
2. أضف متغير الملف الجديد بعد متغيرات الملفات الأخرى:
   ```python
   THIRD_HOUR_FILE = 'third_hour_subscribers.json'
   ```

3. أضف زر جديد في دالة `build_main_keyboard()`:
   ```python
   [KeyboardButton("🕒 ذكر الثلث ساعة")],
   ```

4. أضف معالج للزر الجديد في دالة `handle_message()`:
   ```python
   elif text == "🕒 ذكر الثلث ساعة":
       context.user_data["current_subscription"] = "third"
       await update.message.reply_text(
           "*ذكر كل ثلث ساعة*\n\n"
           "هذه الخدمة تقوم بإرسال ذكر روحاني عشوائي كل ثلث ساعة.\n"
           "الأوقات: 6:00، 6:20، 6:40، 7:00، وهكذا...\n\n"
           "هل ترغب في الاشتراك؟",
           reply_markup=build_subscription_keyboard("third"),
           parse_mode='Markdown'
       )
   ```

5. أضف معالجة الاشتراك وإلغاء الاشتراك في الأقسام المناسبة:
   ```python
   elif subscription_type == "third":
       file_name = THIRD_HOUR_FILE
       time_desc = "ثلث ساعة"
   ```

6. أضف جدولة للأذكار كل ثلث ساعة في دالة `schedule_messages()`:
   ```python
   # جدولة الأذكار كل ثلث ساعة
   for minute in ['00', '20', '40']:
       scheduler.add_job(
           send_scheduled_zikr,
           trigger='cron',
           hour='*',
           minute=minute,
           id=f"third_hour_{minute}",
           replace_existing=True,
           args=[app, THIRD_HOUR_FILE, "الثلث ساعة"]
       )
       print(f"تمت جدولة ذكر الثلث ساعة في الدقيقة {minute}")
   ```

7. قم بإعادة تشغيل البوت لتطبيق التغييرات

## 🤝 المساهمة

هذا البوت صدقة جارية، ونرحب بمساهمات الجميع لتحسينه وتطويره. يمكنك المساهمة عن طريق:

- إضافة أذكار جديدة
- تطوير ميزات جديدة
- نشر رابط البوت بين الأصدقاء والعائلة

## 📈 نصائح

- اشترك في البوت الرسمي [https://t.me/Azkar_daily_bot](https://t.me/Azkar_daily_bot) للاستفادة من التحديثات المستمرة
- شارك البوت مع من تحب لتحصل على أجر الدلالة على الخير
- لا تنس قراءة الأذكار اليومية بتدبر

---

*"من دلّ على خير فله مثل أجر فاعله"*
