# Docling 智能文档处理器 WebUI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Gradio](https://img.shields.io/badge/Gradio-3.x-orange)

一个支持多格式文档转换的自动化工具，支持PDF、Word、Excel等格式转Markdown。

## ✨ 功能特性
- 批量处理多文件
- 支持GPU加速（自动检测CUDA）
- 生成详细处理报告
- 结果文件自动保存至`./documents`

## 🚀 快速开始
```bash
# 安装依赖
pip install -r requirements.txt
```
### 启动服务
```bash
python Docling-webui.py
```
## 📂 支持格式
文档：`.pdf, .docx, .pptx, .xlsx`

文本：`.html, .md, .asciidoc`

图片：`.jpg, .png, .jpeg, .gif`

## ⚙️ 硬件要求
最低配置：4GB RAM + CPU

推荐配置：NVIDIA GPU (CUDA 11+)

## 📜 开源协议
MIT License