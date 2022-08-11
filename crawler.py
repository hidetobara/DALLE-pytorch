import sys, os, argparse, re
from time import sleep

import bs4
import requests


def is_japanese(str):
    return True if re.search(r'[ぁ-んァ-ン的个]', str) else False 

def crawl(url):
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        print('Error')
        exit(1)
    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    for b in soup.find_all("div", class_="thumb-block"):
        thumb_url = b.find("img")["data-src"]
        title = b.find("p", class_="title").find("a")["title"]
        cells = thumb_url.split('/')
        name = cells[-2][0:8]
        print(name, title, thumb_url)
        if is_japanese(title): continue

        file = requests.get(thumb_url, allow_redirects=True)
        open("data/" + name + ".jpg", 'wb').write(file.content)
        open("data/" + name + ".txt", 'w').write(title)

if __name__ == "__main__":
    BASE_URL = "https://www.xvideos.com/new/"
    for i in range(1, 30):
        print("page=", i)
        crawl(BASE_URL + str(i))
        sleep(1)
