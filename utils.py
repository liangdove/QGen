import json
import pandas as pd
import spacy
import csv

# txt 转 list
def read_file_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 使用splitlines方法将内容按行分割成列表
            lines_list = content.splitlines()
        return lines_list
    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到。")
        return []
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []
    
# file_path = "weibo.txt"
# result_list = read_file_to_list(file_path)
# print(result_list)

# list 转 txt
def read_list_to_file(list:list, path:str):
    # 打开文件以写入模式
    with open(path, 'w', encoding='utf-8') as file:
        # 遍历列表中的每一项
        for item in list:
            # 将每一项和换行符写入文件
            file.write(item + '\n')
            
    print("列表项已成功写入txt文件。")

# dict转为JSON
def Dic2JSON(dic:dict):
    json_response = json.dumps(dic, indent=4, ensure_ascii=False) # JSON格式化字典
    # print(json_response)
    return json_response

# dict list 存为 JSON 文件
def save_as_json_file(all_json_response:list, json_save_path):
    with open(json_save_path, 'w', encoding='utf-8') as f:
        json.dump(all_json_response, f, indent=4, ensure_ascii=False)
    print("json响应已经成功写入文件")

# xlsx转csv
def xlsx_to_csv(xlsx_file_path, csv_file_path):
    try:
        # 读取XLSX文件
        df = pd.read_excel(xlsx_file_path)
        df.to_csv(csv_file_path, index=False)
        print(f"成功将 {xlsx_file_path} 转换为 {csv_file_path}")
    except Exception as e:
        print(f"转换过程中出现错误: {e}")

# xlsx_file = 'qq_scrap_world_0301.xlsx'  
# csv_file = 'qq_scrap_world_0301.csv'    
# xlsx_to_csv(xlsx_file, csv_file)

# csv的新闻话题转txt
def csv_first_column_to_txt(csv_file_path, txt_file_path, con):
    try:
        # 以只读模式打开 CSV 文件
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            # 创建 CSV 读取器对象
            csv_reader = csv.reader(csv_file)
            # 以写入模式打开 TXT 文件
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                # 遍历 CSV 文件的每一行
                for row in csv_reader:
                    if row:
                        # 提取第一列数据
                        first_column = row[con]
                        # 将第一列数据写入 TXT 文件，并添加换行符
                        txt_file.write(f"{first_column}\n")
        print(f"成功将 {csv_file_path} 的第 {con} 列数据复制到 {txt_file_path}")
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

# 调用函数进行转换
csv_file = 'data/qq_scrap_edu_0301.csv'  
txt_file = 'data/qq_scrap_edu_0301.txt'   
csv_first_column_to_txt(csv_file, txt_file, 0)





        