import sys, os, io, argparse, re, math, requests, requests_oauthlib, urllib, hashlib
from time import sleep

import bs4
from PIL import Image
from src.Config import Config


class Crawler:
    def __init__(self, config=None):
        self.config = config
    def is_japanese(self, str):
        return True if re.search(r'[ぁ-んァ-ン的个]', str) else False
    def generateUrls(self, pages):
        return []
    def crawl(self, url):
        raise Exception("No implemention.")
    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path) 
    def split_filename(self, f):
        split_name = os.path.splitext(f)
        file_name =split_name[0]
        extension = split_name[-1].replace(".","")
        return file_name,extension
    def download_img(self, path, url):
        self.mkdir(path)
        _,extension  = self.split_filename(url)
        if not extension.lower() in ('jpg','jpeg','gif','png','bmp'):
            return None

        encode_url = urllib.parse.unquote(url).encode('utf-8')
        name = hashlib.sha3_256(encode_url).hexdigest()[0:8]
        full_path = os.path.join(path, name + '.' + extension.lower())

        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            print("HttpError:{0} at{1}".format(r.status_code, url))
            return
        img = Image.open(io.BytesIO(r.content))
        if img.width > img.height:
            size = (256 * img.width // img.height, 256)
        else:
            size = (256, 256 * img.height // img.width)
        resized = img.resize(size)
        resized.save(os.path.join(path, name + '.' + extension.lower()))
        return name
    def remove_non_text(self, text):
        if text.startswith('RT '):
            text = text[3:]
        text = re.sub(r'@[\w\\_:]+', '', text)
        text = re.sub(r'https://[\S]+', '', text)
        text = re.sub(r'#[\S]+', '', text)
        text = re.sub(r'[\n\t|]+', ' ', text)
        return text

class CrawlerXv(Crawler):
    def generateUrls(self, pages):
        return ["https://www.xvideos.com/new/" + str(i) for i in range(1, pages)]

    def crawl(self, url):
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
            if self.is_japanese(title): continue

            file = requests.get(thumb_url, allow_redirects=True)
            open("./data/xv/" + name + ".jpg", 'wb').write(file.content)
            open("./data/xv/" + name + ".txt", 'w').write(title)

class CrawlerTw(Crawler):
    def __init__(self, config=None):
        super().__init__(config)
        self.max_id = ''

    def generateUrls(self, pages):
        return [i for i in range(1, pages)]

    def crawl(self, url):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        query = "photo"
        lang = "en"
        result_type="recent" # 最新のツイートを取得
        count = 100 # 1回あたりの最大取得ツイート数（最大100）
 
        # oauthの設定
        consumer_key = self.config.CONSUMER_KEY
        consumer_secret = self.config.CONSUMER_SECRET
        access_token = self.config.ACCESS_TOKEN
        access_secret = self.config.ACCESS_SECRET
        oauth = requests_oauthlib.OAuth1(consumer_key,consumer_secret,access_token,access_secret)
 
        params = {'q':query,'lang':lang,'result_type':result_type,'count':count,'max_id':self.max_id}
        r = requests.get(url=url,params=params,auth=oauth)
        json_data = r.json()
        for data in json_data['statuses']:
            # 最後のidを格納
            self.max_id = str(data['id']-1)
            if 'media' not in data['entities']:
                continue
            else:
                for media in data['entities']['media']:
                    if media['type'] == 'photo':
                        image_url = media['media_url']
                        try:
                            name = self.download_img("./data/tw/", image_url)
                            if name:
                                text = self.remove_non_text(data['text'])
                                open("./data/tw/" + name + ".txt", 'w').write(text)
                                print("CRAWLED", name)
                        except Exception as e:
                            print("failed to download image at {}".format(image_url), e)
                            continue
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop', default=30, type=int, help='How many times loop')
    parser.add_argument('--xv', action='store_true', help='for XVideos')
    parser.add_argument('--tw', action='store_true', help='for Twitter')
    args = parser.parse_args()

    if args.xv:
        crawler = CrawlerXv()
    if args.tw:
        c = Config("./private/twitter.yml")
        crawler = CrawlerTw(c)
    
    for url in crawler.generateUrls(args.loop):
        crawler.crawl(url)
        sleep(3)
