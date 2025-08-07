import logging
import threading
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from dll_manager import set_duration_ms, set_custom_filename, start_acquisition, stop_acquisition

logger = logging.getLogger(__name__)
acquisition_router = APIRouter(prefix="/acquisition", tags=["acquisition"])


@acquisition_router.post("/set-duration")
def set_acquisition_duration(duration: int):
    logger.info(f"Setting acquisition duration to {duration} ms")
    set_duration_ms(duration)
    return {"message": f"Acquisition duration set to {duration} ms"}


@acquisition_router.post("/set-filename")
def set_acquisition_filename(filename: str):
    logger.info(f"Setting acquisition filename to {filename}")
    set_custom_filename(filename)
    return {"message": f"Acquisition filename set to {filename}"}


@acquisition_router.get("/start")
def start_acquisition_endpoint():
    logger.info("Starting acquisition in separate thread")
    t = threading.Thread(target=start_acquisition, daemon=True)
    t.start()
    return {"message": "Acquisition started in background thread"}


@acquisition_router.post("/stop")
def stop_acquisition_endpoint():
    logger.info("Stopping acquisition")
    stop_acquisition()
    return {"message": "Acquisition stop requested"}


@acquisition_router.get("/download")
def download_file(filename: str):
    path = Path(filename)
    if not path.exists():
        return {"error": "File not found"}
    return FileResponse(path, media_type="application/octet-stream", filename=path.name)
