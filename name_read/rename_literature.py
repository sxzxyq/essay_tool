import os
import re

def rename_literature_files(directory_path, output_filename="processed_literature_names.txt"):
    """
    提取指定目录下所有文献的名字，并将每个文献名字开头的序号
    如“1.”，“2.”等转换为“[1].”、“[2].”等，然后将处理后的名字保存到文本文件中。
    """
    if not os.path.isdir(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在。")
        return

    print(f"正在处理目录：{directory_path}")
    processed_names_with_numbers = [] # 存储 (number, new_filename)
    skipped_count = 0

    for filename in os.listdir(directory_path):
        # 匹配以数字和点开头的模式，例如 "1.文献名称.pdf"
        match = re.match(r"^(\d+)\.(.*)", filename)
        if match:
            number_str = match.group(1)
            rest_of_name = match.group(2)
            new_filename = f"[{number_str}].{rest_of_name}"
            try:
                number_int = int(number_str)
                processed_names_with_numbers.append((number_int, new_filename))
                print(f"已处理：'{filename}' -> '{new_filename}'")
            except ValueError:
                print(f"跳过文件：'{filename}' (序号 '{number_str}' 无法转换为整数)")
                skipped_count += 1
        else:
            print(f"跳过文件：'{filename}' (不符合处理模式)")
            skipped_count += 1

    if processed_names_with_numbers:
        # 按照提取的数字进行排序
        processed_names_with_numbers.sort(key=lambda x: x[0])
        
        # 提取排序后的文件名
        sorted_processed_names = [name for _, name in processed_names_with_numbers]

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                # 写入标题
                f.write("处理后的文献名称列表：\n")
                f.write("=" * 50 + "\n\n")
                # 写入文件名，每个都单独成行
                for name in sorted_processed_names:
                    f.write(f"{name}\n")
                    # f.write(name + '\n')
                # 写入统计信息
                f.write("\n" + "=" * 50 + "\n")
                f.write(f"总计处理文件数：{len(sorted_processed_names)}\n")
            print(f"所有处理后的文件名已保存到 '{output_filename}' 文件中，并已按序号排序。")
        except IOError as e:
            print(f"写入文件 '{output_filename}' 时发生错误：{e}")
    else:
        print("没有找到符合处理模式的文件。")

    print(f"处理完成。共处理了 {len(processed_names_with_numbers)} 个文件，跳过了 {skipped_count} 个文件。")

if __name__ == "__main__":
    # 获取用户输入的目录路径
    target_directory = input("请输入要处理的文献目录路径：")
    rename_literature_files(target_directory)