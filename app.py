from fastapi import FastAPI

from acquisition_api import acquisition_router
from bias_api import bias_router

app = FastAPI()

app.include_router(bias_router)
app.include_router(acquisition_router)
