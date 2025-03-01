import json

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
            
    print("ques问题已成功写入文件。")

# dict转为JSON
def Dic2JSON(dic:dict):
    json_response = json.dumps(dic, indent=4, ensure_ascii=False) # JSON格式化字典
    print(json_response)
    return json_response

# dict list 存为 JSON 文件
def save_as_json_file(all_json_response:list, json_save_path):
    with open(json_save_path, 'w', encoding='utf-8') as f:
        json.dump(all_json_response, f, indent=4, ensure_ascii=False)
    print("json响应已经成功写入文件")
