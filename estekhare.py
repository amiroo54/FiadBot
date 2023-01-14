import requests
import random
from bs4 import BeautifulSoup 
def GetEstekhare():
    output = ""
    pageNumber = random.randint(1, 602/2)
    url = f"https://www.aviny.com/quran/estekhareh/index2.aspx?page={pageNumber*2 - 1}"
    page = requests.get(url)


    soup = BeautifulSoup(page.content, "html.parser")
    output += soup.find(id="L_Chapter_Name").text + " "
    output += soup.find(id="L_Chapter_Code").text + ". "
    output += soup.find(id="L_GoodBad_Name").text + " کلی :"
    output += soup.find(id="L_Result_General").text + " ازدواج :"
    output += soup.find(id="L_Result_Marriage").text + ". معامله :"
    output += soup.find(id="L_Result_Trade").text + ""
    
    return output
