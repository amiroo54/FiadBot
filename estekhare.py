import requests
import random
from bs4 import BeautifulSoup 

def GetEstekhare():
    Rurl = random.randint(1, 604/2)
    url = f"https://www.aviny.com/%D8%A7%D8%B3%D8%AA%D8%AE%D8%A7%D8%B1%D9%87/{Rurl*2-1}"
    response = requests.get(url)    
    soup = BeautifulSoup(response.text, 'lxml')
        
    output = soup.find('div', {'class': 'field field--name-field-soore field--type-entity-reference field--label-inline clearfix'}).text 
    output += soup.find('div', {'class':'field field--name-field-natije-ayeh field--type-integer field--label-above'}).text 
    output += soup.find('div', {'class':'field field--name-field-natije field--type-string-long field--label-inline clearfix'}).text 
    output += soup.find('div', {'class':'field field--name-field-natije-kolli field--type-string-long field--label-inline clearfix'}).text 
    output += soup.find('div', {'class':'field field--name-field-natije-ezdevaj field--type-string-long field--label-inline clearfix'}).text 
    output += soup.find('div', {'class':'field field--name-field-natije-moamele field--type-string-long field--label-inline clearfix'}).text 
    return output
    