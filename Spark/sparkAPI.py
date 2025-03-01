# coding: utf-8
import _thread as thread
import os
import time
import random
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket
import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import Dic2JSON

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
sys_prompt2 = "在用户提出请求后，你要使用网络搜索功能，从互联网上搜集相关信息，整理后然后返回给用户。"

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, close_status_code, close_msg):
    print("**closed**")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # content = Dic2JSON(data)
        print(content,end='')
        if status == 2:
            # print("#### 关闭会话")
            ws.close()


def gen_params(appid, query, domain):
    """
    通过appid和用户的提问来生成请参数
    """

    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",           
            # "patch_id": []    #接入微调模型，对应服务发布后的resourceid          
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096,
                "auditing": "default",
                "show_ref_label": True
            }
        },
        "payload": {
            "message": {
                "text": [{"role":"system","content":sys_prompt},
                         {"role": "user", "content": query}]
            }
        }
    }
    return data


def test(appid, api_secret, api_key, Spark_url, domain, query):
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()

    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.query = query
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

topic_test = ["谁说这豆老啊,这豆太棒了", "GPT-4.5", "美国 “雅典娜” 月球着陆器", "中老 500 千伏联网工程", "随嫦娥六号返回的新疆牧草种子","日本米价暴涨", "中国硕龙 — 越南里板双边口岸开通", "中国制造业产品质量合格率"]
for topic in topic_test:
    print(f"当前topic:{topic}")
    test(appid = '180d9048',
            api_secret = 'NDUxOTY2NmUyMzkzZTA4YWU3MWJiZWY1',
            api_key = '4e4c3c685952c51c62d52826e314417a',
            #星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
            domain = '4.0Ultra',
            #appid、api_secret、api_key三个服务认证信息请前往开放平台控制台查看（https://console.xfyun.cn/services/bm35）
            # Spark_url="wss://spark-api.xf-yun.com/v3.5/chat",      # Max环境的地址   
            Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat" , # 4.0Ultra环境的地址
            # Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro环境的地址
            # Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite环境的地址
            # domain = "generalv3"    # Pro版本
            # domain = "lite"      # Lite版本址
            query=f"针对{topic}这个话题或网络热词，启用你的网络搜索工具，从网络上给我搜集资料，并提出2个问题，每个问题字数在50字左右。")
    random_time = random.uniform(2, 3)
    time.sleep(random_time)
    