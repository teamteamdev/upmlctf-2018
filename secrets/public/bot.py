#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# requires python-telegram-bot package from pip
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text("Hi! What's your secret?")


def help(bot, update):
    update.message.reply_text("Just send me secret and I won't tell it anybody")


def echo(bot, update):
    update.message.reply_text("Wow!")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater("686455660:AAGcg2Q5vn33z3ekMfC_QH5ERHDpf4GoGcI")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
