import pandas as pd

def filter_by_column_index(input_csv, target_index):
    df = pd.read_csv(input_csv)
    
    df['Column Index'] = pd.to_numeric(df['Column Index'], errors='coerce')

    filtered = df[df['Column Index'] == target_index]

    return filtered

if __name__ == "__main__":
    n = 10  
    todo_path = "todo_list.csv"
    
    result_df = filter_by_column_index(todo_path, n)
    print(f"✅ Rows where Column Index == {n}:")
    print(result_df)
