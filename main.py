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
import discord
#endregion
#region Setup
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

httpcoreProxy = SyncHTTPProxy((b'http', b'127.0.0.1', 34229, b''))
proxy = {'http':'http://127.0.0.1:34229', 'https':'http://127.0.0.1:34229'}
apihelper.proxy = proxy

translatorProxy = {'http': httpcoreProxy, 'https':httpcoreProxy}
translator = googletrans.Translator(proxies=translatorProxy)  


FBot = telebot.TeleBot(BOT_TOKEN)

openai.api_key = os.environ.get("OPENAI_TOKEN")
#endregion

@FBot.message_handler(commands=["start"])
def Start(message):
    SendPrivateMessage("با موفقیت استارت شد.", message.chat.id, 1)

@FBot.message_handler(chat_types=["private"])
def Chatgpt(message):
    ModelEngine = "text-davinci-003"
    promp = message.text
    GPTanswer = openai.Completion.create(
        engine=ModelEngine,
        prompt = promp, 
        max_tokens=1024, 
        n=1, 
        stop = None,
        temperature = 0.5
    )
    SendPrivateMessage(GPTanswer.choices[0].text, message.from_user, 1)
#region Main Message Handler
@FBot.message_handler(func = lambda message : True)
def Answer(message):
    #chatbotchecks
    answer = ChatBot.GiveRsponse(message.text)
    if message.from_user.username == "NowThatRickyIsDead":
        FBot.ban_chat_member(message.chat.id, message.from_user.id)
    match answer:
        case "meme":
            meme(message, 1)
            return
        case "estekhare":
            StartEstekhare(message, 1)
            return
        case "shitpost":
            shitpost(message, 1)
            return
        case "wikipedia":
            wikipediaRandom(message, 1)
            return
        case "spy":
            if not message.from_user == FBot.get_me():
                SpyInit(message, 1)
            return
        case "spystart":
            SpyStart(message, 1)
            return
        case "translate":
            Translate(message, 1)
            return
        case "shitranslate":
            ShitranslateStarter(message, 1)
            return
    #messagereplycheck
    if message.reply_to_message != None:
        #spy
        for Instance in BotTypes.Spy.SpyList:    
            if message.reply_to_message.id == Instance.id.id and Instance.started == False and Instance.PlayerListId.count(message.from_user.id) < 1:
                Instance.AddPlayer(message.from_user)
        #estekhare
        for estekhare in BotTypes.estekhare.estekhareList:
            if message.reply_to_message.id == estekhare.photo.id and message.from_user.id == estekhare.ID.from_user.id:
                print("started")
                SendEstekhare(message, estekhare, 1)
                
        
    if answer != None and message.reply_to_message == None: 
        FBot.reply_to(message, answer)
#endregion

#region Functions
def Translate(message, Type):
    empty_text = message.reply_to_message.text
    if translator.detect(empty_text).lang == "fa":
        text = translator.translate(empty_text, dest = 'en').text
        SendTextMessage(text, message, Type)
    else:
        text = translator.translate(empty_text, dest = 'fa').text
        SendTextMessage(text, message, Type)
    

def ShitranslateStarter(message, Type):
    empty_text = message.reply_to_message.text
    #add discord reply to support
    if translator.detect(empty_text).lang == "fa":
        text = translator.translate(empty_text, dest = 'en').text
        SentMessage = SendTextMessage(text, message, Type)
    else:
        text = translator.translate(empty_text, dest = 'fa').text
        SentMessage = SendTextMessage(text, message, Type)
    Shitranslate(SentMessage, message)
    

def Shitranslate(message, Premessage, Type):
    empty_text = message.text 
    if translator.detect(empty_text).lang == "fa":
        text = translator.translate(empty_text, dest = 'en').text
        SentMessage = SendTextMessage(text, message, Type)
    else:
        text = translator.translate(empty_text, dest = 'fa').text
        SentMessage = SendTextMessage(text, message, Type)
    if empty_text != Premessage.reply_to_message.text:
        Shitranslate(SentMessage, message)
    else:
        return

def meme(message, Type):
    File = GetPost(getSubbredit('memes'))
    SendImageMessage(File, message, Type)

def StartEstekhare(message, Type):
    BotTypes.estekhare(message, SendImageMessage(open("estekhareimage.jpg", "rb"), message, Type))
    

def SendEstekhare(message, es, Type):
    SendTextMessage(GetEstekhare(), message, Type)
    es.end()


def shitpost(message, Type):
    File = GetPost(getSubbredit('shitposting'))
    SendImageMessage(File, message, Type)

def wikipediaRandom(message, Type):
    wikipedia.set_lang("fa")
    emptyText = ""
    if message.reply_to_message != None:
        emptyText = message.reply_to_message.text
    if emptyText == "":
        text=wikipedia.summary(wikipedia.random())
        SendTextMessage(text, message, Type)
    else:
        try:
            text=wikipedia.summary(wikipedia.search(emptyText)[0])
            SendTextMessage(text, message, Type)
        except: 
            SendTextMessage(text, message, "موضوع مورد درخواست شما یافت نشد.")
            
def SpyInit(message, Type):
    Sentmessage = SendTextMessage("برای اضافه شدن به بازی روی این پیام ریپلای بزنید.\n \n \n \n \n (برای زیاد شدن طول پیام و جلب توجه.)", message, Type)
    BotTypes.Spy(2, Sentmessage)
    
def SpyStart(message, Type):
    for instance in BotTypes.Spy.SpyList:
        if message.reply_to_message.id == instance.id.id and message.from_user.id == instance.id.reply_to_message.from_user.id:
            instance.Start()
            Spy = instance
            for player in Spy.PlayerList:
                try:
                    if Spy.spy == player:
                        SendPrivateMessage("شما جاسوس هستید.", player, Type)
                    else:
                        SendPrivateMessage(Spy.word, player, Type)
                except apihelper.ApiTelegramException as e:
                    if e.description == "Forbidden: bot can't initiate conversation with a user":
                        SendTextMessage(f"the player {player.username} has not started the bot, the game will start regardless.", message, Type)
#endregion



def SendTextMessage(Text, ReplyToMessage, Type):
    match Type:
        case 1:
            return FBot.reply_to(ReplyToMessage, Text)
        case 2:
            #discordBotSendMessage
            x =1
            
def SendImageMessage(Image, ReplyToMessage, Type):
    match Type:
        case 1:
            return FBot.send_photo(ReplyToMessage.chat.id, Image, reply_to_message_id=ReplyToMessage.id)
            
def SendPrivateMessage(Text, User, Type):
    match Type:
        case 1:
            return FBot.send_message(User.id, Text)
        
FBot.infinity_polling()