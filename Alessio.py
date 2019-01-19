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

import copy;

my_list = ["latte", "pane", "cioccolato", "vino"]
all_chats = []
all_lists = []


def startAle(bot, update):
    keyboard = []
    chatExists = update.message.chat.id in all_chats
    if(not chatExists):
        all_chats.append(update.message.chat.id)
        all_lists.append([])
    index = all_chats.index(update.message.chat.id)
    all_lists[index] = copy.deepcopy(my_list)
    for x in range(0, len(all_lists[index])):
        c_data = 'beta_' + all_lists[index][x]
        keyboard.append([InlineKeyboardButton(all_lists[index][x], callback_data=c_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def buttAle(bot, update):
    query = update.callback_query
    keyboard = []
    index = 0;
        #all_chats.index(update.message.chat.id)
    all_lists[index].remove(query.data.replace("beta_",""))
    for x in range(0, len(all_lists[index])):
        c_data = 'beta_' + all_lists[index][x]
        keyboard.append([InlineKeyboardButton(all_lists[index][x], callback_data=c_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = update.callback_query
    # text = "Selected optiona: {}".format(query.data.replace("beta_",""))

    bot.edit_message_text(text=text, reply_markup=reply_markup,
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
    keyboard = [[InlineKeyboardButton(args[0], callback_data='beta')], [
                InlineKeyboardButton(args[1], callback_data='beta')],
                [InlineKeyboardButton(args[2], callback_data='beta')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Choose a button:', reply_markup=reply_markup)


def myId_callback(bot, update):
    fck_Id = update.message.from_user.id
    update.message.reply_text("your Id: " + str(fck_Id))



