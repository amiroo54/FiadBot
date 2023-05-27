import praw
import random
import requests
from redvid import Downloader
import os
from requests import Session
def getSubbredit(subreddit):
    session = Session()
    redditAPI = praw.Reddit(
        client_id = "5F20ZWZ1Y991Ds7jJqR1mA",
        client_secret = "sOqEkRI8qHU1eGvF95L-oobC17VI6Q",
        user_agent = "amiroo4", 
    )

    Hsubreddit = redditAPI.subreddit(subreddit)
    return Hsubreddit

def GetPost(subreddit):
    randomPost = subreddit.random()
    if "v.redd.it" in randomPost.url:
        return GetPost(subreddit)
    return requests.get(randomPost.url).content
    
#GetRandomPostImage(getHentaiSubbredit())