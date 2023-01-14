import telebot
from telebot import apihelper
from telebot.async_telebot import AsyncTeleBot
import praw
from reddit import *
import asyncio
from estekhare import GetEstekhare
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
    GetRandomPostImage(getHentaiSubbredit('hentai'))
    FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)

@FBot.message_handler(commands=['meme'])
def meme(message):
    print("meme")
    GetRandomPostImage(getHentaiSubbredit('memes'))
    FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    
@FBot.message_handler(commands=['nude'])
def nude(message):
    print("nude")
    GetRandomPostImage(getHentaiSubbredit('RealGirls'))
    FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)

@FBot.message_handler(commands=['estekhare'])
def estekhare(message):
    print("estekhare")
    FBot.reply_to(message=message, text=GetEstekhare())

FBot.infinity_polling()
