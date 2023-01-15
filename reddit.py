import praw
import random
import requests
def getHentaiSubbredit(subreddit):
    redditAPI = praw.Reddit(
        client_id = "5F20ZWZ1Y991Ds7jJqR1mA",
        client_secret = "sOqEkRI8qHU1eGvF95L-oobC17VI6Q",
        user_agent = "amiroo4"
    )

    Hsubreddit = redditAPI.subreddit(subreddit)
    return Hsubreddit

def GetRandomPostImage(subreddit):
    randomPost = subreddit.random()
    if ".jpg" in randomPost.url.lower():
        with open("Image.jpg", "wb") as i:
            i.write(requests.get(randomPost.url).content)
        return "jpg"
    elif ".png" in randomPost.url.lower():
        with open("Image.png", "wb") as i:
            i.write(requests.get(randomPost.url).content)
        return "png"
    elif "gif" in randomPost.url.lower():
        return GetRandomPostImage(subreddit)
    
#GetRandomPostImage(getHentaiSubbredit())