from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path
import uuid
import os
import logging

from app.services.conversion_registry import registry
from app.services.converters import image, document, spreadsheet, presentation, pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("convertx")

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
    input_path = None
    try:
        raw_target = (target_format or target or "pdf").lower()
        file_ext = file.filename.rsplit(".", 1)[-1].lower()

        # PDF Fallback feature
        if file_ext in ["pptx", "ppt", "docx", "doc", "xlsx", "xls"] and raw_target in ["webp", "png", "jpg"]:
            target_fmt = "pdf"
        else:
            target_fmt = raw_target

        # Unsupported conversion par pehle hi saaf error do
        if not registry.supports(file_ext, target_fmt):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": f"{file_ext} se {target_fmt} conversion abhi supported nahi hai"
                }
            )

        uid = uuid.uuid4().hex
        safe_name = Path(file.filename).name
        safe_stem = Path(file.filename).stem

        input_path = UPLOAD_DIR / f"{uid}_{safe_name}"

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        output_filename = f"{uid}_{safe_stem}_converted.{target_fmt}"
        output_path = OUTPUT_DIR / output_filename

        try:
            success = registry.convert(file_ext, target_fmt, str(input_path), str(output_path))
        except Exception as e:
            logger.exception("Conversion crashed")
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": f"Conversion failed: {e}"}
            )

        if not success or not output_path.exists() or output_path.stat().st_size == 0:
            logger.error("Conversion returned failure for %s -> %s", file_ext, target_fmt)
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Conversion failed on server"}
            )

        download_url = f"https://convertx-backend-kk05.onrender.com/download/{output_filename}"
        return {
            "success": True,
            "download_url": download_url,
            "filename": output_filename
        }

    except Exception as e:
        logger.exception("Unexpected error")
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    finally:
        # Input file hamesha delete ho jayegi
        if input_path and input_path.exists():
            try:
                os.remove(input_path)
            except Exception as e:
                logger.warning("Input cleanup error: %s", e)


# --- AUTO-DELETE (CLEANUP) SYSTEM ---

def cleanup_files(file_path: Path):
    try:
        if file_path.exists():
            os.remove(file_path)
    except Exception as e:
        print(f"Cleanup error: {e}")


@app.get("/download/{filename}")
async def download_file(filename: str, background_tasks: BackgroundTasks):
    # Path traversal se bachne ke liye sirf file ka naam use karo
    safe_filename = Path(filename).name
    file_path = OUTPUT_DIR / safe_filename
    if file_path.exists():
        # User ko file dene ke baad delete kar do
        background_tasks.add_task(cleanup_files, file_path)
        return FileResponse(path=str(file_path), filename=safe_filename)
    raise HTTPException(status_code=404, detail="File not found")