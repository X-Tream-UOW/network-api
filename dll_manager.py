import ctypes
from pathlib import Path

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


def set_duration_ms(duration: int) -> None:
    lib.set_duration_ms(duration)


def start_acquisition() -> None:
    lib.start_acquisition()


def stop_acquisition():
    lib.stop_acquisition()


def set_custom_filename(filename: str) -> None:
    lib.set_custom_filename(filename.encode())  # Convert to bytes
