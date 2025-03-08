#### 从共有数据集收集的关于常识性非时效性问题
参考链接：
https://bbs.huaweicloud.com/blogs/401690  

```
SogouQA

数据源链接：https://aistudio.baidu.com/aistudio/datasetdetail/17514

领域：百科

语言：中文

文件：SogouQA.json

数据量：questions count: 29812；qas count: 297336；valid_answer_qas_cnt: 115560；answers cnt: {0: 1, 1: 20058, 2: 7734, 3: 1687, 4: 299, 5: 30, 6: 3}

数据格式：

json文件，一个问题有多个回答，有的回答里没有答案，有的多个回答的答案是重复的；20058个问题有1个答案 … 所有answer都在passage里可以找到

简介：

2018年CIPS-SOGOU问答比赛数据；来自于搜狗搜索引擎真实用户提交的查询请求；含有事实类与非事实类数据;数据量：297.3K；问题类型：单片段抽取.（本数据只有事实类数据，非事实类数据是长文本）（不过好像passage有省略号，不知道是源数据集就是非全文本还是找的数据集不对）

http://task.www.sogou.com/cips-sogou_qa/
```

```
百度WebQA

数据源链接：https://aistudio.baidu.com/aistudio/datasetdetail/17514

领域：百科

语言：中文

文件：WebQA.json

数据量：questions count: 42223；qas count: 569260；valid_answer_qas_cnt: 213742；answers cnt: {0: 115, 1: 42064, 2: 44}

数据格式：

json文件，一个问题有多个回答，有的回答里没有答案，有的多个回答的答案是重复的；42064个问题有1个答案，115个问题没有答案，44个问题有两个答案；所有answer都在passage里可以找到

简介：

基于百度知道和其他资源，一个问题-多个passage&答案，没有答案则为空。为事实性问答。问题-答案都不长。（不过好像passage有省略号，不知道是源数据集就是非全文本还是找的数据集不对）（需要去除掉answer前面的“答：”）

https://spaces.ac.cn/archives/4338
```