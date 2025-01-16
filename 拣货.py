import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import re

# 创建主窗口
root = tk.Tk()
root.title("文件查找与复制工具")
root.geometry("500x530")
root.attributes("-topmost", True)  # 设置窗口置顶

# 设置默认路径
DEFAULT_SEARCH_DIR = r"C:\Users\E5-3\Desktop\原图"  # 替换为实际路径
DEFAULT_OUTPUT_DIR = r"C:\Users\E5-3\Desktop\图"  # 替换为实际路径

# 初始化全局变量
search_dir = DEFAULT_SEARCH_DIR
output_dir = DEFAULT_OUTPUT_DIR

# 移除文件名中的非法字符
def sanitize_filename(file_name):
    illegal_chars = r'[/:*?"<>|]'
    return re.sub(illegal_chars, "", file_name)

# 去除中文字符
def remove_chinese(text):
    return re.sub(r'[\u4e00-\u9fa5]', '', text)

# 获取图像宽度
def get_image_width(file_path):
    try:
        with Image.open(file_path) as img:
            return img.width
    except Exception as e:
        return 0

# 选择源文件夹
def select_search_folder():
    global search_dir
    search_dir = filedialog.askdirectory()
    if search_dir:
        search_folder_label.config(text=f"选择的源文件夹：{search_dir}")
    else:
        search_dir = DEFAULT_SEARCH_DIR
        search_folder_label.config(text=f"使用默认源文件夹：{search_dir}")

# 选择输出文件夹
def select_output_folder():
    global output_dir
    output_dir = filedialog.askdirectory()
    if output_dir:
        output_folder_label.config(text=f"选择的输出文件夹：{output_dir}")
    else:
        output_dir = DEFAULT_OUTPUT_DIR
        output_folder_label.config(text=f"使用默认复制文件夹：{output_dir}")

# 查找并复制文件
def find_and_copy_file(event=None):
    global search_dir, output_dir

    file_name = file_name_entry.get().strip().replace(" ", "").replace("\n", "")
    prefix = prefix_entry.get().strip()

    feedback_label.config(text="")  # 清空之前的反馈信息

    if not os.path.exists(search_dir):
        feedback_label.config(text=f"错误：源文件夹路径不存在。", fg="red")
        return

    if not os.path.exists(output_dir):
        feedback_label.config(text=f"错误：输出文件夹路径不存在。", fg="red")
        return

    if not file_name:
        feedback_label.config(text="错误：请输入文件名。", fg="red")
        return

    if not prefix:
        feedback_label.config(text="错误：请输入文件前缀。", fg="red")
        return

    found_files = []
    for root_dir, _, files in os.walk(search_dir):
        for file in files:
            file_no_spaces = os.path.splitext(file)[0].replace(" ", "").lower()
            sanitized_file_name = remove_chinese(file_no_spaces)
            if sanitized_file_name == remove_chinese(file_name.lower()):
                found_files.append(os.path.join(root_dir, file))

    if found_files:
        if "桌旗" in prefix:
            target_file_path = max(found_files, key=get_image_width)
        elif "餐垫" in prefix:
            target_file_path = min(found_files, key=get_image_width)
        else:
            target_file_path = found_files[0]

        file_extension = os.path.splitext(target_file_path)[1]
        file_name_without_spaces = os.path.splitext(os.path.basename(target_file_path))[0].replace(" ", "")
        safe_file_name = sanitize_filename(file_name_without_spaces)
        new_name = f"{prefix}_{safe_file_name}{file_extension}"
        new_path = os.path.join(output_dir, new_name)

        try:
            shutil.copy(target_file_path, new_path)
            feedback_label.config(text=f"成功：文件已复制到 {new_path}", fg="green")
        except Exception as e:
            feedback_label.config(text=f"错误：文件复制失败: {e}", fg="red")
    else:
        feedback_label.config(text=f"提示：未找到名为 {file_name} 的文件。", fg="orange")

# 创建GUI元素
search_folder_label = tk.Label(root, text=f"默认源文件夹：{search_dir}")
search_folder_label.pack(pady=10)

select_search_button = tk.Button(root, text="选择源文件夹", command=select_search_folder)
select_search_button.pack(pady=5)

output_folder_label = tk.Label(root, text=f"默认输出文件夹：{output_dir}")
output_folder_label.pack(pady=10)

select_output_button = tk.Button(root, text="选择输出文件夹", command=select_output_folder)
select_output_button.pack(pady=5)

file_name_label = tk.Label(root, text="输入文件名：")
file_name_label.pack(pady=5)

file_name_entry = tk.Entry(root, width=50)
file_name_entry.pack(pady=5)

prefix_label = tk.Label(root, text="输入文件前缀：")
prefix_label.pack(pady=5)

prefix_entry = tk.Entry(root, width=50)
prefix_entry.pack(pady=5)

search_button = tk.Button(root, text="查找并复制文件", command=find_and_copy_file)
search_button.pack(pady=20)

feedback_label = tk.Label(root, text="", wraplength=450)
feedback_label.pack(pady=20)

# 绑定回车键
root.bind("<Return>", find_and_copy_file)

# 运行主循环
root.mainloop()
