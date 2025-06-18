import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from middleware.get_col import get_col
from middleware.filter_by_column_index import filter_by_column_index
import random
from tqdm import tqdm


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEESEEK_API_KEY"),
    base_url="https://api.deepseek.com"  
)

def read_interview(row_index):
    txt_path = f"interview_out/interview_out{row_index+1}.txt"
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_row_context(df, row_index, exclude_col_index):
    row = df[df["Row Index"] == row_index]
    examples = []
    for _, r in row.iterrows():
        if r["Column Index"] != exclude_col_index:
            examples.append(f"{r['Column Header']}：{r['Content']}")
    return "\n".join(examples)

def split_text_by_line(full_text, max_chars=3000):
    """
    将文本按行切分，确保每一段不超过 max_chars，并在完整行结束处截断。
    """
    lines = full_text.splitlines()
    chunks = []
    current_chunk = ""
    
    for line in lines:
        # 预估加上当前行后是否超限
        if len(current_chunk) + len(line) + 1 <= max_chars:
            current_chunk += line + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.rstrip())
            current_chunk = line + "\n"
    
    if current_chunk:
        chunks.append(current_chunk.rstrip())
    
    return chunks



def build_prompt(question, original, full_text):
    return f"""以下是一次采访的原始文本内容（完整）：
----------
{full_text}
----------

现在有问题是：{question}

在给出回答的时候我还需要对应的原文，原文可以截取的更长一些，如果找不到对应的原文，被视为无法补充。

如果{original}中已经出现过的内容不需要再提及,注意尽量不要和original 有任何的重复。

有时候人的说话会不完整，或者有些内容没有说清楚，这时候你需要根据上下文和语境，去思考背后的含义。

请你判断是否可以根据已有上下文和语境补充该问题的回答？如果可以，请直接补上合理回答内容；

如果能回答部分内容，声明能补充哪些部分，然后只回答这些能补充的部分，而不需要告诉我哪些不能回答。

所有能提到的回答，必须要有对应的原文支持，原文必须是完整的一句话。

可以使用以下的格式回答：
问题：
回答：
原文证据：

如果不能回答补充任意一个问题，即使是一部分，请仅回复“我无法补充任何内容”，而不带有任何的解释。
"""

def ask_deepseek(prompt):
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个汇总机器，负责汇总所有的回答内容。可以省略部分繁琐的证据和理由。"},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content

def get_question(question_header, original, row_context):
    """
    用 AI 将模糊的 question_header + row_context 归纳出一个明确的问题。
    """
    prompt = f"""
我们正在整理一份调研结果，其中行的标题是："{question_header}"，
我当前已经有一个不完整的回答内容是："{original}"。其中缺乏的内容的地方标记了“待补充” 或者 “需要补充”
如果“待补充”前后已经明确声明了哪些内容需要补充，请包含在回答中。（比如缺少...需要补充），那么缺少的东西是必须要被提问的。

下面是其他受访者对这一列内容的完整回答内容：
----------
{row_context}
----------

你需要学习其他受访者的回答内容，理解我这一个不完整的回答内容缺少了什么内容。

请根据这些内容，总结出不完整的回答内容缺少什么内容，用问题来描述，可以是一个问题或者多个问题.
问题尽量不要过于具体，而给更多回答的空间，但是要保证前后文的关联性。
问题会被作为prompt 进一步传递给 DeepSeek 进行回答下一个问题。
不要带为什么是这个问题的理由，只包含问题本身就好了。
"""

    # 向 DeepSeek 发送请求
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个帮助提炼具体调查问题的助手。"},
            {"role": "user", "content": prompt}
        ]
    )
    
    question = res.choices[0].message.content.strip()
    return question


def ask_deepseek_multi(full_text,question_header, original, row_context, log_file):
    """
    对分段后的文本逐段提问，记录每段的响应。
    收集所有非“无法补充”的回答，最终合并返回。
    """
    chunks = split_text_by_line(full_text)
    valid_answers = []
    question = get_question(question_header, original, row_context)
    with open(log_file, "w", encoding="utf-8") as log:
        log.write(f"🔍 问题：{question}\n")
        for i, chunk in enumerate(tqdm(chunks, desc="🔍 正在生成报告")):

            
            prompt = build_prompt(question, original, chunk)
            result = ask_deepseek(prompt)

            log.write(f"🤖 AI Response {i+1}:\n{result}\n")
            log.write(f"{'-'*80}\n\n")

            simplified = result.strip().replace("。", "").replace(" ", "")
            valid = simplified != "我无法补充任何内容"
            if valid:
                valid_answers.append(f"(From Part {i+1})\n{result.strip()}")
            tqdm.write(f"✅ Chunk {i+1} processed, valid answer: {valid}")

    # 如果没有有效回答，返回默认消息
    if valid_answers:
        return "\n\n".join(valid_answers)
    else:
        return "我无法补充任何内容"


def main():

    
    
    df = pd.read_csv("todo_list.csv")
    full_output = []
    preview_output = []
    for i in range(1, 100):
        
        txt_path = f"interview_out/interview_out{i}.txt"
        if not os.path.exists(txt_path):
            continue
        print(f"Processing {i}th interview...")
        # col_idx = get_col(txt_path, "output.csv")
        col_idx = get_col(txt_path, "output.csv")
        print(f"Predicted Column Index: {col_idx}")
        relevant_rows = filter_by_column_index("todo_list.csv", col_idx)
        #print(relevant_rows)
        for _, row in relevant_rows.iterrows():
            print(f"Processing row: {row['Row Index']}, column: {col_idx}'s content...")
            row_idx = int(row["Row Index"])
            folder = f"result/row{row_idx}_col{col_idx}"
            os.makedirs(folder, exist_ok=True)  
            column_header = row["Column Header"]
            question_header = row["Row Header"]
            original = row["Content"]

            full_text = read_interview(i - 1)
            this_row = df[df["Row Index"] == row_idx]
            other_columns = this_row[this_row["Column Index"] != col_idx]
            sampled = other_columns.sample(n=min(3, len(other_columns)), random_state=42)
            row_context = ""
            for _, r in sampled.iterrows():
                row_context += f"{r['Column Header']}：{r['Content']}\n"
            chunk_log_path = os.path.join(folder, "chunk_log.txt")
            build_prompt_text = ask_deepseek_multi(full_text, question_header, original, row_context, chunk_log_path)
            res = ask_deepseek(build_prompt_text)
            preview_output.append({
                "interview_file": txt_path,
                "Predicted Column Index": col_idx,
                "Row Index": row_idx,
                "Column Header": column_header,
                "Question Header": question_header,
                "Original Content": original,
                "Row Context": row_context,
                "AI Completion": res
            })
            
            with open(os.path.join(folder, "completion.txt"), "w", encoding="utf-8") as f:
                for item in preview_output:
                    f.write(f"🧾 Header: {item['Column Header']}\n")
                    f.write(f"❓ Question Header: {item['Question Header']}\n")
                    f.write(f"🤖 AI Completion:\n{item['AI Completion']}\n")
                    f.write("-" * 60 + "\n\n")         
            preview_output.clear()  
        
                    

if __name__ == "__main__":
    main()
