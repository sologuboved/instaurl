import time
import os
import sys
import requests
import re
from telegram.ext import Updater, MessageHandler, Filters
from tkn import TOKEN


def write_pid():
    prefix = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    previous_pid = find_previous_pid(prefix)
    if previous_pid:
        print("\nRemoving {}...".format(previous_pid))
        os.remove(previous_pid)
    pid_fname = '{}_{}.pid'.format(prefix, str(os.getpid()))
    print("Writing {}\n".format(pid_fname))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def delete_pid(pid_fname):
    try:
        os.remove(pid_fname)
    except FileNotFoundError as e:
        print(str(e))


def find_previous_pid(prefix):
    for fname in os.listdir('.'):
        if re.fullmatch(r'{}_\d+\.pid'.format(prefix), fname):
            return fname


def get_direct_link(page_link):
    return re.findall(r'{"src":"(.*?)","', str(requests.get(page_link).content))[-1].replace('\\\\u0026', '&')


def send_direct_link(update, context):
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
    updater = Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=send_direct_link))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # print(get_direct_link('https://www.instagram.com/p/B4VHea_I7bR/'))
    write_pid()
    main()
