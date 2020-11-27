from bs4 import BeautifulSoup
import requests
import shutil
import os

# url = "https://www.infoq.com/news/"
url = "https://time.geekbang.org/"

headers = {
    'Connection': 'close',
    # 'Accept''': 'application/json, text/javascript, */*; q=0.01',
    'Accept''': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    # 'Cookie': 'gauges_unique_hour=1; _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1',
    'Host': 'time.geekbang.org',
    'Referer': 'https://time.geekbang.org/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
}


# 下载图片
def download_picture(image_url, image_localpath):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_localpath, 'wb')as f:
            response.raw.deconde_content = True
            shutil.copyfileobj(response.raw, f)


# 爬取标题
def craw(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    for title_href in soup.find_all('div', class_='_3S9KmBtG_0'):
        for title in title_href.find_all('a'):
            if title.get('title'):
                print([title.get('title')])


# 爬取图片
def craw_picture(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    for pic_href in soup.find_all('div', class_='_3hVBef3W_0'):
        for pic in pic_href.find_all('img'):
            img_url = pic.get('src')
            dir = os.path.abspath('../files')
            file_name = os.path.basename(img_url)
            img_path = os.path.join(dir, file_name)
            print('开始下载 %s' % img_url)
            download_picture(img_url, img_path)


# craw(url)
craw_picture(url)
