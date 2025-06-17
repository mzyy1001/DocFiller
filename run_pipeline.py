import subprocess
import sys
from pathlib import Path

def run_script(script_path):
    print(f"\n➡️ 正在运行 {script_path.name}...\n{'=' * 50}")

    # 启动子进程，实时读取输出
    process = subprocess.Popen(
        [sys.executable, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    try:
        for line in process.stdout:
            print(line, end='')  # 避免双换行
    except Exception as e:
        print(f"❌ 输出捕捉出错: {e}")

    process.wait()
    if process.returncode != 0:
        print(f"❌ {script_path.name} 出错，退出码为 {process.returncode}")
        sys.exit(process.returncode)
    else:
        print(f"\n✅ {script_path.name} 执行成功\n{'-' * 50}")

def main():
    project_root = Path(__file__).parent
    scripts = [
        "doc_to_txt.py",
        "excel_to_csv.py",
        "extract.py",
    ]

    for script in scripts:
        run_script(project_root / script)

    print("\n🎉 所有脚本已成功运行！")

if __name__ == "__main__":
    main()
