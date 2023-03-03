import praw
import random
import requests
from redvid import Downloader
import os
from requests import Session
proxy = {'http':'http://127.0.0.1:34229', 'https':'http://127.0.0.1:34229'}
def getSubbredit(subreddit):
    session = Session()
    session.proxies['https'] = 'http://127.0.0.1:34229'
    session.proxies['http'] = 'http://127.0.0.1:34229'
    redditAPI = praw.Reddit(
        client_id = "5F20ZWZ1Y991Ds7jJqR1mA",
        requestor_kwargs = {'session' : session},
        client_secret = "sOqEkRI8qHU1eGvF95L-oobC17VI6Q",
        user_agent = "amiroo4", 
        proxy = proxy
    )

    Hsubreddit = redditAPI.subreddit(subreddit)
    return Hsubreddit

def GetPost(subreddit):
    randomPost = subreddit.random()
    if "v.redd.it" in randomPost.url:
        return GetPost(subreddit)
    return requests.get(randomPost.url).content
    
#GetRandomPostImage(getHentaiSubbredit())