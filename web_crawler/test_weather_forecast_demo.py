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

    # 中国天气预报
    def weather_forecast(object, province):
        # url = "http://www.weather.com.cn/textFC/beijing.shtml#"
        url = "http://www.weather.com.cn/textFC/{}.shtml#".format(province)
        headers = {
            'Connection': 'close',
            'Accept''': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept''': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
            # 'Cookie': 'DFF0015216D06A1B48DC7BE3AD3BA45E8|5af2dd013253498be4567c7ab005658a',
            # 'Origin': 'https://www.bilibili.com/',
            # 'Host': 'www.weather.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            # 'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers)
        bs = BeautifulSoup(response.content, 'lxml')

        print('中国天气预报：')
        province = bs.find('div', class_="conMidtab3")
        province_name = province.find('td', width="74").text
        print('{}(市)天气预报：'.format(province_name))
        # for all_cities in province.find_all('tr'):
        #     city_name = all_cities.find('td', width="83").text
        #     city_day_weather = all_cities.find('td', width="89").text
        #     city_night_weather = all_cities.find('td', width="98").text
        #     city_highest_temperature = all_cities.find('td', width="92").text
        #     city_lowest_temperature = all_cities.find('td', width="86").text
        #     print('{}(区/县)：'.format(city_name))
        #     print('白天{} 夜晚{}'.format(city_day_weather, city_night_weather))
        #     print('最高温度：{}℃ 最低温度：{}℃'.format(city_highest_temperature, city_lowest_temperature))
        #     print('===========================================')

    @timefn
    def test_craw(self):
        # province = ['beijing', 'tianjin', 'hebei', 'shanxi', 'neimenggu', 'heilongjiang', 'jilin', 'liaoning',
        #             'shanghai', 'anhui', 'jiangsu', 'shandong', 'zhejiang', 'fujian', 'jiangxi']
        province = ['heilongjiang']
        for i in province:
            self.weather_forecast(i)


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_weather_forecast_demo.py'])
