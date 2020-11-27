import multiprocessing as mp
import os
import sys

import you_get


class YouGet:

    def __init__(self, path):
        self.path = path  # 存放视频文件

    def rmfile(self, path):
        """
        删除文件
        :param path: 文件路径
        :return: None
        """
        try:
            os.remove(path)
        except Exception as e:
            print(e)

    def download(self, url):
        sys.argv = ['you-get', '-o', self.path, url]
        you_get.main()

        # 下载完成，删除xml文件
        for file in os.listdir(self.path):
            if file[-3:] == 'xml':
                self.rmfile(os.path.join(self.path, file))


class MultiCore:
    def __init__(self, path):
        self.yg = YouGet(path)

    def job(self, urls):
        for url in urls:
            self.yg.download(url)

    def process(self, param=[], **kwargs):
        """
        :param param:
            self.job()函数的参数配置
        :param kwargs:
            processes: int, 核数，默认全部
        :return: 计算结果，list
        """
        pool = mp.Pool(processes=kwargs.get("processes"))  # 构建进程池
        pool.map(self.job, param)

    def split_list(self, ls, n):
        """
        将列表分成若干个个小列表
        :param ls: init list/numpy list
        :param n: split num
        :return: n small lists
        """
        if n > len(ls):
            print('分片数大于列表长度！')
        else:
            return [ls[i:i + n] for i in range(0, len(ls), n)]


if __name__ == "__main__":
    path = r"./files"
    urls = ["www.bilibili.com/bangumi/play/ss34440?theme=movie" + str(_) for _ in range(1, 107)]  # 目标视频urls列表

    mc = MultiCore()
    data = mc.split_list(urls, 8)  # 将urls分成8份
    mc.process(param=data)
