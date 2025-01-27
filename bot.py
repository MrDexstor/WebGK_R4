import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebGK.settings")
django.setup()

from Core.config import TELEGRAM_BOT_TOKEN
from TelegramBot.registration.handler import registration_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(registration_handler())
    application.run_polling()

if __name__ == '__main__':
    main()
