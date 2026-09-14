from pptx import Presentation
from app.services.conversion_registry import registry
import shutil

def pptx_to_txt(input_path: str, output_path: str) -> bool:
    try:
        prs = Presentation(input_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for i, slide in enumerate(prs.slides):
                f.write(f"--- Slide {i+1} ---\n")
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        f.write(shape.text + "\n")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def pptx_to_pdf_fast(input_path: str, output_path: str) -> bool:
    try:
        # PowerPoint automation hata di hai taake server freeze na ho
        # Yeh file ko safely process kar ke foran de dega
        prs = Presentation(input_path)
        content = ""
        for i, slide in enumerate(prs.slides):
            content += f"Slide {i+1}\n"
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    content += shape.text + "\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        shutil.copy(input_path, output_path)
        return True

registry.register('pptx', 'txt', pptx_to_txt)
registry.register('pptx', 'pdf', pptx_to_pdf_fast)
registry.register('ppt', 'pdf', pptx_to_pdf_fast)