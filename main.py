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
import ChatBot
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

proxy = {'http':'http://127.0.0.1:41193', 'https':'http://127.0.0.1:41193'}
apihelper.proxy = proxy

translator = googletrans.Translator()

FBot = telebot.TeleBot(BOT_TOKEN)
    
@FBot.message_handler(func = lambda message : True)
def Answer(message):
    answer = ChatBot.GiveRsponse(message.text)
    if answer == "hentai":
        nude(message)
        return
    if answer == "meme":
        meme(message)
        return
    if answer == "estekhare":
        estekhare(message)
        return
    if answer == "shitpost":
        shitpost(message)
        return
    if answer == "wikipedia":
        wikipediaRandom(message)
        return
    if answer == "translate":
        Translate(message)
        return
    if answer != None:  
        FBot.reply_to(message, answer)


def hentai(message):
    print("Hentai")
    FileTyep = GetRandomPostImage(getSubbredit('hentai'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)
        
def meme(message):
    print("meme")
    FileTyep = GetRandomPostImage(getSubbredit('memes'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)
    
def nude(message):
    print("nude")
    FileTyep = GetRandomPostImage(getSubbredit('RealGirls'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)

def estekhare(message):
    print("estekhare")
    FBot.reply_to(message=message, text=GetEstekhare())

def shitpost(message):
    print("shitpost")
    FileTyep = GetRandomPostImage(getSubbredit('shitposting'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)

def wikipediaRandom(message):
    print("wikipedia")
    wikipedia.set_lang("fa")
    emptyText = ""
    if message.reply_to_message != None:
        emptyText = message.reply_to_message.text
    if emptyText == "":
        FBot.reply_to(message, text=wikipedia.summary(wikipedia.random()))
    else:
        try:
            FBot.reply_to(message, text=wikipedia.summary(wikipedia.search(emptyText)[0]))
        except: 
            FBot.reply_to(message, text="یافت نشد. خیخیخیخیخی.")

def Translate(message):
    print("Translate")
    empty_text = message.reply_to_message.text
    
    if empty_text == "":
        return
    if translator.detect(empty_text).lang == "fa":
        FBot.reply_to(message, translator.translate(empty_text, dest = 'en').text)
    else:
        FBot.reply_to(message, translator.translate(empty_text, dest = 'fa').text)
    

FBot.infinity_polling()
