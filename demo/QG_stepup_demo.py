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
    def __init__(self, category, file):
        self.category = category
        self.file = file
        self.all_json_response = []
        self.all_ques_response = []
        self.json_save_path = f'demo/result_json_stepup_{self.category}.json'
        self.ques_save_path = f'demo/result_stepup_{self.category}.txt'
        self.topic_options = []
        self.client = OpenAI(api_key="xxx", base_url="xxx")
        self.search_prompt = """

        # 以下是来自互联网的信息：
        {search_result}

        # 当前日期: 2024-03-02

        # 要求：
        必须通过互联网检索才能回答用户问题, 必须通过互联网检索才能回答用户问题!

        """
        # self.system_prompt = f"""
        # 你是一个{self.category}领域以及互联网搜索的问题提问专家，用户会要求你搜索互联网相关话题信息，并针对该新闻事件的数据、原因、措施、影响等进行提问。
        # """
        self.system_prompt = """
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
            - 列举xxx事件的具体数据？
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

    def extend_clawler(self, file_path):
        self.topic_options.extend(read_file_to_list(file_path))

    def extend_LLM_generated(self, list_data):
        self.topic_options.extend(list_data)

    def process_topics(self):
        self.extend_clawler(self.file)
        start_time = time.time()
        MAX_RETRIES = 2  # 最大重试次数
        for i, topic in enumerate(self.topic_options):
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    topic_time = time.time()
                    # user_prompt = f"对于腾讯新闻上关于“{topic}”的讨论，请搜索相关内容并精心设计出2个问题，仅给出设计的问题即可。"
                    user_prompt = f"请收集最近互联网上关于{topic}的信息，并根据收集到的内容精心设计出2个问题，每个问题字数在50字左右。搜索范围要多样化，比如从各类新闻、媒体、论坛等收集{topic}的相关信息。"
                    messages = [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                    # 设置工具（启用网络搜索）
                    tools = [
                        {
                            "type": "web_search",# 固定值
                            "function": {
                                "description": "这个web_search用来搜索互联网的信息。根据用户输入的想要了解的话题，从互联网网上收集该话题的相关资料，必须调用互联网搜索整合信息才能返回给用户，必须调用互联网搜索整合信息才能返回给用户！"# 描述什么样的信息需要大模型进行搜索。
                            }
                        }
                    ]
                    # 生成响应
                    # response = self.client.chat.completions.create(
                    #     model="glm-4-plus",
                    #     messages=messages,
                    #     tools=tools,
                    #     tool_choice="auto",
                    #     stream=False,
                    #     temperature=0.6  # 设置结果的随机性
                    # )
                    response = self.client.chat.completions.create(
                            model="step-1-8k",
                            messages=messages,
                            # response_format={ "type": "json_object" },
                            tool_choice="auto",
                            tools=tools,  # 启用工具
                            stream=False,
                            temperature=0.6  # 设置结果的随机性
                    )
                    print(f"第 {i + 1} 个话题是: {topic}")
                    random_time = random.uniform(5, 10)
                    response_dict = response.model_dump()  # 将响应对象转换为字典
                    self.all_json_response.append(response_dict)  # 将响应字典添加到列表中
                    self.all_ques_response.append(response.choices[0].message.content)  # 将问题添加到列表中
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

    file_dict = {

        "娱乐": "demo/qq_ent.txt",
        "电竞": "demo/qq_esports.txt",
        "财经": "demo/qq_finance.txt",
        "游戏": "demo/qq_games.txt",
        "理财": "demo/qq_licai.txt",
        "军事": "demo/qq_milite.txt",
        "体育": "demo/qq_sports.txt",
        "科技": "demo/qq_tech.txt",
        "全球": "demo/qq_world.txt",
        "教育": "demo/qq_edu.txt"
    }

    for category, file in file_dict.items():
        print(f"开始处理 {category} 分类的文件: {file}")
        processor = TopicProcessor(category, file)
        processor.process_topics()