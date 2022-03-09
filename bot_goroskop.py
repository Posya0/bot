from bs4 import BeautifulSoup
import requests

request = requests.get("https://www.astrostar.ru/horoscopes/main/bliznetsi/day.html")

bs = BeautifulSoup(request.text, "html.parser")

blok = bs.find("p")

print(blok.text)