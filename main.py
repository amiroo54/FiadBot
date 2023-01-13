import telebot
from telebot import apihelper
from telebot.async_telebot import AsyncTeleBot
import praw
from reddit import *
import asyncio

BOT_TOKEN = "5475225482:AAFr-kBo2nO9YV_Lnc7-BxdvpLXF2YM9QQ8"

apihelper.proxy = {'http':'http://127.0.0.1:41193', 'https':'http://127.0.0.1:41193'}

FBot = telebot.TeleBot(BOT_TOKEN)
@FBot.message_handler(commands=['help'])
def help(message):
    print("Help")
    FBot.reply_to(message=message,text="کمک می خوای؟ بیا بخورش.")

@FBot.message_handler(commands=['hentai'])
def hentai(message):
    print("Hentai")
    GetRandomPostImage(getHentaiSubbredit())
    FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message)


FBot.infinity_polling()
