import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

# ضع هنا التوكن الخاص بالبوت
TOKEN = os.environ.get('TOKEN')

# وظيفة الترحيب عند بدء المحادثة مع البوت
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send me a link from YouTube, Instagram, Facebook, TikTok, and more!")

# وظيفة لتحميل الفيديو
def download_video(url, format='mp4'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# وظيفة التعامل مع الرسائل التي تحتوي على الروابط
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        # تحميل الفيديو
        file_path = download_video(url)

        # إرسال الفيديو للمستخدم
        with open(file_path, 'rb') as file:
            update.message.reply_video(video=file)

        # حذف الملف بعد الإرسال
        os.remove(file_path)

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# الوظيفة الرئيسية لتشغيل البوت
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # إضافة أوامر البوت
    dispatcher.add_handler(CommandHandler("start", start))

    # التعامل مع الرسائل النصية
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
