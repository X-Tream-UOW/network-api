import ctypes
from pathlib import Path


class SampleRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("index", ctypes.c_uint32),
        ("sample", ctypes.c_uint16),
    ]


class DownsampleResult(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(SampleRecord)),
        ("count", ctypes.c_size_t),
    ]


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

lib.downsample_file.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(DownsampleResult)]
lib.downsample_file.restype = ctypes.c_int

lib.free_downsampled.argtypes = [ctypes.POINTER(DownsampleResult)]
lib.free_downsampled.restype = None


def set_duration_ms(duration: int) -> None:
    lib.set_duration_ms(duration)


def start_acquisition() -> None:
    lib.start_acquisition()


def stop_acquisition():
    lib.stop_acquisition()


def set_custom_filename(filename: str) -> None:
    lib.set_custom_filename(filename.encode())  # Convert to bytes


def get_downsampled_samples(filename: str, max_points: int = 1000):
    result = DownsampleResult()
    path = Path(filename).resolve()
    status = lib.downsample_file(str(path).encode(), max_points, ctypes.byref(result))

    if status != 0 or not result.data:
        return []

    samples = [
        {"index": result.data[i].index, "sample": result.data[i].sample}
        for i in range(result.count)
    ]

    lib.free_downsampled(ctypes.byref(result))
    return samples
# TODO : add clean shutdown of the library if needed
