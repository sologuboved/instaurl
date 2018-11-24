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

    if 'instagram' in page_link:
        try:
            message = get_direct_link(page_link)
        except Exception as e:
            print("{}: {} @ {}".format(type(e).__name__, e, page_link))
            message = "Something is off either with your link, or my code. I'll look into this."
    else:
        print("Some nonsense:", page_link)
        message = "This is not an instagram link that you are requesting."

    update.message.reply_text(message, disable_web_page_preview=True)


def main():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=send_direct_link))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    write_pid()
    main()
