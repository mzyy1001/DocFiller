# 电脑小白都会的使用教程

采访 Word 文档配合一个 Excel 表格，自动生成结构化输出。你只需准备好采访文件和 Excel 报表，剩下的交给脚本完成。
把.env 文件放在根目录下再开始运行。
跑得可能会很慢，可以开始跑了之后等一会。
目前还非常不完善，只有参考价值。但是可以省力。

# 📝 DocFiller 使用说明（macOS 新手完全指南）



---

## 📦 第一步：打开终端（Terminal）

1. 在桌面上按下 `Command + 空格` 打开 **Spotlight 搜索**  
2. 输入 `Terminal`，然后点击出现的“终端”图标（黑底白字）

---

## 🔧 第二步：安装 Git（仅第一次需要）

Git 是用来下载和同步项目代码的工具。

```bash
xcode-select --install
```

根据弹出的提示进行安装（如提示“已安装”则跳过）

---

## ⬇️ 第三步：克隆（下载）项目

```bash
git clone https://github.com/mzyy1001/DocFiller.git
cd DocFiller
```

---

## 🐍 第四步：安装 Python（如果尚未安装）

macOS 自带 Python，但推荐安装最新版 Python（>=3.9）

1. 打开浏览器访问：https://www.python.org/downloads/macos/
2. 下载并安装最新版 Python（`.pkg` 安装包）
3. 安装完成后在终端验证：

```bash
python3 --version
```

---

## 🧪 第五步：创建并启用虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

启用后终端前会出现 `(venv)`。

---

## 📦 第六步：安装依赖库

```bash
pip install -r requirements.txt
```

---

## 📁 第七步：准备文件

| 类型 | 说明 | 放置位置 |
|------|------|----------|
| 采访 Word 文件 | `.docx` 原稿 | `notes/` |
| 汇总 Excel 文件 | 单个 `.xlsx` | `notes/`（确保只有 1 个） |

---

## ▶️ 第八步：运行自动化脚本

等第一个跑完再输入第二个命令

```bash
python run_pipeline.py
python main.py
```

脚本自动执行：

1. Word → txt  
2. Excel → csv  
3. 提取信息  
4. 生成结果  

---


---

## ❓常见问题

**`command not found: python3`**  
→ 参考“第四步”安装 Python

**`No module named pandas`**  
→ 确认已 `pip install -r requirements.txt`

---

## ✅ 完成！

运行成功后即可在上述目录查看结果。

然后你可以在result 中找到每一个格子对应的补充内容，其中completion 是内容，而具体的证据和ai 回复 可以在对应文件夹 chunk_log 中找到。
