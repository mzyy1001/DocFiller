# convert_excel_to_csv.py
import pandas as pd
import os

def find_single_xlsx(directory):
    xlsx_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]
    if len(xlsx_files) != 1:
        raise ValueError(f"Expected exactly 1 xlsx file in {directory}, found {len(xlsx_files)}.")
    return os.path.join(directory, xlsx_files[0])

def convert_excel_to_csv(input_path, output_path, sheet_name=0):
    df = pd.read_excel(input_path, sheet_name=sheet_name)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    notes_dir = "notes"
    input_file = find_single_xlsx(notes_dir)
    output_file = "output.csv"
    convert_excel_to_csv(input_file, output_file)
    print(f"✅ Converted '{input_file}' to '{output_file}'")
