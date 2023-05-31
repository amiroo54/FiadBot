import json
import os
FilePath = os.path.dirname(os.path.realpath(__file__))

Users = []
"""with open("GoodNight.json", "w") as file:
    file.write(json.dumps(Users))"""
Users = json.loads(open(FilePath + "GoodNight.json", "r").read())
def SavePerson(person):
    if person in Users:
        return
    Users.append(person)
    with open("GoodNight.json", "w") as file:
        file.write(json.dumps(Users))
        
