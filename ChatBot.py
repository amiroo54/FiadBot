import json
import random
import hazm
with open("intents.json", "r", encoding='utf-8') as file:
    data = json.load(file)
norm = hazm.Normalizer()
stem = hazm.Stemmer()
def ChatBot():
    words = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            pattern = norm.normalize(pattern)
            words.append((pattern, intent))
    return words 
       
def GiveResponse(s):
    words = ChatBot()
    for word in words:
        s = norm.normalize(s)
        if word[0] in s:
            print("_______________")
            print(word[0])
            return random.choice(word[1]['responses'])
    

