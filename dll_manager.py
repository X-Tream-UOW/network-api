import ctypes
from pathlib import Path
from typing import List


class SampleRecord(ctypes.Structure):
    _pack_ = 1  # ← this is the missing key
    _fields_ = [
        ("index", ctypes.c_uint32),
        ("sample", ctypes.c_uint16),
    ]


class StreamedSamples(ctypes.Structure):
    _fields_ = [("buffer", ctypes.POINTER(SampleRecord)), ("count", ctypes.c_size_t)]


lib_path = Path(__file__).parent / "libacquisition.so"
lib = ctypes.CDLL(str(lib_path))

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


def stop_acquisition():
    lib.stop_acquisition()


def set_custom_filename(filename: str) -> None:
    lib.set_custom_filename(filename.encode())  # Convert to bytes


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
