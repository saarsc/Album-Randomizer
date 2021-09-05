import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.allmusic.com:443/search/typeahead/artist/"

HEADERS = {"Connection": "close", "Accept": "*/*", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36", "X-Requested-With": "XMLHttpRequest", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.allmusic.com/advanced-search", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}

PROXY = {
    "http":"http://127.0.0.1:8080",
    "https":"http://127.0.0.1:8080"
}
with open("artists.txt","r") as f:
    artists = f.readlines()
with open("artists-id.txt","w") as f:
    for artist in artists:
        artist = artist.strip()
        artist_data = requests.get(f"{URL}/{artist}", headers=HEADERS,proxies=PROXY, verify=False)

        soup = BeautifulSoup(artist_data.text,"html.parser")
        el = soup.find(attrs={"data-text":re.compile(f"^{artist}$",re.I)})

        id = el["data-id"]

        f.writelines(f"{artist} - {id}\n")
    

