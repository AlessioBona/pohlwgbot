import json 
import requests
import time
import urllib #solves problems with symbols having special meanings in URL context (?&+)

import os
import psycopg2

import telegram

from telegram import ReplyKeyboardMarkup





TOKEN = "435982196:AAGg10t81vJUUygSTVJQ-xYR94bcQEOqv0E"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#does the database work?
def try_database():
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        cursor.execute("""CREATE TABLE tutorials (name char(40));""")
        # run a SELECT statement - no data in there, but we can try it
        cursor.execute("""SELECT * from tutorials""")
        rows = cursor.fetchall()
        print(rows)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

#dowloads contents of URL and returns string
def get_url(url):   
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

#parses sting into Python dictionary (Telegram always gives JSON response)
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"  #timeout: no of seconds until next update 
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
     text = urllib.parse.quote_plus(text) #no more problems with ?&+etc
     url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text, chat_id, replay_markup)
     get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            replay_markup = ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                ]
                            )
            send_message(text, chat, replay_markup)
        except Exception as e:
            print(e)
    
def main():
    try_database()
    last_update_id = None
    while True:
        print ("update")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()

