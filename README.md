# Essay Analysis Tool

这是一个用于文献分析的Python工具集，主要包含两个主要功能模块：

## 功能特点

### 1. 文献分析 (essay_analysis)
- 提供全面的文献分析功能
- 生成详细的分析报告
- 支持批量处理多篇文献

### 2. 文献名称处理 (name_read)
- 处理文献名称
- 自动重命名文献文件
- 标准化文献命名格式

## 安装说明

1. 克隆仓库到本地：
```bash
git clone https://github.com/your-username/essay_tool.git
cd essay_tool
```

2. 安装所需依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 文献分析
```python
python essay_analysis/analyze_literature.py
```

### 文献名称处理
```python
python name_read/rename_literature.py
```

## 项目结构
```
essay_analysis/
    all_literature_analysis.txt   # 文献分析结果
    analyze_literature.py         # 分析脚本

name_read/
    processed_literature_names.txt # 处理后的文献名称
    rename_literature.py          # 重命名脚本
```

## 贡献指南

欢迎提交问题和功能建议！如果你想贡献代码：

1. Fork 本仓库
2. 创建你的特性分支
3. 提交你的改动
4. 推送到你的分支
5. 创建一个新的 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件