import random
import wikipedia


class Spy:
    started = False
    PlayerList = []
    def __init__(self, Difficulty, id):
        self.id = id
        print(self.id.id)
        if Difficulty == 1:
            wikipedia.set_lang("fa")
            self.word = wikipedia.random()
        if Difficulty == 2:
            self.word = ""
            
    def Start(self):
        self.spy = random.choice(self.PlayerList)
        self.started = True
        
