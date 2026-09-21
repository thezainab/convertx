import csv
import openpyxl
import os
import subprocess
from app.services.conversion_registry import registry

def xlsx_to_csv(input_path: str, output_path: str) -> bool:
    try:
        wb = openpyxl.load_workbook(input_path)
        sheet = wb.active
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in sheet.iter_rows(values_only=True):
                writer.writerow(["" if cell is None else str(cell) for cell in row])
        return True
    except Exception as e:
        print(f"Spreadsheet error: {e}")
        return False

def xlsx_to_pdf(input_path: str, output_path: str) -> bool:
    try:
        in_path = os.path.abspath(input_path)
        out_path = os.path.abspath(output_path)
        
        # Cloud/Linux friendly PDF conversion using LibreOffice
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(out_path), in_path], check=True)
        return True
    except Exception as e:
        print(f"Excel to PDF error: {e}")
        return False

# Dono features register ho gaye
registry.register('xlsx', 'csv', xlsx_to_csv)
registry.register('xls', 'csv', xlsx_to_csv)
registry.register('xlsx', 'pdf', xlsx_to_pdf)