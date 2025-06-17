import os
from docx import Document

INPUT_DIR = "interview"
OUTPUT_DIR = "interview_out"

def convert_docx_to_txt(input_path, output_path):
    doc = Document(input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for para in doc.paragraphs:
            if para.text.strip():
                f.write(para.text.strip() + '\n')

def batch_convert():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    docx_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".docx")]
    docx_files.sort()  

    for i, filename in enumerate(docx_files, start=1):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, f"interview_out{i}.txt")
        convert_docx_to_txt(input_path, output_path)
        print(f"✅ Converted '{filename}' → 'interview_out{i}.txt'")

if __name__ == "__main__":
    batch_convert()
