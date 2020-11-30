import pytest
import time
import requests
from functools import wraps
from bs4 import BeautifulSoup


class TestCraw(object):
    def timefn(fn):
        """计算函数运行时间的装饰器"""

        @wraps(fn)
        def measure_time(*args, **kwargs):
            t1 = time.time()
            result = fn(*args, **kwargs)
            t2 = time.time()
            print(f"@timefn: {fn.__name__} took {t2 - t1: .5f} s")
            return result

        return measure_time

    # 哔哩哔哩放映厅
    @timefn
    def test_craw(object):
        url = "https://www.bilibili.com/movie/"
        headers = {
            'Connection': 'close',
            # 'Accept''': 'application/json, text/javascript, */*; q=0.01',
            'Accept''': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
            # 'Cookie': 'DFF0015216D06A1B48DC7BE3AD3BA45E8|5af2dd013253498be4567c7ab005658a',
            'Origin': 'https://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            # 'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers)
        bs = BeautifulSoup(response.content, 'lxml')

        all_movies = bs.find('div', id="app")
        print('哔哩哔哩放映厅热播推荐：')
        for each_movie in all_movies.find_all('li', class_="video-item-biref cinema-large"):
            all_a_tag = each_movie.find_all('a')

            movie_name = all_a_tag[0].find('div', class_="biref-title").text
            url_to_fetch = all_a_tag[0]['href']

            print('{} {}'.format(movie_name, url_to_fetch))

    if __name__ == '__main__':
        pytest.main(['-s', '-v', 'test_movie_demo.py'])
