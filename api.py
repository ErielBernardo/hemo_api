from fastapi import FastAPI
from typing import Optional, Union
from datetime import datetime as dt
import pytz
from dateutil import parser
import logging

from datetime import tzinfo, timezone
import sys
from pydantic import BaseModel

from database import insert_db_temp, insert_db_temp_test, read_db_mod

description = """HemoApp API helps hospitals to control and monitor blood components. 🚀🩸🩸"""
app = FastAPI(title="HemoApp",
              description=description,
              version="0.0.2",
              contact={
                  "name": "Eriel Bernardo Albino",
                  "url": "https://www.linkedin.com/in/erielbernardo/",
                  "email": "erielberrnardo@gmail.com",
              }, )

logger = logging.getLogger('foo-logger')


@app.get("/")
async def read_root():
    return {"Hellow": "New world"}


@app.post("/Insert_TEMP/")
async def insert_temp(storage_temp: float, ldr: Optional[int] = None, mod_id: Optional[int] = None,
                      timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo'))) -> dict:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp)
        except Exception as e:
            pass

    print(f"/Insert_TEMP/ - Timestamp {timestamp}, Refrigerator {storage_temp}°C, LDR {ldr}")

    record_dict = {
        "ModuleID": mod_id,
        "Temperature": storage_temp,
        "Timestamp": timestamp,
        "LDR": ldr
    }
    await insert_db_temp(record_dict)
    return record_dict


@app.post("/Insert_TEMP_TEST/")
async def insert_temp_test(ambient_temp: float, storage_temp: float, mod_id: Optional[int] = None,
                           ldr: Optional[int] = None,
                           timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo'))) -> dict:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp)
        except Exception as e:
            pass

    print(
        f"/Insert_TEMP_TEST/ - Timestamp {timestamp}, Refrigerator {storage_temp}°C, Ambient {ambient_temp}°C, LDR {ldr}")

    record_dict = {
        "ModuleID": mod_id,
        "AmbientTemperature": ambient_temp,
        "StorageTemperature": storage_temp,
        "Timestamp": timestamp,
        "LDRStatus": ldr
    }
    await insert_db_temp_test(record_dict)
    return record_dict


@app.get("/read_mod/{mod_id}")
async def read_mod(mod_id: int) -> object:
    mod_data = read_db_mod(mod_id)
    return mod_data


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')
    read_db_mod(0)
