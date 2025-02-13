import os
import gradio as gr
from docling.document_converter import DocumentConverter
import warnings
import torch
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
from contextlib import closing

# Environment Configuration
os.environ.update({
    'HF_HUB_DISABLE_SYMLINKS_WARNING': '1',
    'KMP_DUPLICATE_LIB_OK': 'TRUE'
})

# Suppress Warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*Blowfish.*")

# Document Directory
DOCUMENTS_DIR = os.path.join(os.getcwd(), 'documents')
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# Device Configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_WORKERS = min(4, os.cpu_count()) if DEVICE == "cuda" else os.cpu_count()

def generate_unique_filename(base_name: str, ext: str) -> str:
    """Generate unique filename"""
    counter = 1
    filename = f"{base_name}.{ext}"
    filepath = os.path.join(DOCUMENTS_DIR, filename)
    while os.path.exists(filepath):
        filename = f"{base_name}_{counter}.{ext}"
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        counter += 1
    return filename

def process_single_file_wrapper(args):
    """Thread-safe file processing wrapper"""
    file, device = args
    try:
        converter = DocumentConverter()  # Removed device parameter
        result = converter.convert(file.name)
        markdown = result.document.export_to_markdown()
        
        base_name = os.path.splitext(os.path.basename(file.name))[0]
        filename = generate_unique_filename(base_name, "md")
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
            
        return {"status": "success", "filename": filename, "original": file.name}
    except Exception as e:
        return {"status": "error", "error": str(e), "original": file.name}

def process_documents(files: List[gr.FileData], progress=gr.Progress()):
    """Optimized document processing"""
    if not files:
        return "Please select at least one file to process"
    
    results = []
    processed = 0
    progress(0, desc="Initializing processing environment")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_file_wrapper, (file, DEVICE)): file for file in files}
        
        progress(0, desc="Starting file processing")
        for future in as_completed(futures):
            processed += 1
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                file = futures[future]
                results.append({"status": "error", "error": str(e), "original": file.name})
            progress(processed / len(files), f"Processed {processed}/{len(files)} files")
    
    success_list = [r for r in results if r["status"] == "success"]
    error_list = [r for r in results if r["status"] == "error"]
    
    report = [
        "📊 Processing Report Summary:",
        f"• Total Files: {len(files)}",
        f"• ✅ Successful Conversions: {len(success_list)}",
        f"• ❌ Failed Conversions: {len(error_list)}",
        "\n📝 Detailed Results:"
    ]
    
    if success_list:
        report.append("\nSuccessfully Converted Files:")
        report.extend([f"  - {res['original']} → {res['filename']}" for res in success_list])
    
    if error_list:
        report.append("\nFailed Files:")
        report.extend([f"  - {res['original']}: {res['error']}" for res in error_list])
    
    return "\n".join(report)

def create_interface():
    """Create optimized interface"""
    with gr.Blocks(title="Docling Document Processor") as demo:
        gr.Markdown(f"""
        ## 📄 Docling Document Processor
        **Supported Formats**: PDF, Word, Excel, PPT, Images  
        **Hardware Acceleration**: {'✅ CUDA Enabled' if DEVICE == 'cuda' else '⛔ CPU Mode'}
        """)
        
        with gr.Row():
            file_input = gr.File(
                label="📁 Batch Upload Files (Multi-select Supported)",
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
                    label="Processing Report",
                    interactive=False,
                    lines=15,
                    max_lines=20,
                    show_copy_button=True
                )
            with gr.Column(scale=1):
                gr.Markdown("""
                **User Guide**:
                1. Click "Choose Files" or drag files
                2. Click Start Processing
                3. View results in the report panel
                4. Outputs saved in `./documents`
                """)
        
        with gr.Row():
            process_btn = gr.Button("🚀 Start Batch Processing", variant="primary")
            clear_btn = gr.Button("🔄 Clear All", variant="secondary")
        
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
    """Find available port"""
    for port in range(start, end+1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    raise OSError(f"No available ports between {start}-{end}")

if __name__ == "__main__":
    port = find_free_port()
    print(f"🌍 Server started: http://localhost:{port}")
    
    try:
        create_interface().queue().launch(
            server_port=port,
            server_name="0.0.0.0",
            share=False,
            show_error=True,
        )
    except Exception as e:
        print(f"⚠️ Port {port} unavailable, trying alternatives...")
        port = find_free_port(7870, 7890)
        create_interface().launch(
            server_port=port,
            server_name="0.0.0.0",
            share=False
        )
    finally:
        print(f"✅ Service closed on port {port}")