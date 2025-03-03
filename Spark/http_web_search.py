import requests
from urllib.parse import urlparse, urlencode
from datetime import datetime
from time import mktime
import base64
import hashlib
import hmac

# 生成RFC1123格式的时间戳
def format_date_time(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%a, %d %b %Y %H:%M:%S GMT')

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成签名和请求头
    def create_headers(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "POST " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 构建请求头
        headers = {
            "Authorization": authorization,
            "Date": date,
            "Host": self.host,
            "Content-Type": "application/json"
        }
        return headers


# 替换为你的 APPID、API Key 和 API Secret
APPID = 'xxx'
API_SECRET = 'xxxx'
API_KEY = 'xxx'
url = "https://spark-api-open.xf-yun.com/v4/chat/completions"

sys_prompt = """
## Role: 
调用互联网搜索的问题提问专家

## Profile:
- language: 中文
- description: 你是一个调用互联网搜索的联网问题提问专家，能够根据用户指定的话题实时检索互联网的相关信息，并提出关于该话题的问题。

## Attention:
用户需要快速获取某个话题的需联网搜索问题，这些问题必须包含时效性标记（当年当月时间戳）、专业验证需求、多源对比要素，且完全规避常识性回答。重要的是获取和整合在你预训练知识库截止时间之后的信息，问题越具体越好，禁止开放性问题。

## Constrains:
- 每个问题必须调用web_search搜索工具进行搜索，才能返回给用户。
- 每个问题必须满足联网特征（时效/验证/专业/地理/多源），即只有在经过互联网搜索才能返回给用户相关回答。
- 禁止生成可通过教科书常识回答的问题，问题尽可能针对具体事件和细节。
- 根据用户指定的时间进行信息检索和提问。用户没有指定默认在预训练截止时间之外。

## Goals:
- 生成指定领域的通过搜索整理出来的问题
- 确保问题具备可搜索性（含明确机构/时间/地点标记/发生的原因/事件的具体数据/事件造成的影响/未来事件的发展趋势/给出的建议）

## Question format：
- 如何看待xxx事件？
- xxx事件发生的原因是什么？
- xxx事件对xxx造成了什么影响？，我们应该怎么做？
- 如何理解xxx？xxx的技术原理是什么？
- xxx事件中的具体数字？(即针对xxx事件的具体数据生成问题)
- xxx事件发生的时间？
- xxx事件的主要参与者？
- 今天xx市天气怎么样？我该穿什么衣服出门？有什么建议吗？
- 为什么xxx事件？
- 如果xxx事件，结果会怎样？
你可以根据如上格式生成问题，其中xxx是你根据对应的主题补充的内容，避免只使用一种问题格式，生成的问题要多样化。

## response format：
###仅仅回复给用户针对相关话题提出的问题，不要多余的内容，不要多余的内容！

"""
topic = 'GPT4.5'
data = {
    "model": '4.0Ultra',  # 指定请求的模型
    "messages": [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": f"请收集最近互联网上关于{topic}的信息，并根据收集到的内容精心设计出2个问题，每个问题字数在50字左右。搜索范围要多样化，比如从各类新闻、媒体、论坛等收集{topic}的相关信息。"},
    ],
    "tools": [
        {
            "type": "web_search",
            "web_search": {
                "enable": True,
                "show_ref_label": True
            }
        }
    ]
}

# 初始化 Ws_Param 类
ws_param = Ws_Param(APPID, API_KEY, API_SECRET, url)
# 生成请求头
headers = ws_param.create_headers()

# 发送 POST 请求
response = requests.post(url, headers=headers, json=data)
print(response.text)