from fastapi import FastAPI

from acquisition_api import acquisition_router
from bias_api import bias_router
from uvicorn import run

app = FastAPI()

app.include_router(bias_router)
app.include_router(acquisition_router)

if __name__ == '__main__':
    run(app, host="0.0.0.0", log_level="debug")