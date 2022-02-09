# uvicorn --host 0.0.0.0 app.main:app --reload
import uvicorn
from fastapi import FastAPI

from config import settings
from api import router

import logging

description = """HemoApp API helps hospitals to control and monitor blood components. 🚀🩸🩸"""
app = FastAPI(title=settings.APP_NAME,
              description=settings.DESCRIPTION,
              version=settings.VERSION,
              contact=settings.CONTACT)

logger = logging.getLogger(__name__)


@app.get("/", tags=["Home"])
async def read_root():
    return {"Hellow": "New world"}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=8000,
    )
