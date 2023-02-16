import random
import wikipedia
import json

SpyList = []
class Spy:
    
    def __init__(self, Difficulty, id):
        self.started = False
        self.PlayerList = []
        self.PlayerListId = []
        self.id = id
        SpyList.append(self)
        
        if Difficulty == 1:
            wikipedia.set_lang("fa")
            self.word = wikipedia.random()
        if Difficulty == 2:
            with open("SpyWord.json") as file:  
                self.word = random.choice(json.load(file)["words"])
    
    def AddPlayer(self,player):
        self.PlayerList.append(player)
        self.PlayerListId.append(player.id)
    
    def Start(self):
        self.spy = random.choice(self.PlayerList)            
        self.started = True
        
    def End(self):
        SpyList.remove(self)
        
