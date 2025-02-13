import os
import gradio as gr
from docling.document_converter import DocumentConverter
import warnings
import torch
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
from contextlib import closing

# 环境配置
os.environ.update({
    'HF_HUB_DISABLE_SYMLINKS_WARNING': '1',
    'KMP_DUPLICATE_LIB_OK': 'TRUE'
})

# 禁用警告
warnings.filterwarnings("ignore", category=UserWarning, message=".*Blowfish.*")

# 文档保存目录
DOCUMENTS_DIR = os.path.join(os.getcwd(), 'documents')
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# 设备配置
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_WORKERS = min(4, os.cpu_count()) if DEVICE == "cuda" else os.cpu_count()

def generate_unique_filename(base_name: str, ext: str) -> str:
    """生成唯一文件名"""
    counter = 1
    filename = f"{base_name}.{ext}"
    filepath = os.path.join(DOCUMENTS_DIR, filename)
    while os.path.exists(filepath):
        filename = f"{base_name}_{counter}.{ext}"
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        counter += 1
    return filename

def process_single_file_wrapper(args):
    """线程安全的文件处理包装器"""
    file, device = args
    try:
        # 每个线程独立创建转换器
        converter = DocumentConverter()  # 移除 device 参数
        result = converter.convert(file.name)
        markdown = result.document.export_to_markdown()
        
        base_name = os.path.splitext(os.path.basename(file.name))[0]
        filename = generate_unique_filename(base_name, "md")
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
            
        return {"status": "success", "filename": filename, "original": file.name}  # 使用 file.name
    except Exception as e:
        return {"status": "error", "error": str(e), "original": file.name}  # 使用 file.name

def process_documents(files: List[gr.FileData], progress=gr.Progress()):
    """优化的文档处理流程"""
    if not files:
        return "请选择至少一个文件进行处理"
    
    results = []
    processed = 0
    progress(0, desc="初始化处理环境")
    
    # 使用上下文管理器确保线程池正确释放
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 为每个文件分配设备参数
        futures = {executor.submit(process_single_file_wrapper, (file, DEVICE)): file for file in files}
        
        progress(0, desc="开始处理文件")
        for future in as_completed(futures):
            processed += 1
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                file = futures[future]
                results.append({"status": "error", "error": str(e), "original": file.name})  # 使用 file.name
            progress(processed / len(files), f"已处理 {processed}/{len(files)} 个文件")
    
    # 生成处理报告
    success_list = [r for r in results if r["status"] == "success"]
    error_list = [r for r in results if r["status"] == "error"]
    
    report = [
        "📊 处理报告总结：",
        f"• 总计文件: {len(files)}",
        f"• ✅ 成功转换: {len(success_list)}",
        f"• ❌ 转换失败: {len(error_list)}",
        "\n📝 详细结果："
    ]
    
    if success_list:
        report.append("\n成功转换文件：")
        report.extend([f"  - {res['original']} → {res['filename']}" for res in success_list])
    
    if error_list:
        report.append("\n失败文件列表：")
        report.extend([f"  - {res['original']}：{res['error']}" for res in error_list])
    
    return "\n".join(report)

def create_interface():
    """创建优化后的界面"""
    with gr.Blocks(title="Docling 智能文档处理器") as demo:
        gr.Markdown("""
        ## 📄 Docling 智能文档处理器
        **支持格式**：PDF、Word、Excel、PPT、图片等  
        **硬件加速**：{'✅ CUDA加速' if DEVICE == 'cuda' else '⛔ CPU模式'}
        """)
        
        with gr.Row():
            file_input = gr.File(
                label="📁 批量上传文件（支持多选）",
                file_count="multiple",
                file_types=[
                    '.pdf', '.docx', '.pptx', '.xlsx', 
                    '.html', '.md', '.asciidoc', 
                    '.jpg', '.png', '.jpeg', '.gif'
                ],
                height=200
            )
            
        with gr.Row():
            with gr.Column(scale=3):
                output = gr.Textbox(
                    label="处理报告",
                    interactive=False,
                    lines=15,
                    max_lines=20,
                    show_copy_button=True
                )
            with gr.Column(scale=1):
                gr.Markdown("""
                **操作指南**：
                1. 点击"选择文件"或拖放文件到上传区
                2. 点击开始处理按钮
                3. 查看右侧处理报告
                4. 结果文件保存在程序目录/documents
                """)
        
        with gr.Row():
            process_btn = gr.Button("🚀 开始批量处理", variant="primary")
            clear_btn = gr.Button("🔄 清除所有", variant="secondary")
        
        process_btn.click(
            process_documents,
            inputs=[file_input],
            outputs=output,
            concurrency_limit=MAX_WORKERS
        )
        
        clear_btn.click(
            lambda: ["", None],
            outputs=[output, file_input]
        )
    
    return demo

def find_free_port(start=7860, end=8000):
    """寻找可用端口优化版"""
    for port in range(start, end+1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    raise OSError(f"No available ports between {start}-{end}")

if __name__ == "__main__":
    port = find_free_port()
    print(f"🌍 启动服务: http://localhost:{port}")
    
    try:
        create_interface().queue().launch(
            server_port=port,
            server_name="0.0.0.0",
            share=False,
            show_error=True,
        )
    except Exception as e:
        print(f"⚠️ 端口 {port} 不可用，尝试备用端口...")
        port = find_free_port(7870, 7890)
        create_interface().launch(
            server_port=port,
            server_name="0.0.0.0",
            share=False
        )
    finally:
        print(f"✅ 服务已运行在端口 {port}")