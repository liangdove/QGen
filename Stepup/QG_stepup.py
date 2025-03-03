# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import time
import json
import random
from utils import read_file_to_list, read_list_to_file, Dic2JSON, save_as_json_file
from crawler.NewsAPI import NewsAPI_everything, NewsAPI_headlines # 一天100次额度，效果也不好

# 存储模块
all_json_response = []  # 用于存储所有的json响应
all_ques_response = []  # 用于存储所有问题
json_save_path = 'result_json_stepup.json'
ques_save_path = 'result_ques_stepup.txt'

# topic提取模块
topic_options = []

# topic_test = ["谁说这豆老啊,这豆太棒了", "GPT-4.5", "美国 “雅典娜” 月球着陆器", "中老 500 千伏联网工程", "随嫦娥六号返回的新疆牧草种子","日本米价暴涨", "中国硕龙 — 越南里板双边口岸开通", "中国制造业产品质量合格率"]

topic_options_LLM = ["GPT-4.5", "微软 Copilot for MacOS", 
                "亚马逊量子芯片 Ocelot", "Meta AR 眼镜 Aria Gen 2", 
                "Figure AI 人形机器人", "养老机器人国际标准", "小米 SU7 Ultra", 
                "综合极端条件实验装置", "四维高景一号 03、04 星", "美国 “雅典娜” 月球着陆器", 
                "中共中央办公厅《全国党员教育培训工作规划（2024—2028 年）》", 
                "商务部部长致信美国贸易代表", "中国黄岩岛战备警巡与执法巡查", "二十届中央纪委四次全会工作报告", 
                "俄美双边会谈", "朝鲜战略巡航导弹发射训练", "奥地利三党联合政府", "加拿大为强迫因纽特人搬迁道歉", 
                "欧盟第 16 轮对俄制裁", "巴以冲突", "美国对墨西哥、加拿大及欧盟加征关税", 
                "乌克兰与美国矿产框架协议", "中老 500 千伏联网工程", "中国硕龙 — 越南里板双边口岸开通", 
                "京津冀信用提升联合举措", "国家能源局 2025 新能源装机目标", "商务部跨境服务贸易负面清单", 
                "英伟达财报", "印尼主权基金启动", "上交所优化科创指数方案", "银行业保险业绿色金融方案", 
                "日本米价暴涨", "美英贸易协定谈判", "强冷空气影响中东部", "世界卫生组织刚果（金）不明疾病", 
                "北京花鳅新物种", "2025 年全国两会新闻中心", "哈尔滨冰雪大世界梦幻冰雪馆重启", 
                "青岛海岛低空物流航线开通", "新版《上海市轨道交通乘客守则》", "福建惠台利民措施", 
                "40 名中国籍偷渡人员被遣返", "临沂沂州实验学校女篮队员入选国家队", "沂河新区婚姻登记处揭牌", 
                "比勒费尔德枪击案", "加沙疫苗接种", "张译蒋欣《以法之名》", "电影《阴阳师 0》", "《奔跑吧 2025》", 
                "王鹤棣怒退《极限挑战》录制现场", "七星连珠", "土星", "水星", "海王星", "金星", "天王星", "木星", "火星", 
                "嫦娥六号月球背面样品研究成果", "“进步 MS-30” 货运飞船发射", "中国制造业产品质量合格率", "云南鱼类新物种", 
                "退役风机叶片防沙材料", "随嫦娥六号返回的新疆牧草种子", "12 届世界运动会火炬 “竹梦”", "第七批国家级烈士纪念设施", 
                "8600 车双燃料汽车运输船交付", "促进再生稻发展工作导引", "摩根士丹利人形机器人报告"]

# def extend_NewsAPI(q:str):
#     topic_options.extend(NewsAPI_everything(q))

def extend_clawler(file_path:str):
    topic_options.extend(read_file_to_list(file_path))
    
def extend_LLM_generated(list:list):
    topic_options.extend(list)

# News API慎用，效果不好
# NewsAPI_list = ["华盛顿", "乌克兰", "泽连斯基", "GPT4.5", "清洁能源", "哪吒2", "加沙", "NBA"]
# for q in NewsAPI_list:
#     extend_NewsAPI(q)
#     time.sleep(0.2)

# 爬虫方案
# extend_clawler("crawler\zhihu.txt")
extend_clawler("crawler\weibo_3.txt")

# LLM自己寻找话题方案
extend_LLM_generated(topic_options_LLM)

print("所有话题为:\n", topic_options)

# LLM生成模块
client = OpenAI(api_key="xxx", base_url="https://api.stepfun.com/v1")
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

tools = [
    {
        "type": "web_search",# 固定值
        "function": {
            "description": "这个web_search用来搜索互联网的信息。根据用户输入的想要了解的话题，从互联网网上收集该话题的相关资料，必须调用互联网搜索整合信息才能返回给用户，必须调用互联网搜索整合信息才能返回给用户！"# 描述什么样的信息需要大模型进行搜索。
        }
    }
]

start_time = time.time()
MAX_RETRIES = 2  # 最大重试次数
for i, topic in enumerate(topic_options):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            topic_time = time.time()
            messages = [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"请收集最近互联网上关于{topic}的信息，并根据收集到的内容精心设计出2个问题，每个问题字数在50字左右。搜索范围要多样化，比如从各类新闻、媒体、论坛等收集{topic}的相关信息。"},
            ]
            response = client.chat.completions.create(
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

