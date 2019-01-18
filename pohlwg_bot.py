##import json 
##import requests
##import time
##import urllib #solves problems with symbols having special meanings in URL context (?&+)
##

##
##import telegram
##
##from telegram import ReplyKeyboardMarkup, KeyboardButton
##
##
##TOKEN = "435982196:AAGg10t81vJUUygSTVJQ-xYR94bcQEOqv0E"
##URL = "https://api.telegram.org/bot{}/".format(TOKEN)
##
##

##
###dowloads contents of URL and returns string
##def get_url(url):   
##    response = requests.get(url)
##    content = response.content.decode("utf8")
##    return content
##
###parses sting into Python dictionary (Telegram always gives JSON response)
##def get_json_from_url(url):
##    content = get_url(url)
##    js = json.loads(content)
##    return js
##
##
##def get_updates(offset=None):
##    url = URL + "getUpdates?timeout=100"  #timeout: no of seconds until next update 
##    if offset:
##        url += "&offset={}".format(offset)
##    js = get_json_from_url(url)
##    return js
##
##def get_last_update_id(updates):
##    update_ids = []
##    for update in updates["result"]:
##        update_ids.append(int(update["update_id"]))
##    return max(update_ids)
##
##def get_last_chat_id_and_text(updates):
##    num_updates = len(updates["result"])
##    last_update = num_updates - 1
##    text = updates["result"][last_update]["message"]["text"]
##    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
##    return (text, chat_id)
##
##
##def send_message(text, chat_id):
##     text = urllib.parse.quote_plus(text) #no more problems with ?&+etc
##     url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text, chat_id)
##     get_url(url)
##
##def echo_all(updates):
##    for update in updates["result"]:
##        try:
##            text = update["message"]["text"]
##            chat = update["message"]["chat"]["id"]
##            send_message(text, chat)
##        except Exception as e:
##            print(e)
##    
##def main():
##    try_database()
##    last_update_id = None
##    while True:
##        print ("update")
##        updates = get_updates(last_update_id)
##        if len(updates["result"]) > 0:
##            last_update_id = get_last_update_id(updates) + 1
##            echo_all(updates)
##        time.sleep(0.5)
##
##if __name__ == '__main__':
##    main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-








"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

#for the database
import os
import psycopg2


TOKEN = "435982196:AAGg10t81vJUUygSTVJQ-xYR94bcQEOqv0E"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# for the database (still necessary?)
DATABASE_URL = os.environ['DATABASE_URL']


#does the database work?
def try_database(bot, update):
    try:
        #connect
        conn = psycopg2.connect(DATABASE_URL, sslmode='require') #(DATABASE_URL, sslmode='require') 
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        cursor.execute("""CREATE TABLE prova (id INTEGER, name VARCHAR(255));""")
        # run a SELECT statement - no data in there, but we can try it
        cursor.execute("""SELECT * from prova""")
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        #to save: conn.commit()    to close: cur.close()   and   conn.close()
        print(rows)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

#PSQL language
#


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def repeat(bot, update, args):
    userMessage = " ".join(args)
    update.message.reply_text("you said: " + userMessage)


def makeButtons(bot, update, args):
    keyboard = [[KeyboardButton(args[0], callback_data=args[0]),
                 KeyboardButton(args[1], callback_data='2')],

                [KeyboardButton(args[2], callback_data='3')]]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Scegli un bottone diff:', reply_markup=reply_markup)


def button2(bot, update):
    query = update.callback_query

    update.message.reply_text(text="Selected option: {}".format(query.data),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button)) #hier ist der queryhandler!!!
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('repeat', repeat, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('makeButtons', makeButtons, pass_args=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(button2))
    updater.dispatcher.add_handler(CommandHandler('tryDB', try_database))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
