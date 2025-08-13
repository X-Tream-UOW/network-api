import ctypes
from pathlib import Path
from typing import List, Tuple


lib_path = Path(__file__).parent.parent / "libacquisition.so"
lib = ctypes.CDLL(str(lib_path))


class SampleRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("index", ctypes.c_uint32),
        ("sample", ctypes.c_uint16),
    ]


class StreamedSamples(ctypes.Structure):
    _fields_ = [("buffer", ctypes.POINTER(SampleRecord)), ("count", ctypes.c_size_t)]


lib.set_duration_ms.argtypes = [ctypes.c_int]
lib.set_duration_ms.restype = None

lib.start_acquisition.argtypes = []
lib.start_acquisition.restype = None

lib.set_custom_filename.argtypes = [ctypes.c_char_p]
lib.set_custom_filename.restype = None

lib.stop_acquisition.argtypes = []
lib.stop_acquisition.restype = None

lib.get_streamed_samples.argtypes = [ctypes.POINTER(StreamedSamples)]
lib.get_streamed_samples.restype = ctypes.c_int

lib.free_streamed_samples.argtypes = [ctypes.POINTER(StreamedSamples)]
lib.free_streamed_samples.restype = None

lib.reset_stream_state.argtypes = []
lib.reset_stream_state.restype = None


def set_duration_ms(duration: int) -> None:
    lib.set_duration_ms(duration)


def start_acquisition() -> None:
    lib.start_acquisition()


def stop_acquisition() -> None:
    lib.stop_acquisition()


def set_custom_filename(filename: str) -> None:
    lib.set_custom_filename(filename.encode())


def get_downsampled_samples() -> List[List[int]]:
    out = StreamedSamples()
    result = lib.get_streamed_samples(ctypes.byref(out))
    if result != 0 or not bool(out.buffer):
        return []
    samples = []
    for i in range(out.count):
        rec = out.buffer[i]
        samples.append([rec.index, rec.sample])
    lib.free_streamed_samples(ctypes.byref(out))
    return samples


def reset_stream_state() -> None:
    lib.reset_stream_state()


# =========================
# Bias API bindings
# =========================

# C signatures
lib.bias_api_start_io.argtypes = []
lib.bias_api_start_io.restype = None

lib.bias_api_stop_io.argtypes = []
lib.bias_api_stop_io.restype = None

lib.bias_api_set_voltage_mV.argtypes = [ctypes.c_int32]
lib.bias_api_set_voltage_mV.restype = ctypes.c_int

lib.bias_api_set_polarity.argtypes = [ctypes.c_bool]
lib.bias_api_set_polarity.restype = ctypes.c_int

lib.bias_api_hv_on.argtypes = []
lib.bias_api_hv_on.restype = ctypes.c_int

lib.bias_api_hv_off.argtypes = []
lib.bias_api_hv_off.restype = ctypes.c_int

lib.bias_api_get_status.argtypes = [
    ctypes.POINTER(ctypes.c_bool),  # enabled*
    ctypes.POINTER(ctypes.c_bool),  # is_negative*
    ctypes.c_uint  # timeout_us
]
lib.bias_api_get_status.restype = ctypes.c_int

lib.bias_api_get_bias_mV.argtypes = [
    ctypes.POINTER(ctypes.c_int32),  # mV*
    ctypes.c_uint  # timeout_us
]
lib.bias_api_get_bias_mV.restype = ctypes.c_int


class BiasError(RuntimeError):
    def __init__(self, code: int, where: str):
        super().__init__(f"{where} failed (code {code})")
        self.code = code
        self.where = where


def _check(code: int, where: str) -> None:
    if code != 0:
        raise BiasError(code, where)


# Public wrappers
def bias_start_io() -> None:
    lib.bias_api_start_io()


def bias_stop_io() -> None:
    lib.bias_api_stop_io()


def bias_set_voltage_mv(mv: int) -> None:
    _check(lib.bias_api_set_voltage_mV(ctypes.c_int32(mv)), "bias_api_set_voltage_mV")


def bias_set_polarity(negative: bool) -> None:
    _check(lib.bias_api_set_polarity(ctypes.c_bool(negative)), "bias_api_set_polarity")


def bias_hv_on() -> None:
    _check(lib.bias_api_hv_on(), "bias_api_hv_on")


def bias_hv_off() -> None:
    _check(lib.bias_api_hv_off(), "bias_api_hv_off")


def bias_get_status(timeout_us: int = 100_000) -> Tuple[bool, bool]:
    en = ctypes.c_bool(False)
    neg = ctypes.c_bool(False)
    _check(lib.bias_api_get_status(ctypes.byref(en), ctypes.byref(neg), ctypes.c_uint(timeout_us)),
           "bias_api_get_status")
    return bool(en.value), bool(neg.value)


def bias_get_bias_mv(timeout_us: int = 100_000) -> int:
    mv = ctypes.c_int32(0)
    _check(lib.bias_api_get_bias_mV(ctypes.byref(mv), ctypes.c_uint(timeout_us)),
           "bias_api_get_bias_mV")
    return int(mv.value)
