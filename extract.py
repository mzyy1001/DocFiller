import pandas as pd

def extract_todo(input_csv, output_csv, keywords=None):
    if keywords is None:
        keywords = ["待补充", "需要补充", "xx"]
    df = pd.read_csv(input_csv, index_col=0) 
    result = []

    for row_index, (row_label, row) in enumerate(df.iterrows()):
        for col_index, (col_label, value) in enumerate(row.items()):
            if pd.notna(value) and any(kw in str(value) for kw in keywords):
                result.append({
                    "Column Header": col_label,
                    "Row Header": row_label,
                    "Content": value,
                    "Row Index": row_index,
                    "Column Index": col_index+1
                })

    result_df = pd.DataFrame(result)
    result_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✅ Found {len(result)} cells containing '{keywords}', written to '{output_csv}'")

if __name__ == "__main__":
    extract_todo("output.csv", "todo_list.csv")
