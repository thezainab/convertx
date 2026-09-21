import os
from docx import Document
from app.services.conversion_registry import registry
import subprocess

def docx_to_txt(input_path: str, output_path: str) -> bool:
    try:
        doc = Document(input_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Word to TXT error: {e}")
        return False

def docx_to_pdf(input_path: str, output_path: str) -> bool:
    try:
        in_path = os.path.abspath(input_path)
        out_path = os.path.abspath(output_path)
        
        # Cloud/Linux friendly PDF conversion using LibreOffice
        # This will work on Render (Linux) and locally if LibreOffice is installed
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(out_path), in_path], check=True)
        return True
    except Exception as e:
        print(f"Word to PDF error: {e}")
        # Note: Render par Word to PDF function ko mukkamal chalane ke liye LibreOffice ki zaroorat hoti hai.
        # Filhal app ko crash se bachane ke liye yeh safe tareeqa lagaya gaya hai.
        return False

# Dono features register ho gaye
registry.register('docx', 'txt', docx_to_txt)
registry.register('doc', 'txt', docx_to_txt)
registry.register('docx', 'pdf', docx_to_pdf)