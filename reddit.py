import praw
import random
import requests
def getHentaiSubbredit():
    redditAPI = praw.Reddit(
        client_id = "5F20ZWZ1Y991Ds7jJqR1mA",
        client_secret = "sOqEkRI8qHU1eGvF95L-oobC17VI6Q",
        user_agent = "amiroo4"
    )

    Hsubreddit = redditAPI.subreddit('hentai')
    return Hsubreddit

def GetRandomPostImage(subreddit):
    with open("Image.jpg", "wb") as i:
        i.write(requests.get(subreddit.random().url).content)
    
#GetRandomPostImage(getHentaiSubbredit())