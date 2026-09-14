from app.services.conversion_registry import registry
from pdf2docx import Converter
import pypdf

def pdf_to_docx(input_path: str, output_path: str) -> bool:
    try:
        # PDF ko Word (.docx) mein convert karne ka logic
        cv = Converter(input_path)
        cv.convert(output_path)      # Saari pages convert karega
        cv.close()
        return True
    except Exception as e:
        print(f"PDF to DOCX conversion error: {e}")
        return False

def pdf_to_txt(input_path: str, output_path: str) -> bool:
    try:
        # PDF se Text nikalne ka logic
        reader = pypdf.PdfReader(input_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"PDF to TXT conversion error: {e}")
        return False

# Apni class-based registry mein PDF formats ko add karein
registry.register('pdf', 'docx', pdf_to_docx)
registry.register('pdf', 'txt', pdf_to_txt)