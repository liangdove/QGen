import torch
from sentence_transformers import SentenceTransformer, util
from utils import read_file_to_list, read_list_to_file
import spacy

# 下载去重预训练模型LaBSE，现在模型已经保存到了model目录
# model = SentenceTransformer('sentence-transformers/LaBSE')
# model.save('model')

def del_empty_lines(file_path:str, file_path_processed:str):
    try:
        with open(file_path, "r", encoding = 'utf-8') as file:
            lines = file.readlines()
        non_empty_lines = [line for line in lines if line.strip()]
        
        with open(file_path_processed, "w", encoding='utf-8') as file:
            file.writelines(non_empty_lines)
        print(f"已成功消除的空行")
    
    except Exception as e:
        print("发生错误：", e)
        
def char_limit(file_path, file_path_processed, min:int, max:int):
    try:
        # 打开文件，读取所有行
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 筛选出符合条件的行
        selected_lines = []
        for line in lines:
            # 去除行末的换行符
            line = line.strip()
            # 检查行的字数是否在 5 到 40 之间
            if min < len(line) < max:
                selected_lines.append(line + '\n')
        # 将筛选后的行写回原文件
        with open(file_path_processed, 'w', encoding='utf-8') as file:
            file.writelines(selected_lines)
        print("已成功完成字符数量限制筛选")
    except FileNotFoundError:
        print(f"未找到文件: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

# 去除重复语义的话题
def remove_semantic_similar_topics(file_path, file_path_processed ,threshold=0.8):
    # nlp = spacy.load('zh_core_web_md') # 使用预训练?
    nlp = spacy.load('zh_core_web_sm') # 使用磁性标记和命名实体识别
    with open(file_path, 'r', encoding='utf-8') as file:
        topics = [line.strip() for line in file.readlines()]

    unique_topics = []
    for topic in topics:
        doc1 = nlp(topic)
        is_similar = False
        for unique_topic in unique_topics:
            doc2 = nlp(unique_topic)
            similarity = doc1.similarity(doc2)
            if similarity >= threshold:
                is_similar = True
                break
        if not is_similar:
            unique_topics.append(topic)

    with open(file_path_processed, 'w', encoding='utf-8') as file:
        for topic in unique_topics:
            file.write(topic + '\n')
        rate = len(unique_topics) / len(topics)
        print("已成功去除语义重复的话题，保留比例为", rate, "%")

    
file_path = "data/test.txt"

# 去重操作
def semanticTextualDeduplication_loop(lines, threshold):
    embedder = SentenceTransformer("model_torch")
    corpus = []
    corpus.append(lines[0])
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    lines.pop(0)
    for line in lines:
        queries = [line]
        print('line: {0} and corpus.size: {1}'.format(line, len(corpus)))
        query_embedding = embedder.encode(queries, convert_to_tensor=True)
        if not semantic_search_exist(query_embedding, corpus_embeddings, threshold, line):
            corpus.append(line)
            print('before corpus_embeddings size: {0}'.format(len(corpus_embeddings)))
            # 沿着指定维度拼接张量
            corpus_embeddings = torch.cat((query_embedding, corpus_embeddings), dim=0)
            print('end corpus_embeddings size: {0}'.format(len(corpus_embeddings)))
    rate = (len(corpus) / len(lines)) * 100
    print("已完成语义去重，保留比例为", rate, "%")
    return corpus

def semantic_search_exist(query_embedding, corpus_embeddings, threshold, query):
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=1)
    hits = hits[0]
    hits = hits[0]
    score = hits['score']
    print('input: {0} and output: {1}'.format(query, hits['score']))
    if score > threshold:
        return True
    return False
 
def pre_process_file(file_path, proc_file_path, tar_file_path, min:int=6, max:int=40, threshold:int=0.9):

    del_empty_lines(file_path,proc_file_path)
    char_limit(proc_file_path, proc_file_path, min, max)
    # remove_semantic_similar_topics(proc_file_path, proc_file_path, threshold)
    result = semanticTextualDeduplication_loop(read_file_to_list(proc_file_path), threshold)
    read_list_to_file(result, tar_file_path)
    print("话题预处理完成")
    
if __name__ == "__main__":
    # 执行去重
    src_file_path = 'data/test.txt'
    proc_file_path = 'data/proc_test.txt'
    tar_file_path = 'data/tar_test.txt'
    pre_process_file(src_file_path, proc_file_path, tar_file_path, 6, 40, 0.9)

    
