import logging
import threading
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from dll_manager import get_downsampled_samples, set_duration_ms, set_custom_filename, start_acquisition, \
    stop_acquisition

logger = logging.getLogger(__name__)
acquisition_router = APIRouter(prefix="/acquisition", tags=["acquisition"])


@acquisition_router.post("/set-duration")
def set_acquisition_duration(duration: int):
    """ Set the acquisition duration in milliseconds. The C controller will round up to the nearest round buffer number,
     e.g multiples of ~65ms."""
    logger.info(f"Setting acquisition duration to {duration} ms")
    set_duration_ms(duration)
    return {"message": f"Acquisition duration set to {duration} ms"}


@acquisition_router.post("/set-filename")
def set_acquisition_filename(filename: str):
    """ Set the filename for the acquisition. The C controller will append the .bin extension and generate a default
     timestamped filename if none is given before acquisition"""
    logger.info(f"Setting acquisition filename to {filename}")
    santized_filename = filename.rsplit('.', 1)[0] if '.' in filename else filename
    set_custom_filename(santized_filename)
    return {"message": f"Acquisition filename set to {filename}"}


@acquisition_router.get("/start")
def start_acquisition_endpoint():
    logger.info("Starting acquisition")
    t = threading.Thread(target=start_acquisition, daemon=True)
    t.start()
    return {"message": "Acquisition started"}


@acquisition_router.post("/stop")
def stop_acquisition_endpoint():
    logger.info("Stopping acquisition")
    stop_acquisition()
    return {"message": "Acquisition stop requested"}


@acquisition_router.get("/download")
def download_file(filename: str):  # This could be bettered (stream during acq) to avoid long downloads for large files
    """ Download the specified .bin file from the Pi. """
    path = Path(filename)
    if not path.exists():
        return {"error": "File not found"}
    return FileResponse(path, media_type="application/octet-stream", filename=path.name)


@acquisition_router.get("/stream")
def stream_downsampled():  # This could configure the downsampling factor
    """ Return the newest downsampled samples from the acquisition. The C controller keep track of the newest samples,
    so this will always return the latest data. """
    samples = get_downsampled_samples()
    return JSONResponse(content={"samples": samples})


@acquisition_router.get("/list-files", response_model=List[str])
def list_bin_files():
    """ List all .bin files generated during acquisitions in the parent directory on the pi."""
    data_dir = Path("..")
    bin_files = sorted(f.name for f in data_dir.glob("*.bin"))
    return bin_files


@acquisition_router.delete("/delete-all")
def delete_all_bin_files():
    """ Delete all .bin files in the parent directory on the pi (mind the space on the SD card!). """
    bin_files = list(Path(".").glob("*.bin"))
    if not bin_files:
        raise HTTPException(status_code=404, detail="No .bin files found")

    for f in bin_files:
        try:
            f.unlink()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete {f.name}: {e}")

    return {"message": f"Deleted {len(bin_files)} .bin file(s)"}
