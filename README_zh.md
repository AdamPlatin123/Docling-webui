# Docling 智能文档处理器 WebUI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Gradio](https://img.shields.io/badge/Gradio-3.x-orange)

![image](https://github.com/user-attachments/assets/5df7a744-8d6d-4d1a-bbb7-f640023197d3)


一个支持多格式文档转换的自动化工具，支持PDF、Word、Excel等格式转Markdown。

![WebUI-ZH](https://github.com/user-attachments/assets/6192cc64-7916-47d0-8688-6308290efec3)


## ✨ 功能特性
- 批量处理多文件
- 支持GPU加速（自动检测CUDA）
- 生成详细处理报告
- 结果文件自动保存至`./documents`

## 🚀 快速开始

为了更便捷地启动应用，您可以使用项目提供的启动脚本。这些脚本会自动处理虚拟环境创建、依赖安装以及启动应用等步骤。

### 自动化启动脚本

**对于 Linux/macOS 用户:**
1.  首先，确保脚本有执行权限 (如果尚未设置或刚下载脚本):
    ```bash
    chmod +x start.sh
    ```
2.  然后运行脚本:
    ```bash
    ./start.sh
    ```

**对于 Windows 用户:**
1.  直接双击 `start.bat` 文件，或者在命令提示符 (cmd) 中输入以下命令运行:
    ```bash
    start.bat
    ```

这些脚本将会：
*   检查 Python 3 是否已安装。
*   如果 `venv` 虚拟环境尚不存在，则创建它。
*   激活 `venv` 虚拟环境。
*   从 `requirements.txt` 文件中安装或更新所有必要的依赖库。
*   启动 `Docling-webui.py` (英文版UI) 或 `Docling-webui-ZH.py` (中文版UI) 应用。**请注意：** 启动脚本会优先尝试启动 `Docling-webui.py`。如果需要启动中文版，请修改 `start.sh` 或 `start.bat` 中对应的 `python Docling-webui.py` 为 `python Docling-webui-ZH.py`。
*   尝试在您的默认浏览器中打开 `http://localhost:7860`。

**重要提示：** 如果 7860 端口已被占用，应用程序可能会在其他端口启动。请留意脚本运行后控制台的输出信息，以获取实际的访问 URL (例如 `http://localhost:XXXX`)。如果浏览器未能自动打开正确的地址，请手动复制该 URL 到浏览器中访问。

### 手动设置

如果您倾向于手动设置和运行应用程序：

#### 安装依赖
```bash
pip install -r requirements.txt
```
*(请确保在执行此命令前，您已处于 Python 3 环境或已激活相应的虚拟环境。)*

#### 启动服务
```bash
# 启动中文版界面
python Docling-webui-ZH.py

# 或者启动英文版界面
# python Docling-webui.py
```
## 📂 支持格式
文档：`.pdf, .docx, .pptx, .xlsx`

文本：`.html, .md, .asciidoc`

图片：`.jpg, .png, .jpeg, .gif`

## ⚙️ 硬件要求
最低配置：4GB RAM + CPU

推荐配置：NVIDIA GPU (CUDA 11+)

## 参考

If you use Docling in your projects, please consider citing the following:

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

## 📜 开源协议
MIT License
