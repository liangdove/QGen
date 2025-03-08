import json

def json_to_ques(file_path, output_file_path):
    try:
        # 打开 JSON 文件并以只读模式和 UTF-8 编码读取
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用 json.load() 函数从文件中加载 JSON 数据，将其转换为 Python 字典
            data = json.load(file)

            # # data 是 列表
            if isinstance(data, list):
                all_questions = []
                for item in data:
                    question = item.get('question')
                    if question:
                        all_questions.append(question)
            
            # 如果 data 是一个字典，则直接提取 question
            elif isinstance(data, dict):
                question = data.get('original_text')
                all_questions = [question] if question else []
            else:
                all_questions = []

            # 将提取到的问题保存到 txt 文件中
            if all_questions:
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for question in all_questions:
                        output_file.write(question + '\n')
                print(f"成功将 {len(all_questions)} 个问题保存到 {output_file_path}")
            else:
                print("未找到任何 'question' 标签。")

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON 文件。")

def json_to_ques_format(file_path, output_file_path):
    import json

    # 从 1.json 文件中读取非标准 JSON 内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            non_standard_json = f.read()
    except FileNotFoundError:
        print("未找到 json 文件，请检查文件路径。")
    else:
        # 将非标准 JSON 内容转换为标准 JSON 格式
        standard_json_str = '[' + non_standard_json.replace('}\n{', '},{') + ']'

        # 解析 JSON 数据
        try:
            data = json.loads(standard_json_str)
        except json.JSONDecodeError:
            print("JSON 解析出错，请检查 JSON 内容格式。")
        else:
            # 提取所有 original_text 的内容
            original_texts = [item["original_text"] for item in data]

            # 打印提取的内容
            # for text in original_texts:
            #     print(text)
            
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for question in original_texts:
                        output_file.write(question + '\n')
            print(f"成功将 {len(original_texts)} 个问题保存到 {output_file_path}")
        

        
if __name__ == "__main__":
    file_path = 'Data\Math23k\math23k_test.json'
    output_file_path = 'Data\\Math23k\\result_math23k_test.txt'
    json_to_ques_format(file_path, output_file_path)