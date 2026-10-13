import os
import shutil
import subprocess
import tempfile
from docx import Document
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


def _find_libreoffice():
    # Different systems mein command ka naam alag hota hai
    return shutil.which("libreoffice") or shutil.which("soffice")


def docx_to_pdf(input_path: str, output_path: str) -> bool:
    try:
        in_path = os.path.abspath(input_path)
        out_path = os.path.abspath(output_path)

        lo = _find_libreoffice()
        if not lo:
            print("Word to PDF error: LibreOffice is server par installed nahi hai")
            return False

        # Alag temp folder taake LibreOffice ka output naam aur hamara naam na takraye
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = subprocess.run(
                [
                    lo,
                    "--headless",
                    "--norestore",
                    "--convert-to", "pdf",
                    "--outdir", tmp_dir,
                    in_path,
                ],
                capture_output=True,
                text=True,
                timeout=120,
                env={**os.environ, "HOME": "/tmp"},
            )

            if result.returncode != 0:
                print(f"LibreOffice error: {result.stderr}")
                return False

            # LibreOffice input file ke naam par PDF banata hai
            produced = os.path.join(
                tmp_dir, os.path.splitext(os.path.basename(in_path))[0] + ".pdf"
            )
            if not os.path.exists(produced):
                print(f"LibreOffice ne PDF nahi banayi. Output: {result.stdout}")
                return False

            # Ab hamare expected naam par move karo
            shutil.move(produced, out_path)

        return True
    except subprocess.TimeoutExpired:
        print("Word to PDF error: conversion timeout ho gayi")
        return False
    except Exception as e:
        print(f"Word to PDF error: {e}")
        return False


registry.register('docx', 'txt', docx_to_txt)
registry.register('doc', 'txt', docx_to_txt)
registry.register('docx', 'pdf', docx_to_pdf)
registry.register('doc', 'pdf', docx_to_pdf)