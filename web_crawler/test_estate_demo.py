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

    @timefn
    def test_craw(self):
        # district_all = {"pudong"}
        district_all = {"jingan", "xuhui", "huangpu", "changning", "putuo", "pudong", "baoshan", "hongkou",
                        "yangpu", "minhang", "jiading", "songjiang", "qingpu", "fengxian", "jinshan", "chongming"}
        property_type = "nht1"  # 住宅 nht1, 别墅 nht2, 商业 nht3, 写字楼 nht4
        sale_type = "nhs1"  # 在售 nhs1, 未开盘 nhs2, 售罄 nhs3
        decoration_type = "nhd2"  # 带装修 nhd1, 毛坯 nhd2

        print('链家在售楼盘：')
        for district in district_all:
            url = "https://sh.fang.lianjia.com/loupan/{}/{}{}{}/".format(
                district, property_type, sale_type, decoration_type)
            response = requests.get(url)
            bs = BeautifulSoup(response.content, 'lxml')

            print(district + '：')
            all_estates = bs.find('div', class_="resblock-list-container clearfix")
            result = all_estates.find('div', class_="resblock-have-find")
            result_0 = result.find_all('span')[0].text
            result_1 = result.find_all('span')[1].text
            result_2 = result.find_all('span')[2].text
            print(result_0 + result_1 + result_2)

            if int(result_1) == 0:
                print('===========================================')
                continue
            else:
                for each_estate in all_estates.find_all('div', class_="resblock-desc-wrapper"):
                    estate_name = each_estate.find('div', class_="resblock-name").find('a').text
                    estate_location = each_estate.find('div', class_="resblock-location")
                    estate_location_span_0 = estate_location.find_all('span')[0].text
                    estate_location_span_1 = estate_location.find_all('span')[1].text
                    estate_location_span_a = estate_location.find('a').text
                    estate_area = each_estate.find('div', class_="resblock-area").text
                    estate_price = each_estate.find('div', class_="resblock-price").find('div', class_="main-price")
                    estate_price_0 = estate_price.find_all('span')[0].text
                    estate_price_1 = estate_price.find_all('span')[1].text
                    print('{}'.format(estate_name))
                    print('{}/{}/{}'.format(estate_location_span_0, estate_location_span_1, estate_location_span_a))
                    print('{}'.format(estate_area))
                    print('{}{}'.format(estate_price_0, estate_price_1))
                    print('===========================================')


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_estate_demo.py'])
