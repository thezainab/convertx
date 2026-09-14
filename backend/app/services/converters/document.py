import os
from docx import Document
from docx2pdf import convert as docx_convert
from app.services.conversion_registry import registry

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
        docx_convert(in_path, out_path)
        return True
    except Exception as e:
        print(f"Word to PDF error: {e}")
        return False

# Dono features register ho gaye
registry.register('docx', 'txt', docx_to_txt)
registry.register('doc', 'txt', docx_to_txt)
registry.register('docx', 'pdf', docx_to_pdf)