# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from html import parser
from fastapi import FastAPI, Path
from pymongo import MongoClient
from typing import Optional, Union
from pydantic import BaseModel
import os
from datetime import datetime as dt, datetime
from datetime import tzinfo, timezone
import pytz
from dateutil import parser
import sys
import logging

app = FastAPI()

db_password = os.getenv('db_password')
db_login = os.getenv('db_login')
# db_password = 'admin'
# db_login = 'admin'

var_url = f"mongodb+srv://{db_login}:{db_password}@cluster0.3g8z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(var_url)
db = client.test
mydb = client['HemoDB']
mycol = mydb['Temperatures']

logger = logging.getLogger('foo-logger')

@app.get("/")
def read_root():
    return {"Hellow": "New world"}


@app.post("/Insert_TEMP/")
async def insert_temp(temp: float, timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo')), mod_id: Optional[int] = None, ldr: int) -> bool:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp)
        except Exception as e:
            pass

    print(timestamp)
    logger.debug(str(timestamp))

    record_dict = dict()
    record_dict = {
        "mod_id": mod_id,
        "Temperature": temp,
        "Timestamp": timestamp,
        "LDR": ldr
    }
    mycol.insert_one(record_dict)
    return True


@app.get("/read_mod/{mod_id}")
async def read_mod(mod_id: int) -> object:
    mod_data = {}
    for x in mycol.find({"mod_id": mod_id}):
        mod_data[x['Timestamp']] = {"Temperature": x["Temperature"], "mod_id": x["mod_id"] }
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
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
