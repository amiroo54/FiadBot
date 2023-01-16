import praw
import random
import requests
from redvid import Downloader
import os
def getSubbredit(subreddit):
    redditAPI = praw.Reddit(
        client_id = "5F20ZWZ1Y991Ds7jJqR1mA",
        client_secret = "sOqEkRI8qHU1eGvF95L-oobC17VI6Q",
        user_agent = "amiroo4"
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
        VDownloader.download()
        os.rename(VDownloader.file_name, "Video.mp4")
        return "mp4"
    elif "gif" in randomPost.url.lower():
        return GetRandomPostImage(subreddit)
    
#GetRandomPostImage(getHentaiSubbredit())