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