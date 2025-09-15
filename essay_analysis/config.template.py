# config.template.py
# 重命名此文件为 config.py 并填入你的实际 API 密钥

# DeepSeek API 配置
DEEPSEEK_API_KEY = "your_api_key_here"

# API 模型配置
DEFAULT_MODEL = "deepseek-chat"

# Prompt 配置
SYSTEM_PROMPT = "你是一个专业的文献分析助手，请对提供的文献内容进行总结和关键信息提取。"
USER_PROMPT_TEMPLATE = """请分析以下文献内容，并使用以下模版总结，总结内容内部不要有多余的空行：
XXX单位的XXX等人开展了XXX工作研究，面向XXX的需求，针对XXX的特点，采用了XXX方法，突破了XXX难点，实现了XXX的效果。其中，重点开展了XXX，包括XXX……（不少于350字）\\n\\n{text_content[:4000]}"""

# 其他配置选项
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30  # 秒
MAX_TEXT_LENGTH = 4000  # API 请求的最大文本长度