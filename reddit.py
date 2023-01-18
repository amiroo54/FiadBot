import praw
import random
import requests
from redvid import Downloader
import os
from requests import Session
def getSubbredit(subreddit):
    proxy = {'http':'http://127.0.0.1:41193', 'https':'http://127.0.0.1:41193'}
    session = Session()
    session.proxies['https'] = 'http://127.0.0.1:41193'
    session.proxies['http'] = 'http://127.0.0.1:41193'
    redditAPI = praw.Reddit(
        client_id = "5F20ZWZ1Y991Ds7jJqR1mA",
        requestor_kwargs = {'session' : session},
        client_secret = "sOqEkRI8qHU1eGvF95L-oobC17VI6Q",
        user_agent = "amiroo4", 
        proxy = proxy
    )

    Hsubreddit = redditAPI.subreddit(subreddit)
    return Hsubreddit

def GetRandomPostImage(subreddit):
    randomPost = subreddit.random()
    print(randomPost.url)
    if ".jpg" in randomPost.url.lower():
        with open("Image.jpg", "wb") as i:
            i.write(requests.get(randomPost.url).content)
        return "jpg"
    elif ".png" in randomPost.url.lower():
        with open("Image.png", "wb") as i:
            i.write(requests.get(randomPost.url).content)
        return "png"
    elif "v.redd.it" in randomPost.url.lower():
        VDownloader = Downloader(max_q=True) 
        VDownloader.max_s = 5 * (1 << 20)
        VDownloader.url = randomPost.url
        try:
            VDownloader.download()
        except:
            GetRandomPostImage(subreddit)
            return
        os.rename(VDownloader.file_name, "Video.mp4")
        return "mp4"
    elif "gif" in randomPost.url.lower():
        return GetRandomPostImage(subreddit)
    
#GetRandomPostImage(getHentaiSubbredit())