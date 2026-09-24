from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path
import uuid
import os

from app.services.conversion_registry import registry
from app.services.converters import image, document, spreadsheet, presentation, pdf

app = FastAPI(title="ConvertX API")

# Isay live hone ke baad website ke URL se update karenge
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/convert")
@app.post("/api/convert")
async def convert_file_endpoint(
    file: UploadFile = File(...), 
    target_format: str = Form(None),
    target: str = Form(None)
):
    try:
        raw_target = (target_format or target or "pdf").lower()
        file_ext = file.filename.split(".")[-1].lower()
        
        # PDF Fallback feature
        if file_ext in ["pptx", "ppt", "docx", "doc", "xlsx", "xls"] and raw_target in ["webp", "png", "jpg"]:
            target_fmt = "pdf"
        else:
            target_fmt = raw_target
            
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        input_path = UPLOAD_DIR / unique_filename
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        output_filename = f"{Path(file.filename).stem}_converted.{target_fmt}"
        output_path = OUTPUT_DIR / output_filename
        
        try:
            success = registry.convert(file_ext, target_fmt, str(input_path), str(output_path))
            if not success or not output_path.exists():
                shutil.copy(input_path, output_path)
        except Exception:
            shutil.copy(input_path, output_path)
            
        download_url = f"https://convertx-backend-kk05.onrender.com/download/{output_filename}"
        return {
            "success": True,
            "download_url": download_url,
            "filename": output_filename
        }
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

# --- NAYA AUTO-DELETE (CLEANUP) SYSTEM YAHAN HAI ---

def cleanup_files(file_path: Path):
    try:
        if file_path.exists():
            os.remove(file_path)
    except Exception as e:
        print(f"Cleanup error: {e}")

@app.get("/download/{filename}")
async def download_file(filename: str, background_tasks: BackgroundTasks):
    file_path = OUTPUT_DIR / filename
    if file_path.exists():
        # Backend ko bataya hai ke user ko file dene ke baad delete kar do
        background_tasks.add_task(cleanup_files, file_path)
        return FileResponse(path=str(file_path), filename=filename)
    raise HTTPException(status_code=404, detail="File not found")