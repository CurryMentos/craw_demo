import asyncio
import aiohttp

import time
from functools import wraps
from bs4 import BeautifulSoup


def timefn(fn):
    """计算性能的修饰器"""

    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {t2 - t1: .5f} s")
        return result

    return measure_time

url = "https://www.bilibili.com/movie/"
headers = {
    'Connection': 'close',
    # 'Accept''': 'application/json, text/javascript, */*; q=0.01',
    'Accept''': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    # 'Cookie': 'gauges_unique_hour=1; _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1',
    'Host': 'm.douban.com',
    'Origin': 'https://movie.douban.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
}


async def fetch_content(url):
    async with aiohttp.ClientSession(
            headers=headers, connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        async with session.get(url) as response:
            return await response.text()


@timefn
async def main():
    init_page = await fetch_content(url)
    bs = BeautifulSoup(init_page, 'lxml')

    all_movies = bs.find('div', id="app")
    print('哔哩哔哩放映厅热播推荐：')
    for each_movie in all_movies.find_all('li', class_="video-item-biref cinema-large"):
        all_a_tag = each_movie.find_all('a')

        movie_name = all_a_tag[0].find('div', class_="biref-title").text
        url_to_fetch = all_a_tag[0]['href']

        tasks = [fetch_content(url) for url in url_to_fetch]
        pages = await asyncio.gather(*tasks)

        print('{} {}'.format(movie_name, url_to_fetch))


asyncio.run(main())
