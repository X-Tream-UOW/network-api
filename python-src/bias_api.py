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
    """ Set the bias voltage in millivolts (mV), applied by the DAC before any gain or offset is applied."""
    logger.info(f"bias.set_voltage_mv({mv})")
    try:
        bias_set_voltage_mv(mv)
        return {"message": f"Bias setpoint set to {mv} mV"}
    except BiasError as e:
        raise HTTPException(status_code=500, detail=str(e))


@bias_router.post("/set-polarity")
def set_polarity(negative: bool):
    """ Set the bias polarity : True for negative, False for positive."""
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
        return {"message": "HV enabled"}
    except BiasError as e:
        raise HTTPException(status_code=500, detail=str(e))


@bias_router.post("/off")
def hv_off():
    logger.info("bias.hv_off()")
    try:
        bias_hv_off()
        return {"message": "HV disabled"}
    except BiasError as e:
        raise HTTPException(status_code=500, detail=str(e))


@bias_router.get("/status")
def get_status(timeout_us: int = 100_000):
    """ Get the status of the bias, including whether it is enabled and its polarity."""
    logger.info(f"bias.get_status(timeout_us={timeout_us})")
    try:
        enabled, is_negative = bias_get_status(timeout_us=timeout_us)
        return {"enabled": enabled, "is_negative": is_negative}
    except BiasError as e:
        raise HTTPException(status_code=504 if e.code < 0 else 500, detail=str(e))


@bias_router.get("/voltage")
def get_voltage(timeout_us: int = 100_000):
    """ Get the current bias voltage in millivolts (mV) after gain and offset are applied."""
    logger.info(f"bias.get_bias_mv(timeout_us={timeout_us})")
    try:
        mv = bias_get_bias_mv(timeout_us=timeout_us)
        return {"millivolts": mv, "volts": mv / 1000.0}
    except BiasError as e:
        raise HTTPException(status_code=504 if e.code < 0 else 500, detail=str(e))
