## 目标
为了测试LLM的联网RAG能力，我们需要制定相应的问题数据集。根据评测标准评价LLM的RAG性能。

## 解析
我们制作的问题一定是只有在网络搜索的条件下才能得到对应问题的正确答案的。
5万个问题庞大，选择让现有的LLM生成。
所以问题转化为如何让LLM获取广泛的互联网信息，并进一步生成多样性、可靠性的问题。

## 解决思路
1. 使用精心设计的prompt, 结合LLM的联网搜索功能，让他自己寻找topic, 并根据topic整合信息，生成问题。
    >弊端是LLM也不知道自己要找什么话题，从RAG的角度来讲，我们无论如何精心的设计prompt, 都不能命中LLM联网搜索的知识库，所以要给出LLM具体的话题，提高命中概率。

2. 如何有效收集具体的topic呢（比如关于“乌克兰签署矿产协议”）。NLP中这样的任务叫话题识别，是语义级别的任务，做起来麻烦（因为要联网，不是私有数据集）。所以我们干脆直接爬取微博、知乎热题，把他们做成topic。

3. 另一种有效收集topic方案是是使用LLM的联网功能，先行一步，收集网络话题（比如收集100个），然后将这些话题逐一做成prompt SQL,在让LLM生成问题，这样命中率会有极大的提升。比如我们可以这样问LLM：
    >帮我收集2024年12月份的网络热议话题比如从央视网、微博、知乎、虎扑、贴吧、抖音、sohu等平台收集。返回给我100个热议话题，不要给我多余的回答。

4. 我们将收集到的topic做成topics列表,下一步是根据列表中的热词，收集网络资料，逐一生成回答。通过遍历热词列表，我们可以实现问题生成自动化。经过各家厂商的测试，发现阶跃星辰的具有联网tool的API最好用。（一般厂商的API都遵循openai的格式规范，所以只需要替换API密钥和模型选项即可）

## 问题 
- 搜索范围单一，总是从news.qq.com收集信息
~~太慢，生成时间和topic在网络上的出现频次（热度）有关。比如“GPT4.5”话题要比“杨紫换装”话题产生对应问题的速度更快。猜测速度瓶颈主要在搜索上~~
- 找到了太慢的原因是LLM回复内容的复杂度和吐字数量。比如让LLM返回 “问题-参考答案-来源” 远比 返回 “问题” 时间开销大。前者平均时长100s, 后者平均时长15s
- 模型参数对搜索性能有影响？？

## cost计算（2个问题 <- 1个话题）
#### 钱:  
阶跃：  
21个话题->40个问题 （一个话题违法）  
10.34-0.91 = 0.93 r  
0.93 * 50000 / 24 = 1937.5 r  

智谱：  
一个话题2000 - 3000 tokens  
智谱新用户5百万+2百万额度  
一个用户 = 7 000 000 / 2500 = 2800 个话题  
需要大约10-20个新用户  
99r / 千万tokens  

kimi:  
0.03/query 额外收费  
50000 * 0.03 = 1500元，有点贵了，但是效果好  
还不算tokens价钱  

spark：
难用，tokens也不给优惠，需要websocket才能使用联网功能  

####  存储：  
json格式：150KB / 40个问题（20个话题）  
txt纯问题格式：60KB / 40个问题（20个话题）  

#### 时间:
智谱：  
9.6 min / 50个话题  
50000个话题大约需要9600min (16h)  

## demo
demo收集了腾讯新闻的10个板块的相关新闻标题，经过Bret预训练模型进行语义重复清洗，避免了重复话题的问题生成。每个板块裁剪了50个话题，每个话题生成2个问题，总共生成了1000个问题。  
评价：从json的tokens消耗上来讲，确实生成得到问题是经过联网搜索得到的，绝大多数符合“必须经过联网搜索才能得到答案这一要求”。  
但是有时候生成的两个问题之间有耦合关系，并不是两个独立的问题。（所以感觉一个话题生成1-3个问题比较合适）  
......  

## demo2
demo2 针对问题中‘非主观问题太少这个问题’进行了专门的prompt提示，修改prompt后非主观问题比例得到很大提高  
V1是修改的prompt  
V2是另一版prompt,效果比V1好  
V3是使用了V2的prompt,模型换成了qwen-max  





