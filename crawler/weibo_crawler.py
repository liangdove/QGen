from bs4 import BeautifulSoup
import requests
import json

# 头数据
headers = {
    'scheme': 'https',
    'accept': 'text/html, application/xhtml+xml, application/xml',
    'accept-language': 'zh-CN, zh',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

# 发送请求获取数据
r = requests.get('https://weibo.com/ajax/statuses/hot_band', headers=headers)

try:
    # 转 JSON
    data = json.loads(r.text)
    # 尝试查找时间信息
    # 这里需要根据实际返回的数据结构调整查找方式
    # 假设返回数据中有 'update_time' 字段表示热榜更新时间
    hot_list_time = data.get('data', {}).get('update_time')
    if hot_list_time:
        print(f"微博热榜时间: {hot_list_time}")
    else:
        print("未找到微博热榜时间信息")

    # 总计内容
    textStr = ''
    # 遍历列表数据
    for index, item in enumerate(data['data']['band_list']):
        if 'topic_ad' not in item:
            # 标题
            word = item['word']
            itemStr = '{}'.format(word)
            textStr += str(itemStr + '\n')

    # 写入文件
    with open('data/weibo_2.txt', 'w', encoding="utf-8") as f:
        if hot_list_time:
            f.write(f"微博热榜时间: {hot_list_time}\n\n")
        f.write(textStr)
        print("已经写入当天热词")
        
except json.JSONDecodeError:
    print("无法解析返回的 JSON 数据")
    
except KeyError as e:
    print(f"数据结构与预期不符，缺少字段: {e}")
    
except Exception as e:
    print(f"发生未知错误: {e}")