import logging

from fastapi import APIRouter

from dll_manager import set_duration_ms, start_acquisition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

acquisition_router = APIRouter(prefix="/acquisition", tags=["acquisition"])


@acquisition_router.post("/set-duration")
def set_acquisition_duration(duration: int):
    logger.info(f"Setting acquisition duration to {duration} ms")
    set_duration_ms(duration)
    return {"message": f"Acquisition duration set to {duration} ms\n"}


@acquisition_router.get("/start")
def start_acquisition_endpoint():
    logger.info("Starting acquisition")
    start_acquisition()
    return {"message": "Acquisition started\n"}
