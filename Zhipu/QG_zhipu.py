from zhipuai import ZhipuAI
from datetime import datetime
import os
import sys
import time
import random
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import read_file_to_list, read_list_to_file, Dic2JSON, save_as_json_file
# from crawler.NewsAPI import NewsAPI_everything, NewsAPI_headlines # 一天100次额度，效果也不好
# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

# 存储模块
all_json_response = []  # 用于存储所有的json响应
all_ques_response = []  # 用于存储所有问题
json_save_path = 'result_json_zhipu.json'
ques_save_path = 'result_ques_zhipu.txt'

topic_options = []

def extend_clawler(file_path:str):
    topic_options.extend(read_file_to_list(file_path))
    
def extend_LLM_generated(list:list):
    topic_options.extend(list)

# 爬虫方案
# extend_clawler("crawler\zhihu.txt")
extend_clawler("crawler\weibo_3.txt")

# LLM自己寻找话题方案
# extend_LLM_generated(topic_options_LLM)

print("所有话题为:\n", topic_options)

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key="41863f9d3b7d4a998c8d6f1da1114c7f.P2e8qDmnGZUiEPxG")

search_prompt = """

# 以下是来自互联网的信息：
{search_result}

# 当前日期: 2024-03-01

# 要求：
必须通过互联网检索才能回答用户问题, 必须通过互联网检索才能回答用户问题!

"""

system_prompt = f"""
你是一个调用互联网搜索的联网问题提问专家，用户会要求你搜索互联网相关话题信息，并提出针对该话题的问题。
"""

start_time = time.time()
MAX_RETRIES = 2  # 最大重试次数
for i, topic in enumerate(topic_options):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            topic_time = time.time()
            

            user_prompt = f"收集最近互联网上关于{topic}的信息，并根据收集到的内容精心设计出2个问题，每个问题字数在50字左右，仅给出设计的问题即可。"

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            # 设置工具（启用网络搜索）
            tools = [{
                "type": "web_search",
                "web_search": {
                    "enable": True,  # 启用网络搜索
                    "search_query": topic,
                    "search_prompt": search_prompt 
                }
            }]
            # 生成响应
            response = client.chat.completions.create(
                model="glm-4-plus",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                stream=False,
                temperature=0.6  # 设置结果的随机性
            )
            print(f"第 {i + 1} 个话题是: {topic}")
            random_time = random.uniform(5, 10)
            response_dict = response.model_dump()  # 将响应对象转换为字典
            all_json_response.append(response_dict)  # 将响应字典添加到列表中
            all_ques_response.append(response.choices[0].message.content) # 将问题添加到列表中
            print(response.choices[0].message.content)
            time.sleep(random_time)
            topic_time_cost = time.time() - topic_time
            print(f"该话题耗时：{topic_time_cost:.3f}\n")
            break  # 请求成功，跳出重试循环
        except Exception as e:
            print(f"请求 {topic} 时发生错误: {e}，正在进行第 {retries + 1} 次重试...")
            retries += 1
            time.sleep(2)  # 等待 2 秒后重试

    if retries == MAX_RETRIES:
        print(f"请求 {topic} 失败，已达到最大重试次数，跳过该话题。\n")
        continue  # 跳过当前话题，进入下一个话题的循环

    if (i + 1) % 5 == 0 and i != 0: 
        # 将所有响应列表以 JSON 格式写入文件
        print(f"已保存{i + 1}个话题\n")
        save_as_json_file(all_json_response, json_save_path)

        # 将所有生成的问题存为txt文件，一行代表一个问题：
        read_list_to_file(all_ques_response, ques_save_path)
        
# 循环结束后再次保存，确保最后一部分数据也被保存
save_as_json_file(all_json_response, json_save_path)
read_list_to_file(all_ques_response, ques_save_path)
print("已经全部保存")


# 总耗时
all_time_cost = time.time() - start_time
print(f"总耗时：{all_time_cost:.3f}")