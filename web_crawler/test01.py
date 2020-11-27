import pytest

'''
pytest参数化
'''

# 列表
data = ['123', '456']


# @pytest.mark.do
@pytest.mark.parametrize('pwd', data)
def test1(pwd):
    print(pwd)


# 元组
data2 = [(1, 2, 3), (4, 5, 6)]


# @pytest.mark.do
@pytest.mark.parametrize('a,b,c', data2)
def test2(a, b, c):
    print(a, b, c)


# 字典
data3 = (
    {'user': 'admin', 'pwd': 123456},
    {'age': 18, 'sex': '男'}
)


# @pytest.mark.undo
@pytest.mark.parametrize('dic', data3)
def test3(dic):
    print(dic)
