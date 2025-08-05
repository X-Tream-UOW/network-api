import logging

from fastapi.routing import APIRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bias_router = APIRouter(prefix="/bias", tags=["bias"])

bias_value = None
bias_on = False


@bias_router.post("/set-bias")
async def set_bias(value: float):
    global bias_value
    bias_value = value
    logger.info(f"Set bias to {bias_value}")
    return {"message": f"Bias set to {bias_value}"}


@bias_router.get("/get-bias")
async def get_bias():
    logger.info("Get bias value")
    return {"bias_value": bias_value}


@bias_router.post("/on")
async def bias_on_endpoint():
    global bias_on
    bias_on = True
    logger.info("Bias turned ON")
    return {"message": "Bias is ON"}


@bias_router.post("/off")
async def bias_off_endpoint():
    global bias_on
    bias_on = False
    logger.info("Bias turned OFF")
    return {"message": "Bias is OFF"}


@bias_router.get("/status")
async def bias_status():
    logger.info("Get bias status")
    return {"bias_on": bias_on, "bias_value": bias_value}
