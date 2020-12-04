import pytest
import time
import asyncio
import aiohttp
from functools import wraps
from bs4 import BeautifulSoup


# 异步
# 中国天气预报
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

    async def craw_one(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                bs = BeautifulSoup(response.content, 'lxml')

                print('中国天气预报：')
                provinces = bs.find('div', class_="conMidtab")
                for all_provinces in provinces.find_all('div', class_="conMidtab3"):
                    province_name = all_provinces.find('td', width="74").text
                    print('{}(市)天气预报：'.format(province_name))
                    for all_cities in all_provinces.find_all('tr'):
                        city_name = all_cities.find('td', width="83").text
                        city_day_weather = all_cities.find('td', width="89").text
                        city_night_weather = all_cities.find('td', width="98").text
                        city_highest_temperature = all_cities.find('td', width="92").text
                        city_lowest_temperature = all_cities.find('td', width="86").text
                        print('{}(区/县)：'.format(city_name))
                        print('白天{} 夜晚{}'.format(city_day_weather, city_night_weather))
                        print('最高温度：{}℃ 最低温度：{}℃'.format(city_highest_temperature, city_lowest_temperature))
                        print('===========================================')

    async def craw_all(self, urls):
        tasks = [asyncio.create_task(self.craw_one(url)) for url in urls]
        # tasks = [asyncio.ensure_future(self.craw_one(url)) for url in urls]
        await asyncio.gather(*tasks)

    @timefn
    def test_craw(self):
        province = ['beijing', 'tianjin', 'hebei', 'shanxi', 'neimenggu', 'heilongjiang', 'jilin', 'liaoning',
                    'shanghai', 'anhui', 'jiangsu', 'shandong', 'zhejiang', 'fujian', 'jiangxi', 'hubei', 'hunan',
                    'henan', 'guangxi', 'guangdong', 'hainan', 'shanxi', 'gansu', 'xinjiang', 'qinghai', 'ningxia',
                    'sichuan', 'chongqing', 'guizhou', 'yunnan', 'xizang', 'hongkong', 'macao', 'taiwan']
        urls = ["http://www.weather.com.cn/textFC/{}.shtml#".format(i) for i in province]
        asyncio.run(self.craw_all(urls))
        # loop = asyncio.get_event_loop()
        # try:
        #     loop.run_until_complete(self.craw_all(urls))
        # finally:
        #     loop.close()


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_weather_forecast_asyncio_demo.py'])
