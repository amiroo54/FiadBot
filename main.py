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

    
@FBot.message_handler(func = lambda message : True)
def Answer(message):
    answer = ChatBot.GiveRsponse(message.text)
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
    if answer == "TTS":
        #TTSBot(message)
        return
    if answer == "shitranslate":
        ShitranslateStarter(message)
        return
    if answer != None:  
        FBot.reply_to(message, answer)

def meme(message):
    print("meme")
    FileTyep = GetRandomPostImage(getSubbredit('memes'))
    if FileTyep == "png":
        FBot.send_photo(message.chat.id, photo=open("Image.png", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "jpg":
        FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)
    elif FileTyep == "mp4":
        FBot.send_video(message.chat.id, video=open("Video.mp4", "rb"), reply_to_message_id=message.id)
    
def estekhare(message):
    print("estekhare")
    GetEstekhare()
    FBot.send_photo(message.chat.id, photo=open("Image.jpg", "rb"), reply_to_message_id=message.id)

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
    
def TTSBot(message):
    print("TTS")
    Engine.save_to_file(message.text, "Voice.mp3")
    Engine.runAndWait()
    FBot.send_audio(message.chat.id, telebot.types.InputFile("Voice.mp3"), reply_to_message_id=message.id)
    print("done")

def ShitranslateStarter(message):
    print('shitranslateStart')
    empty_text = message.reply_to_message.text
    if translator.detect(empty_text).lang == "fa":
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'en').text)
    else:
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'fa').text)
    Shitranslate(SentMessage, message)
    

def Shitranslate(message, Premessage):
    print("shitranslate")
    empty_text = message.text 
    if translator.detect(empty_text).lang == "fa":
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'en').text)
    else:
        SentMessage = FBot.reply_to(message, translator.translate(empty_text, dest = 'fa').text)
    if empty_text != Premessage.reply_to_message.text:
        Shitranslate(SentMessage, message)
    else:
        return

FBot.infinity_polling()
