import random
import wikipedia
import json
import os
FilePath = os.path.dirname(os.path.realpath(__file__)) + "/"

class Spy:
    SpyList = []
    def __init__(self, Difficulty, id):
        self.started = False
        self.PlayerList = []
        self.PlayerListId = []
        self.id = id
        Spy.SpyList.append(self)
        
        if Difficulty == 1:
            wikipedia.set_lang("fa")
            self.word = wikipedia.random()
        if Difficulty == 2:
            with open(FilePath + "SpyWord.json") as file:  
                wordList = json.load(file)
                self.word = random.choice(wordList["words"])
    
    def AddPlayer(self,player):
        self.PlayerList.append(player)
        self.PlayerListId.append(player.id)
    
    def Start(self):
        self.spy = random.choice(self.PlayerList)            
        self.started = True
        
    def End(self):
        Spy.SpyList.remove(self)

class estekhare:
    estekhareList = []
    def __init__(self, initmessage, sentPhoto):
        self.ID = initmessage
        self.photo = sentPhoto
        estekhare.estekhareList.append(self)
        
    def end(self):
        estekhare.estekhareList.remove(self)