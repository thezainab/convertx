from app.services.conversion_registry import registry
from pdf2docx import Converter
import pypdf


def pdf_to_docx(input_path: str, output_path: str) -> bool:
    cv = None
    try:
        cv = Converter(input_path)
        cv.convert(output_path)  # Saari pages convert karega
        return True
    except Exception as e:
        print(f"PDF to DOCX conversion error: {e}")
        return False
    finally:
        if cv is not None:
            try:
                cv.close()
            except Exception:
                pass


def pdf_to_txt(input_path: str, output_path: str) -> bool:
    try:
        reader = pypdf.PdfReader(input_path)

        if reader.is_encrypted:
            print("PDF to TXT error: PDF password protected hai")
            return False

        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        if not text.strip():
            print("PDF to TXT error: PDF mein text nahi mila (shayad scanned PDF hai)")
            return False

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"PDF to TXT conversion error: {e}")
        return False


registry.register('pdf', 'docx', pdf_to_docx)
registry.register('pdf', 'txt', pdf_to_txt)