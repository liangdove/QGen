# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import time
import json
from file2list import read_file_to_list

client = OpenAI(api_key="f70rlr8gJsjNjFkA33DuPE3jkcbDINX4HSR6qkdUMsWcqLnAgVpECgcjD4dZ5PZL", base_url="https://api.stepfun.com/v1")

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

topic_options_crawler = []
crawled_file_path = "weibo.txt"
topic_options_crawler.extend(read_file_to_list(crawled_file_path))

# print(topic_options_crawler)

sys_prompt = """
## Role: 
领域联网问题生成专家

## Profile:
- language: 中文
- description: 你是一个领域定向的联网问题生成专家，能够根据用户指定的领域批量产出需要实时检索的问题集合。你需要整合该方面联网搜索的最新信息，来生成出你现有预训练知识库所不能正确回答的问题，专为特定领域批量产出需实时验证的高质量搜索问题。

## Attention:
用户需要快速获取某个垂直领域的大量需联网搜索问题，这些问题必须包含时效性标记（当年当月时间戳）、专业验证需求、多源对比要素，且完全规避常识性回答。重要的是获取和整合在你预训练知识库截止时间之后的信息，问题越具体越好，禁止开放性问题。

## Constrains:
- 每个问题必须满足至少2个联网特征（时效/验证/专业/地理/多源）
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
问题1: xxxxxx # 总结整理后提出的问题
回答1: xxxxxx # 该问题对应的答案
问题1来源: xxxxxx

问题2: xxxxxx
回答2: xxxxxx
问题2来源: xxxxxx

问题3: xxxxxx
回答3: xxxxxx
问题3来源: xxxxxx

......

注意不要回答多余的文字，仅仅给出如上的回答格式即可。
"""

tools = [
    {
        "type": "web_search",# 固定值
        "function": {
            "description": "这个web_search用来搜索互联网的信息"# 描述什么样的信息需要大模型进行搜索。
        }
    }
]

for topic in topic_options_crawler:
    messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"请收集最近互联网上关于{topic}的信息,，并根据收集到的内容精心设计出3个问题，每个问题字数在50字左右。搜索范围要多样化，比如从央视网、微博、知乎、虎扑、贴吧、抖音、sohu等平台收集{topic}的相关信息，给出使用搜索工具搜索出的来源。"},
        ]
    response = client.chat.completions.create(
        model="step-1-8k",
        messages=messages,
        # response_format={ "type": "json_object" },
        tool_choice="auto",
        tools=tools, # 启用工具
        stream=False,
        temperature=0.6 # 设置结果的随机性
    )
    
    print(f"当前topic:{topic}\n")
    print(response.choices[0].message.content)
    

    # response_dict = response.model_dump() # 将响应对象转换为字典
    # formatted_response = json.dumps(response_dict, indent=4, ensure_ascii=False) # JSON格式化字典
    # print(formatted_response)
    time.sleep(0.5)
    
    
    

