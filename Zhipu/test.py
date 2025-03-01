from zhipuai import ZhipuAI
from datetime import datetime
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import Dic2JSON

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key="41863f9d3b7d4a998c8d6f1da1114c7f.P2e8qDmnGZUiEPxG")

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

search_prompt = """

# 以下是来自互联网的信息：
{search_result}

# 当前日期: 2024-03-01

# 要求：
必须通过互联网检索才能回答用户问题, 必须通过互联网检索才能回答用户问题!

"""
# 系统提示模板，包含时间信息
system_prompt = f"""
你是一个调用互联网搜索的联网问题提问专家，用户会要求你搜索互联网相关话题信息，并提出针对该话题的问题。
"""

topic = '0帧起手'
# 构建动态用户问题提示
user_prompt = f"收集最近互联网上关于{topic}的信息，并根据收集到的内容精心设计出2个问题，每个问题字数在50字左右，仅给出设计的问题即可。"

# 设置工具（启用网络搜索）
tools = [{
    "type": "web_search",
    "web_search": {
        "enable": True,  # 启用网络搜索
        "search_query": topic,
        "search_prompt": search_prompt 
    }
}]

# 构建消息
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

# 生成响应
response = client.chat.completions.create(
    model="glm-4-plus",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    stream=False,
    temperature=0.6  # 设置结果的随机性
)

# 输出结果
# json_response = Dic2JSON(response.choices[0].message)
print(response.choices[0].message)
# print(response)
