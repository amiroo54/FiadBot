#region imports
import telebot
from telebot import apihelper
import praw
from reddit import *
from estekhare import GetEstekhare
import wikipedia
import os
from dotenv import load_dotenv
import googletrans
import ChatBot
from httpcore import SyncHTTPProxy
import BotTypes
from telebot import types
import openai
#endregion
#region Setup
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

httpcoreProxy = SyncHTTPProxy((b'http', b'127.0.0.1', 45657, b''))
proxy = {'http':'http://127.0.0.1:45657', 'https':'http://127.0.0.1:45657'}
apihelper.proxy = proxy

translatorProxy = {'http': httpcoreProxy, 'https':httpcoreProxy}
translator = googletrans.Translator(proxies=translatorProxy)  


FBot = telebot.TeleBot(BOT_TOKEN)

openai.api_key = os.environ.get("OPENAI_TOKEN")
#endregion

@FBot.message_handler(commands=["start"])
def Start(message):
    FBot.send_message(message.chat.id, "با موفقیت استارت شد.")

@FBot.message_handler(chat_types=["privte"])
def Chatgpt(message):
    ModelEngine = "text-davinci-003"
    promp = message.text
    GPTanswer = openai.Completion.create(
        engine=ModelEngine,
        prompt = promp, 
        max_token=1024, 
        n=1, 
        stop = None,
        temperatre = 0.5
    )
    FBot.reply_to(message, GPTanswer.choices[0].text)
#region Main Message Handler
@FBot.message_handler(func = lambda message : True)
def Answer(message):
    #chatbotchecks
    answer = ChatBot.GiveRsponse(message.text)
    if message.from_user.username == "NowThatRickyIsDead":
        FBot.ban_chat_member(message.chat.id, message.from_user.id)
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
    if answer == "spy":
        if not message.from_user == FBot.get_me():
            SpyInit(message)
        return
    if answer == "spystart":
        SpyStart(message)
        return
    if answer == "translate":
        Translate(message)
        return
    if answer == "shitranslate":
        ShitranslateStarter(message)
        return
    #messagereplycheck
    if message.reply_to_message != None:
        #spy
        for Instance in BotTypes.Spy.SpyList:    
            if message.reply_to_message.id == Instance.id.id and Instance.started == False and Instance.PlayerListId.count(message.from_user.id) < 1:
                Instance.AddPlayer(message.from_user)
        #estekhare
        if message.reply_to_message.id == last_estekhare:
            SendEstekhare(message)   
            return
        return
    if answer != None and message.reply_to_message == None: 
        FBot.reply_to(message, answer)
#endregion

#region Functions
def Translate(message):
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

last_estekhare = 0
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
            
def SpyInit(message):
    markup = types.InlineKeyboardMarkup()
    startButton = types.InlineKeyboardButton("شروع", callback_data="Start")
    endButton = types.InlineKeyboardButton("پایان", callback_data="End")
    InfoButton = types.InlineKeyboardButton("قوانین", callback_data="Info")
    markup.add(startButton, endButton).add(InfoButton)
    Sentmessage = FBot.reply_to(message, "برای اضافه شدن به بازی روی این پیام ریپلای بزنید.", reply_markup = markup)
    BotTypes.Spy(2, Sentmessage)
    
def SpyStart(message):
    for instance in BotTypes.Spy.SpyList:
        if message.reply_to_message.id == instance.id.id and message.from_user.id == instance.id.reply_to_message.from_user.id:
            instance.Start()
            Spy = instance
            for player in Spy.PlayerList:
                try:
                    if Spy.spy == player:
                        FBot.send_message(player.id, "شما جاسوس هستید.")
                    else:
                        FBot.send_message(player.id, Spy.word)
                except apihelper.ApiTelegramException as e:
                    if e.description == "Forbidden: bot can't initiate conversation with a user":
                        FBot.reply_to(message, f"the player {player.username} has not started the bot, the game will start regardless.")
#endregion


FBot.infinity_polling()