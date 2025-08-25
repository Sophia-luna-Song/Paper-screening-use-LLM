import http.client
import json
import pandas as pd
import re
import traceback


def get_response_from_api(title, abstract):
    conn = http.client.HTTPSConnection("api.chatanywhere.tech")
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Based on the title of paper:’{title}‘, According to the topic understanding, judge classification."
                           f"Analyze each research title and determine if the study investigates animals."
                           f"If the title indicates a focus on this interaction, label it as '1.' If not, label it as '0.'"
                           f"Reply in the following format: Label is n !!"
            }
        ]
    })
    headers = {
        'Authorization': 'Bearer sk-qPQtTU47NOASDBYmjpu6nPMad959c6ZbR53OkufCAfFjw7yJ',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def extract_label(response_content):
    # 寻找“标签是”后的数字
    match = re.search(r'Label is (\d+)', response_content)
    if match:
        print(match.group(1))
        return match.group(1)  # 返回匹配到的标签值
    return None  # 如果没有找到标签，返回 None


# 读取 Excel 表格中的 "Title" 列
excel_file_path = 'E:\Web_of_science\手筛\single-cla\只有题目处理\\二次机筛表型.xlsx'  # 替换为你的 Excel 文件路径
df = pd.read_excel(excel_file_path)


# 创建一个空列表用于存储结果
results = []


# 定义保存结果的函数
def save_results():
    results_df = pd.DataFrame(results)
    results_df.to_excel('E:\Web_of_science\手筛\single-cla\只有题目处理\\去掉动物研究-后半部分.xlsx', index=False, encoding='utf-8-sig')
    print("Progress saved to '二次机筛表型.xlsx'")


# 遍历 "Title" 列中的每个标题
for index, row in df.iterrows():
    title = row["Title"]
    abstract = row["Abstract"]

    try:
        response = get_response_from_api(title, abstract)

        # 调试输出，查看响应内容
        print("Response:", response)  # 打印响应内容

        # 直接处理字符串响应
        label_value = extract_label(response)

        results.append({
            "Title": title,
            "Label": label_value
        })
        print(f"Response for title '{title}': {response}")

    except Exception as e:
        # 如果发生异常，打印错误信息并保存当前结果
        print(f"Error processing title '{title}': {e}")
        print(traceback.format_exc())
        save_results()
        break  # 中断循环

# 最后一次保存结果
save_results()
print("Classification results saved to 'seed-1 - 2.xlsx'")