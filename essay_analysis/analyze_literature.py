import os
import PyPDF2
import requests
import json
import sys
from pathlib import Path

# 添加当前目录到 Python 路径
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
import config

def extract_text_from_pdf(pdf_path):
    """
    从 PDF 文件中提取所有文本内容。
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"从 '{pdf_path}' 提取文本时发生错误: {e}")
    return text

def call_deepseek_api(text_content, api_key=None, model=None):
    """
    调用 DeepSeek API 对文本内容进行解析。
    """
    api_key = api_key or config.DEEPSEEK_API_KEY
    model = model or config.DEFAULT_MODEL

    if not api_key:
        print("错误: DeepSeek API Key 未提供。请在 config.py 中设置 DEEPSEEK_API_KEY。")
        return None

    url = "https://api.deepseek.com/chat/completions" 
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 您可以根据需要调整这里的 prompt，以指导 DeepSeek API 进行特定类型的解析
    messages = [
        {"role": "system", "content": "你是一个专业的文献分析助手，请对提供的文献内容进行总结和关键信息提取。"},
        {"role": "user", "content": f"请分析以下文献内容，并使用以下模版总结，总结内容内部不要有多余的空行：XXX单位的XXX等人开展了XXX工作研究，面向XXX的需求，针对XXX的特点，采用了XXX方法，突破了XXX难点，实现了XXX的效果。其中，重点开展了XXX，包括XXX……（不少于350字）\\n\\n{text_content[:4000]}"} # 限制文本长度以避免API请求过大
    ]

    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    result = None
    for attempt in range(config.MAX_RETRIES):
        try:
            response = requests.post(
                url, 
                headers=headers, 
                data=json.dumps(payload),
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()  # 如果请求失败，抛出 HTTPError
            result = response.json()
            if result and 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                print(f"DeepSeek API 返回了意外的响应格式: {result}")
                if attempt == config.MAX_RETRIES - 1:
                    return None
                continue
        except (requests.RequestException, json.JSONDecodeError) as e:
            if attempt == config.MAX_RETRIES - 1:  # 最后一次重试
                print(f"API 请求失败 (尝试 {attempt + 1}/{config.MAX_RETRIES}): {str(e)}")
                return None
            print(f"API 请求失败，正在重试 ({attempt + 1}/{config.MAX_RETRIES})...")

def analyze_literature_in_directory(directory_path, api_key, output_filename="all_literature_analysis.txt"):
    """
    遍历指定目录下的 PDF 文献，提取内容并调用 DeepSeek API 进行解析，
    将所有分析结果保存到一个文本文件中。
    """
    if not os.path.isdir(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在。")
        return

    print(f"正在处理目录：{directory_path}")
    all_analysis_results = [] # 用于存储所有文献的分析结果

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            print(f"正在处理文件: {filename}")

            text_content = extract_text_from_pdf(pdf_path)
            if text_content:
                print(f"已从 '{filename}' 提取文本，长度: {len(text_content)} 字符。")
                analysis_result = call_deepseek_api(text_content, api_key)
                if analysis_result:
                    # 将当前文献的分析结果添加到列表中
                    all_analysis_results.append(f"--- 文献名称: {filename} ---\n")
                    all_analysis_results.append(analysis_result)
                    all_analysis_results.append("\n\n") # 在不同文献结果之间添加空行
                    print(f"已获取 '{filename}' 的 DeepSeek API 分析结果。")
                else:
                    print(f"未能获取 '{filename}' 的 DeepSeek API 分析结果。")
            else:
                print(f"未能从 '{filename}' 提取文本，跳过 DeepSeek API 调用。")
        else:
            print(f"跳过文件：'{filename}' (不是 PDF 文件)")

    if all_analysis_results:
        try:
            # 将所有分析结果写入一个文件
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.writelines(all_analysis_results)
            print(f"所有文献的分析结果已保存到 '{output_filename}' 文件中。")
        except IOError as e:
            print(f"保存所有分析结果到 '{output_filename}' 时发生错误: {e}")
    else:
        print("没有找到符合处理模式的 PDF 文件或未能获取任何分析结果。")

    print("所有文献处理完毕。")

if __name__ == "__main__":
    
    literature_directory = input("请输入要处理的文献目录路径：")
    
    # 使用配置文件中的 API 密钥，可以指定输出文件名，这里使用默认值
    analyze_literature_in_directory(literature_directory, config.DEEPSEEK_API_KEY)