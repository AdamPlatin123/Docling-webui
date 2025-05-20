# Docling Document Processor WebUI

![image](https://github.com/user-attachments/assets/790d82a1-48bc-417b-9a23-2098d1454291)


![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Gradio](https://img.shields.io/badge/Gradio-3.x-orange)

[简体中文](https://github.com/AdamPlatin123/Docling-webui/blob/main/README_zh.md)

An automated tool for converting documents (PDF, Word, Excel, etc.) to Markdown.

![webui-en](https://github.com/user-attachments/assets/aa7196cf-96e5-428d-8fc5-b0c029c9c9fe)

## ✨ Features
- Batch file processing
- GPU acceleration (auto-detects CUDA)
- Detailed processing reports
- Outputs saved to `./documents`

## 🚀 Quick Start

For a more automated setup, you can use the provided startup scripts. These scripts handle virtual environment creation, dependency installation, and application launch.

### Automated Startup Scripts

**For Linux/macOS users:**
1.  Make the script executable (if you haven't already done so, or if you downloaded it):
    ```bash
    chmod +x start.sh
    ```
2.  Run the script:
    ```bash
    ./start.sh
    ```

**For Windows users:**
1.  Simply run the script by double-clicking `start.bat` or typing the following in your command prompt:
    ```bash
    start.bat
    ```

These scripts will:
*   Check for Python 3.
*   Create a Python virtual environment named `venv` if it doesn't already exist.
*   Activate the virtual environment.
*   Install (or update) all necessary dependencies from `requirements.txt`.
*   Launch the `Docling-webui.py` application.
*   Attempt to open your default web browser to `http://localhost:7860`.

**Note:** The application might sometimes start on a different port if 7860 is occupied. Please check the console output from the script for the exact URL (e.g., `http://localhost:XXXX`) and open it manually if the browser doesn't point to the correct address.

### Manual Setup

If you prefer to set up and run the application manually:

#### Install dependencies
```bash
pip install -r requirements.txt
```
*(Ensure you are in a Python 3 environment or virtual environment before running this.)*

#### Launch service
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

## References


```bib
@techreport{Docling,
  author = {Deep Search Team},
  month = {8},
  title = {Docling Technical Report},
  url = {https://arxiv.org/abs/2408.09869},
  eprint = {2408.09869},
  doi = {10.48550/arXiv.2408.09869},
  version = {1.0.0},
  year = {2024}
}
```

## 📜 License
MIT License
