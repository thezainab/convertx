import csv
import os
import shutil
import subprocess
import tempfile
import openpyxl
from app.services.conversion_registry import registry


def _find_libreoffice():
    return shutil.which("libreoffice") or shutil.which("soffice")


def _lo_convert(input_path: str, output_path: str, fmt: str) -> bool:
    """LibreOffice se file convert karta hai aur output ko expected naam par rakhta hai."""
    try:
        in_path = os.path.abspath(input_path)
        out_path = os.path.abspath(output_path)

        lo = _find_libreoffice()
        if not lo:
            print("LibreOffice is server par installed nahi hai")
            return False

        with tempfile.TemporaryDirectory() as tmp_dir:
            result = subprocess.run(
                [lo, "--headless", "--norestore", "--convert-to", fmt,
                 "--outdir", tmp_dir, in_path],
                capture_output=True,
                text=True,
                timeout=120,
                env={**os.environ, "HOME": "/tmp"},
            )
            if result.returncode != 0:
                print(f"LibreOffice error: {result.stderr}")
                return False

            produced = os.path.join(
                tmp_dir, os.path.splitext(os.path.basename(in_path))[0] + "." + fmt
            )
            if not os.path.exists(produced):
                print(f"LibreOffice ne output nahi banaya: {result.stdout}")
                return False

            shutil.move(produced, out_path)
        return True
    except subprocess.TimeoutExpired:
        print("LibreOffice conversion timeout ho gayi")
        return False
    except Exception as e:
        print(f"LibreOffice conversion error: {e}")
        return False


def xlsx_to_csv(input_path: str, output_path: str) -> bool:
    try:
        # data_only=True: formulas ki jagah un ki calculated value aayegi
        wb = openpyxl.load_workbook(input_path, data_only=True)
        sheet = wb.active
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in sheet.iter_rows(values_only=True):
                writer.writerow(["" if cell is None else str(cell) for cell in row])
        return True
    except Exception as e:
        print(f"Spreadsheet error: {e}")
        return False


def xls_to_csv(input_path: str, output_path: str) -> bool:
    # openpyxl purani .xls nahi parh sakta, is liye LibreOffice use hota hai
    return _lo_convert(input_path, output_path, "csv")


def xlsx_to_pdf(input_path: str, output_path: str) -> bool:
    return _lo_convert(input_path, output_path, "pdf")


registry.register('xlsx', 'csv', xlsx_to_csv)
registry.register('xls', 'csv', xls_to_csv)
registry.register('xlsx', 'pdf', xlsx_to_pdf)
registry.register('xls', 'pdf', xlsx_to_pdf)