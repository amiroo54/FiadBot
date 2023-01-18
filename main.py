import telebot
from telebot import apihelper
from telebot.async_telebot import AsyncTeleBot
import praw
from reddit import *
import asyncio
from estekhare import GetEstekhare
import wikipedia
import os
from dotenv import load_dotenv
import googletrans
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

proxy = {'http':'http://127.0.0.1:41193', 'https':'http://127.0.0.1:41193'}
apihelper.proxy = proxy

translator = googletrans.Translator()

FBot = telebot.TeleBot(BOT_TOKEN)
    
        

@FBot.message_handler(commands=['help'])
def help(message):
    print("Help")
    FBot.reply_to(message=message,text="کمک می خوای؟ بیا بخورش.")
    

@FBot.message_handler(commands=['hentai'])
def hentai(message):
    print("Hentai")
    FileTyep = GetRandomPostImage(getSubbredit('hentai'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)
        
@FBot.message_handler(commands=['meme'])
def meme(message):
    print("meme")
    FileTyep = GetRandomPostImage(getSubbredit('memes'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)
    
@FBot.message_handler(commands=['nude'])
def nude(message):
    print("nude")
    FileTyep = GetRandomPostImage(getSubbredit('RealGirls'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)

@FBot.message_handler(commands=['estekhare'])
def estekhare(message):
    print("estekhare")
    FBot.reply_to(message=message, text=GetEstekhare())

@FBot.message_handler(commands=['shitpost'])
def shitpost(message):
    print("shitpost")
    FileTyep = GetRandomPostImage(getSubbredit('shitposting'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)

@FBot.message_handler(commands=["wikipedia"])
def wikipediaRandom(message):
    print("wikipedia")
    wikipedia.set_lang("fa")
    emptyText = message.text.replace("/wikipedia", "").replace("@Fiard_bot", "")
    if emptyText == "":
        FBot.reply_to(message, text=wikipedia.summary(wikipedia.random()))
    else:
        try:
            FBot.reply_to(message, text=wikipedia.summary(wikipedia.search(emptyText)[0]))
        except:
            FBot.reply_to(message, text="یافت نشد. خیخیخیخیخی.")

@FBot.message_handler(commands=["translate"])
def Translate(message):
    print("Translate")
    if message.reply_to_message == None:
        empty_text = message.text.replace("/translate", "").replace("@Fiard_bot", "")
    else:
        empty_text = message.reply_to_message.text
        
    if translator.detect(empty_text).lang == "fa":
        FBot.reply_to(message, translator.translate(empty_text, dest = 'en').text)
    else:
        FBot.reply_to(message, translator.translate(empty_text, dest = 'fa').text)
    

FBot.infinity_polling()
