import logging

from fastapi import APIRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

acquisition_router = APIRouter(prefix="/acquisition", tags=["acquisition"])


@acquisition_router.get("/start")
def start_acquisition():
    logger.info("Starting data acquisition")
    return {"message": "Data acquisition started"}


@acquisition_router.post("/set-duration")
def set_acquisition_duration(duration: int):
    logger.info(f"Setting acquisition duration to {duration} ms")
    return {"message": f"Acquisition duration set to {duration} ms"}
