from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from acquisition_api import *
from bias_api import bias_router
from dll_manager import bias_start_io, bias_stop_io

app = FastAPI()

app.include_router(bias_router)
app.include_router(acquisition_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # or ["*"] for a quick demo
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    try:
        bias_start_io()
        run(app, host="0.0.0.0", log_level="debug")
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        stop_acquisition()
        bias_stop_io()
