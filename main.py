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
import praw.exceptions
import time
import json
#import discord
#endregion
#region Setup
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
#DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
translator = googletrans.Translator()  

FilePath = os.path.dirname(os.path.realpath(__file__)) + "/"
#DBot = discord.Client(intents=discord.Intents.default())
FBot = telebot.TeleBot(BOT_TOKEN)

HasGoodNighted = False
#endregion

@FBot.message_handler(commands=["start"])
def Start(message):
    SendPrivateMessage("با موفقیت استارت شد.", message.chat, 1)

@FBot.message_handler(commands=["reddit"])
def Reddit(message):
    text = message.text.replace("/reddit", "").replace("@FiardBot", "").replace(" ", '')
    try:
        File = GetPost(getSubbredit(text))
        SendImageMessage(File, message, 1)
    except praw.exceptions.InvalidURL as e:
        SendTextMessage("وجود ندارد.", message, 1)
        


#region Main Telegram Message Handler
@FBot.message_handler(func = lambda message : True)
def Answer(message):
    global HasGoodNighted
    #chatbotchecks
    if (time.localtime().tm_hour > 21 or time.localtime().tm_hour < 4) and not HasGoodNighted:
        #SendGoodNight(1)
        HasGoodNighted = True
    answer = ChatBot.GiveResponse(message.text)
    if answer != None: print(message.chat.title)
    if message.from_user.username == "Aaaaa20202":
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
            ShitranslateOnce(message)
            return
        case "google":
            GooglAuto(message)
            return
    if message.chat.type == "private":
        if answer == "goodnight":
                import GoodNighter
                GoodNighter.SavePerson(message.from_user.id)
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
    
    if answer == "goodnight":
        SendTextMessage(random.choice(("شو بخیر.", "شب خوش.", "شو خوش.", "شب بخیر.")), message, 1)      
        return      
    
    if answer != None and message.reply_to_message == None: 
        FBot.reply_to(message, answer)
#endregion

"""@DBot.event
async def on_message(message):
    answer = ChatBot.GiveRsponse(message.content)
    match answer:
        case "meme":
            meme(message, 2)
            return
        case "estekhare":
            StartEstekhare(message, 2)
            return
        case "shitpost":
            shitpost(message, 2)
            return
        case "wikipedia":
            wikipediaRandom(message, 2)
            return
        case "spy":
            if not message.author == DBot.user:
                SpyInit(message, 2)
            return
        case "spystart":
            SpyStart(message, 2)
            return
        case "translate":
            Translate(message, 2)
            return
        case "shitranslate":
            ShitranslateStarter(message, 2)
            return"""

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
    Shitranslate(SentMessage, message, Type)
    

def Shitranslate(message, Premessage, Type):
    empty_text = message.text 
    if translator.detect(empty_text).lang == "fa":
        text = translator.translate(empty_text, dest = 'en').text
        SentMessage = SendTextMessage(text, message, Type)
    else:
        text = translator.translate(empty_text, dest = 'fa').text
        SentMessage = SendTextMessage(text, message, Type)
    if empty_text != Premessage.reply_to_message.text:
        Shitranslate(SentMessage, message, Type)
    else:
        return
    
def ShitranslateOnce(message):
    result = message.reply_to_message.text
    for i in range(1, 5):
        result = translator.translate(result, random.choice(list(googletrans.LANGUAGES))).text
    result = translator.translate(result, "fa").text
    SendTextMessage(result, message, 1)

def meme(message, Type):
    File = GetPost(getSubbredit('memes'))
    SendImageMessage(File, message, Type)

def StartEstekhare(message, Type):
    BotTypes.estekhare(message, SendImageMessage(open(FilePath + "estekhareimage.jpg", "rb"), message, Type))
    

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
        text=wikipedia.summary(wikipedia.search(emptyText)[0])
        try:
            SendTextMessage(text, message, Type)
        except: 
            SendTextMessage("موضوع مورد درخواست شما یافت نشد.", message, Type)
            
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

def GooglAuto(message):
    text = message.reply_to_message.text
    headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    result = ""
    response = requests.get(f'http://google.com/complete/search?client=chrome&q={text}', headers=headers)
    for item in json.loads(response.text)[1]:
        result += item + "\n"
    SendTextMessage(result, message, 1)
#endregion


def SendTextMessage(Text, ReplyToMessage, Type):
    match Type:
        case 1:
            if (Text[-1] == "." or Text[-1] == "?"):
                return FBot.reply_to(ReplyToMessage, Text)
            else:
                return FBot.reply_to(ReplyToMessage, Text + ".")
        case 2:
            return ReplyToMessage.channel.send(Text)
            
def SendImageMessage(Image, ReplyToMessage, Type):
    match Type:
        case 1:
            return FBot.send_photo(ReplyToMessage.chat.id, Image, reply_to_message_id=ReplyToMessage.id)
        case 2:
            #return ReplyToMessage.channel.send(file=discord.File(Image))
            x=2
            
def SendPrivateMessage(Text, User, Type):
    match Type:
        case 1:
            return FBot.send_message(User, Text)
        case 2:
            User.create_dm()
            User.dm_channel.send(Text)

"""def SendGoodNight(Type):
    import GoodNighter
    for user in GoodNighter.Users:
        SendPrivateMessage(random.choice(("شو بخیر.", "شب خوش.", "شو خوش.", "شب بخیر.", "شبت بخیر.")), user, Type)
"""


#DBot.run(DISCORD_TOKEN)
FBot.infinity_polling()
