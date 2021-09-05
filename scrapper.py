
from requests import post
import re
from pprint import pprint
from bs4 import BeautifulSoup
from os import remove

OUTPUT_FILE_NAME = "data.txt"
DATA_FILE_NAME = "artists-id.txt"

def get_data(filter,):
    URL = f"https://www.allmusic.com:443/advanced-search/results/"
    burp0_cookies = {"allmusic_session": "tf34YQWPy7eBQDW9e%2F6hK2wjiCK0ra%2FAcPK8grbukJ018xSwPc%2BM3D1bJI51CIKpGfL1BPsyIC3JjF4v6uGYMa%2BqrtKdEU5KxI7x7ifEumGhjDF9N1lWLSF6lBWvQoNQuPI59vOkMO4QPSgd%2BAP8d9XEowplCMyWqvhJf8PpUZorPRMwQksDm39gIyIWg3C4Z%2Fi11Zzu%2BI5otmH9fqZwQcOXHoKLChDwzYC1lni0a6rC2AMX47p7hw81vQ%2BhKX568AO6RRIl8q4OwKCsCcTJV3rbKExry0ydinFBdy9j%2BAQbg0QUkUCJPr%2Fd2iQDruNDqYGalduHupFOHPUmnqWGVpy5ZVmChMdtQBMaWmW%2FIE17L8Gip02%2ByG8Shpaz4pCno1087gs6JYgpZQPkHPt%2B%2FHV0EZZ5yTA8d2Uy89dFW1ctR4%2BpkQ7BebpNFX7lA%2FLsai3QJLFTESuNVeSburOHow%3D%3D",
                     "_ga": "GA1.2.1481225704.1616054455", "_gid": "GA1.2.600374094.1616054455", "registration_prompt": "1", "_gat_smbTracker": "1", "_gat_smbTracker2": "1", "__qca": "P0-141625465-1616054461164", "policy": "notified", "__gads": "ID=64baecc255b2aec7-221ada6120a700fc:T=1616054506:RT=1616054506:S=ALNI_MasLiI8qJO1ryKjFFBDFPVEPz4a2Q", "_gat": "1"}
    HEADERS = {"Connection": "close", "Accept": "text/html, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Origin": "https://www.allmusic.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.allmusic.com/advanced-search", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    PAYLOAD = [("filters[]", "editorialrating:9|editorialrating:8|editorialrating:7|editorialrating:6|editorialrating:5"),
               ("filters[]", "recordingtype:mainalbum"),
               ("filters[]", filter),
               ("sort", '')]


    r = post(URL, data=PAYLOAD,headers=HEADERS )

    soup = BeautifulSoup(r.text, "html.parser")

    soup = soup.tbody
    titles = [x.get_text() for x in soup.select(".title a:first-child")]

    artists = [x.get_text() for x in soup.select(".artist a:first-child")]

    with open(OUTPUT_FILE_NAME, "w+") as f:
        res = [f"{i} - {j}\n" for i, j in zip(artists, titles)]
        f.writelines(res)


def generateArtistFilter():
    with open(DATA_FILE_NAME) as f:
        data = f.readlines()
    filter = ""
    for artist in data:
        id = re.search(r"(?<=- ).*", artist).group(0)
        filter += f"performerid:{id}|"
    return filter[:-1]


remove(OUTPUT_FILE_NAME)
filter = generateArtistFilter()

get_data(filter)
