
# Docling Document Processor WebUI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Gradio](https://img.shields.io/badge/Gradio-3.x-orange)

An automated tool for converting documents (PDF, Word, Excel, etc.) to Markdown.

![webui-en](https://github.com/user-attachments/assets/aa7196cf-96e5-428d-8fc5-b0c029c9c9fe)

## ✨ Features
- Batch file processing
- GPU acceleration (auto-detects CUDA)
- Detailed processing reports
- Outputs saved to `./documents`

## 🚀 Quick Start

### Install dependencies
```bash
pip install -r requirements.txt
```
### Launch service
```bash
python Docling-webui.py
```
## 📂 Supported Formats
Documents: `.pdf, .docx, .pptx, .xlsx`

Text: `.html, .md, .asciidoc`

Images: `.jpg, .png, .jpeg, .gif`

## ⚙️ Hardware Requirements
Minimum: 4GB RAM + CPU

Recommended: NVIDIA GPU (CUDA 11+)

## 📜 License
MIT License
