## 目标
为了测试LLM的联网RAG能力，我们需要制定相应的问题数据集。根据评测标准评价LLM的RAG性能。

## 解析
我们制作的问题一定是只有在网络搜索的条件下才能得到对应问题的正确答案的。
5万个问题庞大，选择让现有的LLM生成。
所以问题转化为如何让LLM获取广泛的互联网信息，并进一步生成多样性、可靠性的问题。 

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

## demo3:
demo3是针对解决非失效性问题生成，设计了prompt。 

针对非时效性问题有两种方案：  
1. 利用LLM的生成能力进行生成。过程中发现的问题：必须提供一个专业领域（话题域），让LLM知道朝哪个方向进行生成。必须提出生成的问题的格式，比如事实、推理、多跳检索问题，否则LLM将会重复输出格式化的问题。效果见demo3文件夹。后续prompt可以继续优化。  
2. 从公开的问答数据集中提取出问题：
更新了data_timeless文件夹。  
目前选用了WebQA（4.2万个基于百度知道和其他资源的问题）和SougouQA（2.9万个搜狗用户的搜索记录）以及Math23k（2.3万个小学水平数学问题） 3个比较简单的问答数据集。后续可以从中筛选一些高质量的问题，关于怎么筛选还没有思路。  
原始数据集是json格式，数据量庞大没有上传。  

## 参考数据集链接：
https://rajpurkar.github.io/SQuAD-explorer/  
https://opendatalab.org.cn/OpenDataLab/SQuAD1_dot_1_dev/tree/main
https://blog.csdn.net/OpenDataLab/article/details/130208401  
https://github.com/InsaneLife/ChineseNLPCorpus  
https://github.com/CLUEbenchmark/CLUEDatasetSearch  
https://github.com/CyberCommy/baidu-wiki-500w  
 







