import logging

from fastapi import APIRouter, HTTPException

from dll_manager import (
    bias_set_voltage_mv,
    bias_set_polarity, bias_hv_on, bias_hv_off, bias_get_status, bias_get_bias_mv, BiasError
)

logger = logging.getLogger(__name__)
bias_router = APIRouter(prefix="/bias", tags=["bias"])


@bias_router.post("/set-voltage")
def set_voltage(mv: int):
    logger.info(f"bias.set_voltage_mv({mv})")
    try:
        bias_set_voltage_mv(mv)
        return {"message": f"Bias setpoint set to {mv} mV"}
    except BiasError as e:
        raise HTTPException(status_code=500, detail=str(e))


@bias_router.post("/set-polarity")
def set_polarity(negative: bool):
    logger.info(f"bias.set_polarity(negative={negative})")
    try:
        bias_set_polarity(negative)
        return {"message": f"Polarity set to {'NEGATIVE' if negative else 'POSITIVE'}"}
    except BiasError as e:
        raise HTTPException(status_code=500, detail=str(e))


@bias_router.post("/on")
def hv_on():
    logger.info("bias.hv_on()")
    try:
        bias_hv_on()
        return {"message": "HV enabled (connected to DUT)"}
    except BiasError as e:
        raise HTTPException(status_code=500, detail=str(e))


@bias_router.post("/off")
def hv_off():
    logger.info("bias.hv_off()")
    try:
        bias_hv_off()
        return {"message": "HV disabled (disconnected from DUT)"}
    except BiasError as e:
        raise HTTPException(status_code=500, detail=str(e))


@bias_router.get("/status")
def get_status(timeout_us: int = 100_000):
    logger.info(f"bias.get_status(timeout_us={timeout_us})")
    try:
        enabled, is_negative = bias_get_status(timeout_us=timeout_us)
        return {"enabled": enabled, "is_negative": is_negative}
    except BiasError as e:
        raise HTTPException(status_code=504 if e.code < 0 else 500, detail=str(e))


@bias_router.get("/voltage")
def get_voltage(timeout_us: int = 100_000):
    logger.info(f"bias.get_bias_mv(timeout_us={timeout_us})")
    try:
        mv = bias_get_bias_mv(timeout_us=timeout_us)
        return {"millivolts": mv, "volts": mv / 1000.0}
    except BiasError as e:
        raise HTTPException(status_code=504 if e.code < 0 else 500, detail=str(e))
