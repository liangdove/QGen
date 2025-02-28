from json import encoder
from bs4 import BeautifulSoup
import requests
import json


# 设置 头数据
headers = {'scheme': 'https',
           'accept': 'text/html, application/xhtml+xml, application/xml',
           'accept-language': 'zh-CN, zh',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
           }

# get请求 热榜地址
r = requests.get(
    'https://www.zhihu.com/billboard', headers=headers)


# 解析
soup = BeautifulSoup(r.text, 'html.parser')

# 获取页面内的js数据 并转换类型
data = json.loads(soup.find('script', {'id': 'js-initialData'}).get_text())

# 解析list类型的数据
jsonStr = data['initialState']['topstory']['hotList']

# 打印类型
print(type(jsonStr))


# 解析为json字符串
txt = json.dumps(jsonStr, ensure_ascii=False)

textStr = ''

for index, item in enumerate(jsonStr):
    titleArea = item['target']['titleArea']['text']
    excerptArea = item['target']['excerptArea']['text']
    imageArea = item['target']['imageArea']['url']
    metricsArea = item['target']['metricsArea']['text']
    link = item['target']['link']['url']
    itemStr = '{}'.format(
        titleArea)
    print(itemStr)
    textStr += itemStr+'\n'

# 保存json的字符串
with open('zhihu.txt', 'w', encoding="utf-8") as f:
    f.write(textStr)
