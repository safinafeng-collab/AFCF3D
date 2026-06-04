import os
import re
import sys

def rename_files(directory, start_old=0, end_old=3999, start_new=16000):
    """
    重命名指定目录中的PNG文件。
    """
    # 获取目录中的所有PNG文件，按照文件名排序
    try:
        files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
    except FileNotFoundError:
        print(f"目录不存在：{directory}")
        sys.exit(1)
    
    # 使用正则表达式提取数字部分并排序
    def extract_number(filename):
        match = re.match(r'(\d{5})\.png$', filename)
        if match:
            return int(match.group(1))
        else:
            return -1  # 非匹配文件排在前面
    
    files_sorted = sorted(files, key=extract_number)
    
    # 过滤出需要重命名的文件
    files_to_rename = []
    for f in files_sorted:
        number = extract_number(f)
        if start_old <= number <= end_old:
            files_to_rename.append(f)
    
    print(f"找到 {len(files_to_rename)} 个文件需要重命名。")
    
    if not files_to_rename:
        print("没有符合条件的文件需要重命名。")
        return
    
    # 确保没有目标文件已经存在，以避免覆盖
    for i, f in enumerate(files_to_rename):
        new_number = start_new + i
        new_filename = f"{new_number:05d}.png"
        new_filepath = os.path.join(directory, new_filename)
        if os.path.exists(new_filepath):
            print(f"目标文件已存在：{new_filename}。请确保不会覆盖重要文件。")
            sys.exit(1)
    
    # 临时重命名前，打印重命名计划
    print("重命名计划：")
    for i, f in enumerate(files_to_rename):
        old_number = extract_number(f)
        new_number = start_new + i
        old_name = f"{old_number:05d}.png"
        new_name = f"{new_number:05d}.png"
        print(f"{old_name} -> {new_name}")
    
    # 确认是否继续
    confirm = input("确认开始重命名吗？(y/n): ")
    if confirm.lower() != 'y':
        print("重命名操作已取消。")
        return
    
    # 临时重命名，避免冲突
    temp_suffix = "_temp_rename"
    temp_files = []
    for f in files_to_rename:
        old_path = os.path.join(directory, f)
        temp_name = f.replace('.png', temp_suffix + '.png')
        temp_path = os.path.join(directory, temp_name)
        os.rename(old_path, temp_path)
        temp_files.append(temp_name)
        print(f"临时重命名 {f} -> {temp_name}")
    
    # 最终重命名
    for i, f in enumerate(temp_files):
        temp_path = os.path.join(directory, f)
        new_number = start_new + i
        new_filename = f"{new_number:05d}.png"
        new_path = os.path.join(directory, new_filename)
        os.rename(temp_path, new_path)
        print(f"最终重命名 {f} -> {new_filename}")
    
    print("所有文件重命名完成。")

if __name__ == "__main__":
    # 指定目标目录
    target_directory = r"C:\遥感\test\test\label"
    
    # 调用重命名函数
    rename_files(target_directory)
