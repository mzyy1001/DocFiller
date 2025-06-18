import pandas as pd
import os
from openai import OpenAI
import re

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

client = OpenAI(
    api_key=os.getenv("DEESEEK_API_KEY"),
    base_url="https://api.deepseek.com"  
)

def read_output_preview(path, char_limit=500):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content[:char_limit]

def get_column_samples(csv_path, row_limit=2):
    df = pd.read_csv(csv_path)
    sample_data = {}
    for col in df.columns:
        samples = df[col].astype(str).head(row_limit).tolist()
        sample_data[col] = samples
    return sample_data

def build_prompt(output_preview, column_samples):
    prompt = f"""你是一个文本分类助手。
我将给你一个内容片段和若干列的列头与样本数据。

你的任务是：判断内容最可能属于哪一列，对应的表头，以及对应的被采访人的名字。

内容片段如下：
\"{output_preview}\"

下面是所有列（格式：索引 - 列名 - 样本）：
"""
    for idx, (col, samples) in enumerate(column_samples.items()):
        prompt += f"{idx} - {col} - {' / '.join(samples)}\n"
    prompt += "\n请返回对应的列头，不需要其他内容。只返回列名，不要返回其他的解释。"
    return prompt

def ask_deepseek(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个文本列分类机器人"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    content = response.choices[0].message.content
    match = re.search(r"\d+", content)
    if match:
        return int(match.group())
    else:
        raise ValueError(f"无法解析 DeepSeek 返回内容: {content}")

def get_column_count(csv_path):
    df = pd.read_csv(csv_path)
    return len(df.columns)

def get_col(output_path, csv_path):
    preview = read_output_preview(output_path)
    samples = get_column_samples(csv_path)
    prompt = build_prompt(preview, samples)

    result = ask_deepseek(prompt)
    return result

if __name__ == "__main__":
    output_path = "interview_out/interview_out3.txt"
    csv_path = "output.csv"

    preview = read_output_preview(output_path)
    samples = get_column_samples(csv_path)
    prompt = build_prompt(preview, samples)

    print("🧠 正在向 DeepSeek 提问，请稍候...\n")
    result = ask_deepseek(prompt)

    print(f"✅ DeepSeek 的预测列索引是：{result}")
    print(f"📊 当前 CSV 文件总共有 {get_column_count(csv_path)} 列")