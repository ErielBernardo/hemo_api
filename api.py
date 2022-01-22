# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from html import parser
from fastapi import FastAPI, Path
from pymongo import MongoClient
from typing import Optional, Union
import os
from datetime import datetime as dt
import pytz
from dateutil import parser
import logging
from datetime import tzinfo, timezone
import sys
from pydantic import BaseModel
from uvicorn import logging

description = """HemoApp API helps hospitals to control and monitor blood components. 🚀"""
app = FastAPI(title="HemoApp",
              description=description,
              version="0.0.1",
              contact={
                  "name": "Eriel Bernardo Albino",
                  "url": "https://www.linkedin.com/in/erielbernardo/",
                  "email": "erielberrnardo@gmail.com",
              },)

db_password = os.getenv('db_password')
db_login = os.getenv('db_login')
# db_password = 'admin'
# db_login = 'admin'

var_url = f"mongodb+srv://{db_login}:{db_password}@cluster0.3g8z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(var_url)
db = client.test
mydb = client['HemoDB']
mycol = mydb['Temperatures']
mycol_teste = mydb['TemperaturesTest']

logger = logging.getLogger('foo-logger')


@app.get("/")
async def read_root():
    return {"Hellow": "New world"}


@app.post("/Insert_TEMP/")
async def insert_temp(temp: float, timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo')),
                      mod_id: Optional[int] = None, ldr: Optional[int] = None) -> bool:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp)
        except Exception as e:
            pass

    print(timestamp)
    logger.debug(str(timestamp))

    record_dict = dict()
    record_dict = {
        "ModuleID": mod_id,
        "Temperature": temp,
        "Timestamp": timestamp,
        "LDR": ldr
    }
    mycol.insert_one(record_dict)
    return True


@app.post("/Insert_TEMP_TEST/")
async def insert_temp_test(ambient_temp: float, storage_temp: float,
                           timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo')),
                           mod_id: Optional[int] = None, ldr: Optional[int] = None) -> bool:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp)
        except Exception as e:
            pass

    print(timestamp)
    logger.debug(str(timestamp), str(storage_temp))

    record_dict = dict()
    record_dict = {
        "ModuleID": mod_id,
        "AmbientTemperature": ambient_temp,
        "StorageTemperature": storage_temp,
        "Timestamp": timestamp,
        "LDRStatus": ldr
    }
    mycol_teste.insert_one(record_dict)
    return True


@app.get("/read_mod/{mod_id}")
async def read_mod(mod_id: int) -> object:
    mod_data = {}
    for x in mycol.find({"mod_id": mod_id}):
        mod_data[x['Timestamp']] = {"Temperature": x["Temperature"], "mod_id": x["mod_id"]}
    return mod_data


@app.post("/Insert_TEMP/{TEMP}/{timestamp}")
def insert_temp_date(temp: float, timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo'))) -> bool:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp)
        except Exception as e:
            pass

    print(timestamp)
    logger.debug(str(timestamp))

    record_dict = dict()
    record_dict = {
        "Temperature": temp,
        "Timestamp": timestamp
    }
    mycol.insert_one(record_dict)
    return True


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')
