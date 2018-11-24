import time
import os
import sys
import requests
import re
from telegram.ext import Updater, MessageHandler, Filters
from tkn import TOKEN


def write_pid():
    pid_fname = '{}_{}.pid'.format(os.path.splitext(os.path.basename(sys.argv[0]))[0], str(os.getpid()))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def get_direct_link(page_link):
    return re.findall(r'"src":"(https://.+?\.jpg)"', str(requests.get(page_link).content))[0]


def send_direct_link(bot, update):
    page_link = update.message.text
    time.sleep(3)
    try:
        message = get_direct_link(page_link)
    except Exception as e:
        message = str(e)
    update.message.reply_text(message, disable_web_page_preview=True)


def main():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=send_direct_link))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    write_pid()
    main()
