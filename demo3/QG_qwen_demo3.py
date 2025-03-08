from zhipuai import ZhipuAI
from datetime import datetime
import os
import sys
import time
import random
from openai import OpenAI

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import read_file_to_list, read_list_to_file, Dic2JSON, save_as_json_file


class TopicProcessor:
    def __init__(self):
        # self.category = category
        # self.file = file
        self.all_json_response = []
        self.all_ques_response = []
        self.history = []
        self.json_save_path = f'demo3\sample.json'
        self.ques_save_path = f'demo3\sample.txt'
        self.topic_options = []
        self.client = OpenAI(
            api_key="xxx",
            base_url="https://api.agicto.cn/v1"
        )
        self.search_prompt = """

        # 这是用户调用的互联网搜索工具

        # 当前日期: 2024-03-08

        # 要求：
        必须通过互联网检索才能回答用户问题, 必须通过互联网检索才能回答用户问题!

        """
        self.system_prompt = f"""
        你是一个使用互联网工具进行搜索的问题生成专家，用户会要求你你生成如下几个类型的问题：
            ​事实型​（例如："珠穆朗玛峰的高度是多少？"）
            ​推理型​（例如："为什么气候变化会导致冰川融化？"）
            ​多跳检索​（例如："爱因斯坦获得诺贝尔奖的年份，当时他的国籍是什么？"）
        请你根据用户提供的专业领域，提出相应的需要检索外部知识和生成准确答案的问题。
        """

    def extend_clawler(self, file_path):
        self.topic_options.extend(read_file_to_list(file_path))

    def extend_LLM_generated(self, list_data):
        self.topic_options.extend(list_data)

    def process_topics(self):
        # self.extend_clawler(self.file)
        start_time = time.time()
        MAX_RETRIES = 2  # 最大重试次数
        SAVE_TRAL = 5  # 保存间隔
        for i in range(5):
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    topic_time = time.time()
                    user_prompt = f"你是微生物专业领域的专家，请从网上收集专业资料，针对事实型、推理型、多跳检索型这三种类型的问题，每一种类型提出10个有价值的问题。注意不要和你已经提出的问题重复。仅仅给出设计的问题即可，不要返回多余的内容。"
                    self.history.append({"role": "system", "content": self.system_prompt})
                    self.history.append({"role": "user", "content": user_prompt})
                    messages = self.history
                    # 设置工具（启用网络搜索）
                    # tools = [{
                    #     "type": "web_search",
                    #     "web_search": {
                    #         "enable": True,  # 启用网络搜索
                    #         "search_query": topic,
                    #         "search_prompt": self.search_prompt
                    #     }
                    # }]
                    # 生成响应
                    response = self.client.chat.completions.create(
                        model="qwen-max",
                        messages=messages,
                        # tools=tools,
                        # tool_choice="auto",
                        stream=False,
                        temperature=0.7,  # 设置结果的随机性
                        extra_body={"enable_search": True}
                    )
                    # print(f"第 {i + 1} 个话题是: {topic}")
                    random_time = random.uniform(5, 8)
                    # print(type(response))

                    # 打印响应内容
                    if response.choices:
                        message_content = response.choices[0].message.content
                        self.history.append({"role": "assistant", "content": message_content})
                        if message_content:
                            print(f"第{i + 1}轮响应内容:")
                            print(message_content)
                            self.all_ques_response.append(message_content)  # 将问题添加到列表中

                    response_dict = response.model_dump()  # 将响应对象转换为字典
                    self.all_json_response.append(response_dict)  # 将响应字典添加到列表中

                    time.sleep(random_time)
                    topic_time_cost = time.time() - topic_time
                    print(f"该话题耗时：{topic_time_cost:.3f}\n")
                    break  # 请求成功，跳出重试循环
                except Exception as e:
                    print(f"请求时发生错误: {e}，正在进行第 {retries + 1} 次重试...")
                    retries += 1
                    time.sleep(2)  # 等待 2 秒后重试

            if retries == MAX_RETRIES:
                print(f"请求失败，已达到最大重试次数，跳过该话题。\n")
                continue  # 跳过当前话题，进入下一个话题的循环

            if (i + 1) % SAVE_TRAL == 0 and i != 0:
                # 将所有响应列表以 JSON 格式写入文件
                print(f"已保存{i + 1}个话题\n")
                save_as_json_file(self.all_json_response, self.json_save_path)
                # 将所有生成的问题存为txt文件，一行代表一个问题：
                read_list_to_file(self.all_ques_response, self.ques_save_path)

        # 循环结束后再次保存，确保最后一部分数据也被保存
        save_as_json_file(self.all_json_response, self.json_save_path)
        read_list_to_file(self.all_ques_response, self.ques_save_path)
        print("已经全部保存")

        # 总耗时
        all_time_cost = time.time() - start_time
        print(f"总耗时：{all_time_cost:.3f}")


if __name__ == "__main__":
    # 获取当前日期
    current_date = datetime.now().strftime("%Y-%m-%d")

    # file_dict2 = {
    #     "娱乐": "demo2/V3_qwen/qq_ent_sm.txt",
    #     "电竞": "demo2/V3_qwen/qq_esports.txt",
    #     "财经": "demo2/V3_qwen/qq_finance.txt",
    #     "游戏": "demo2/V3_qwen/qq_games.txt",
    #     "理财": "demo2/V3_qwen/qq_licai.txt",
    #     "军事": "demo2/V3_qwen/qq_milite.txt",
    #     "体育": "demo2/V3_qwen/qq_sports.txt",
    #     "科技": "demo2/V3_qwen/qq_tech.txt",
    #     "全球": "demo2/V3_qwen/qq_world.txt",
    #     "教育": "demo2/V3_qwen/qq_edu.txt"
    # }
    
    # file_dict = {
    #     "测试":"demo2/V3_qwen/test.txt"
    # }

    # for category, file in file_dict.items():
    # print(f"开始处理 {category} 分类的文件: {file}")
    processor = TopicProcessor()
    processor.process_topics()