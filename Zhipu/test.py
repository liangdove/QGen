from zhipuai import ZhipuAI
from datetime import datetime
import os
import sys
import time
import random
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import read_file_to_list, read_list_to_file, Dic2JSON, save_as_json_file

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key="xxx.xxx")

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
system_prompt = """
你是一个调用互联网搜索的联网问题提问专家，用户会要求你搜索互联网相关话题信息，并提出针对该话题的问题。你可以针对话题的数据、方法、措施、原因、影响等进行提问。
"""

topics2 = ["GPT-4.5", "英伟达财报", "微软 Copilot for MacOS", "四维高景一号 03、04 星", "美国 “雅典娜” 月球着陆器", 
        "商务部部长致信美国贸易代表", "中国黄岩岛战备警巡与执法巡查", "二十届中央纪委四次全会工作报告", 
        "朝鲜战略巡航导弹发射训练", "奥地利三党联合政府", "加拿大为强迫因纽特人搬迁道歉", 
        "欧盟第 16 轮对俄制裁", "美国对墨西哥、加拿大及欧盟加征关税", 
        "乌克兰与美国矿产框架协议", "中国硕龙 — 越南里板双边口岸开通", 
        "亚马逊量子芯片 Ocelot", "Meta AR 眼镜 Aria Gen 2", 
        "Figure AI 人形机器人", "养老机器人国际标准", "小米 SU7 Ultra",
        "京津冀信用提升联合举措", "国家能源局 2025 新能源装机目标", "商务部跨境服务贸易负面清单", 
        "印尼主权基金启动", "上交所优化科创指数方案", "银行业保险业绿色金融方案",  "美英贸易协定谈判", 
        "强冷空气影响中东部", "世界卫生组织刚果（金）不明疾病", 
        "北京花鳅新物种", "青岛海岛低空物流航线开通","40 名中国籍偷渡人员被遣返", "临沂沂州实验学校女篮队员入选国家队",
        "王鹤棣怒退《极限挑战》录制现场", "七星连珠","嫦娥六号月球背面样品研究成果", "“进步 MS-30” 货运飞船发射", 
        "12 届世界运动会火炬 “竹梦”", "第七批国家级烈士纪念设施", "8600 车双燃料汽车运输船交付"]

topics = read_file_to_list("crawler/test.txt")

for topic in topics:
    
    # 构建动态用户问题提示
    user_prompt2 = f"收集最近互联网上关于{topic}的信息，并根据收集到的内容精心设计出2个问题，每个问题字数在50字左右，仅给出设计的问题即可。"
    user_prompt = f"请收集最近互联网上关于{topic}的信息，并根据收集到的内容精心设计出2个问题，每个问题字数在50字左右。搜索范围要多样化，比如从各类新闻、媒体、论坛等收集{topic}的相关信息，仅给出设计的问题即可。"
    
    # 构建消息
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

    # 输出结果
    # json_response = Dic2JSON(response.choices[0].message)
    print("当前topic:", topic)
    print(response.choices[0].message)
    # print(response)
