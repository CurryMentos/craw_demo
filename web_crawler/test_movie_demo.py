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
            print(f"方法{fn.__name__}耗时{t2 - t1:.2f}秒")
            return result

        return measure_time

    # 哔哩哔哩放映厅
    @timefn
    def test_craw(object):
        url = "https://www.bilibili.com/movie/"
        response = requests.get(url)
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
