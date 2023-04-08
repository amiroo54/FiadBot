import json

Users = []
"""with open("GoodNight.json", "w") as file:
    file.write(json.dumps(Users))"""
Users = json.loads(open("GoodNight.json", "r").read())
def SavePerson(person):
    if person in Users:
        return
    Users.append(person)
    with open("GoodNight.json", "w") as file:
        file.write(json.dumps(Users))
        
