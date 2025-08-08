from fastapi import FastAPI
from uvicorn import run

from acquisition_api import *
from bias_api import bias_router

app = FastAPI()

app.include_router(bias_router)
app.include_router(acquisition_router)

if __name__ == '__main__':
    try:
        run(app, host="0.0.0.0", log_level="debug")
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        stop_acquisition()
