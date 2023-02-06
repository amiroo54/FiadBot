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
from httpcore import SyncHTTPProxy
import pyttsx3
import asyncio
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

httpcoreProxy = SyncHTTPProxy((b'http', b'127.0.0.1', 41193, b''))
proxy = {'http':'http://127.0.0.1:41193', 'https':'http://127.0.0.1:41193'}
apihelper.proxy = proxy

translatorProxy = {'http': httpcoreProxy, 'https':httpcoreProxy}
translator = googletrans.Translator(proxies=translatorProxy)  

Engine = pyttsx3.init()
Engine.setProperty('voice', 'persian-pinglish')

FBot = telebot.TeleBot(BOT_TOKEN)

last_estekhare = 0
    
@FBot.message_handler(func = lambda message : True)
def Answer(message):
    answer = ChatBot.GiveRsponse(message.text)
    if message.reply_to_message != None:
        if message.reply_to_message.id == last_estekhare:
            SendEstekhare(message)   
            return
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
        print("start")
        Translate(message)
        print('end')
        return
    if answer == "shitranslate":
        ShitranslateStarter(message)
        return
    if answer == "TTS":
        return
    if answer != None and message.reply_to_message == None: 
        FBot.reply_to(message, answer)

def Translate(message):
    print(message.text)
    empty_text = message.reply_to_message.text
    
    if empty_text == "":
        return
    if translator.detect(empty_text).lang == "fa":
        FBot.reply_to(message, translator.translate(empty_text, dest = 'en').text)
    else:
        FBot.reply_to(message, translator.translate(empty_text, dest = 'fa').text)
    

def ShitranslateStarter(message):
    empty_text = message.reply_to_message.text
    if translator.detect(empty_text).lang == "fa":
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'en').text)
    else:
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'fa').text)
    Shitranslate(SentMessage, message)
    

def Shitranslate(message, Premessage):
    empty_text = message.text 
    if translator.detect(empty_text).lang == "fa":
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'en').text)
    else:
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'fa').text)
    if empty_text != Premessage.reply_to_message.text:
        Shitranslate(SentMessage, message)
    else:
        return

def meme(message):
    FileTyep = GetRandomPostImage(getSubbredit('memes'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)
    
def estekhare(message):
    global last_estekhare
    sentphoto = FBot.send_photo(message.chat.id, photo=open('estekhareimage.jpg', 'rb'), reply_to_message_id=message.id)
    last_estekhare = sentphoto.id

def SendEstekhare(message):
    FBot.reply_to(message, GetEstekhare())
    global last_estekhare
    last_estekhare = 0

def shitpost(message):
    FileTyep = GetRandomPostImage(getSubbredit('shitposting'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)

def wikipediaRandom(message):
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



FBot.infinity_polling()
