from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime as dt
import pytz
from dateutil import parser
import logging
from database import insert_db_temp, insert_db_temp_test, insert_db_multi_temp, read_db_mod


description = """HemoApp API helps hospitals to control and monitor blood components. 🚀🩸🩸"""
app = FastAPI(title="HemoApp",
              description=description,
              version="0.0.2",
              contact={
                  "name": "Eriel Bernardo Albino",
                  "url": "https://www.linkedin.com/in/erielbernardo/",
                  "email": "erielberrnardo@gmail.com",
              })

logger = logging.getLogger('foo-logger')


class ModuleDataPost(BaseModel):
    AmbientTemperature: Optional[float] = None
    StorageTemperature: float
    LDRStatus: Optional[int] = None
    ModuleID: Optional[int] = None
    Timestamp: Union[str, dt]


@app.get("/")
async def read_root():
    return {"Hellow": "New world"}


@app.post("/Insert_TEMP/")
async def insert_temp(storage_temp: float, ldr: Optional[int] = None, mod_id: Optional[int] = None,
                      ambient_temp: float = None,
                      timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo')),
                      teste: bool = False) -> object:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp)
        except Exception as e:
            pass

    print(f"/Insert_TEMP/ - Timestamp {timestamp}, Refrigerator {storage_temp}°C, LDR {ldr}")

    record_dict = {
        "ModuleID": mod_id,
        "AmbientTemperature": ambient_temp,
        "StorageTemperature": storage_temp,
        "LDRStatus": ldr,
        "Timestamp": timestamp
    }

    await insert_db_temp(record_dict, teste)
    return record_dict


@app.post("/Insert_MULTI_TEMP/")
async def insert_MULTI_TEMP(data: list[ModuleDataPost], teste: bool = False) -> bool:
    data = jsonable_encoder(data)
    record_list = []
    for document in data:
        print(document)
        timestamp = document['Timestamp']
        if isinstance(timestamp, str):
            try:
                timestamp = parser.parse(timestamp)
            except Exception as e:
                pass
        print(
            f"/Insert_MULTI_TEMP_TEST_MODEL/ - Timestamp {timestamp}, Refrigerator {document['StorageTemperature']}°C, Ambient {document['AmbientTemperature']}°C, LDR {document['LDRStatus']}")
        record_dict = {
            "ModuleID": document['ModuleID'],
            "AmbientTemperature": document['AmbientTemperature'],
            "StorageTemperature": document['StorageTemperature'],
            "Timestamp": timestamp,
            "LDRStatus": document['LDRStatus']
        }
        record_list.append(record_dict)

    await insert_db_multi_temp(record_list, teste)

    return True


@app.post("/Insert_TEMP_TEST/")
async def insert_temp_test(storage_temp: float, ambient_temp: float, ldr: Optional[int] = None,
                           mod_id: Optional[int] = None,
                           timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo'))) -> bool:
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
    print("Inserted")
    return True


@app.post("/Insert_TEMP_EVENT/")
async def insert_temp_test(storage_temp: float, ambient_temp: float, ldr: Optional[int] = None,
                           mod_id: Optional[int] = None,
                           timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo'))) -> bool:
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
    print("Inserted")
    return True


@app.get("/read_mod/{mod_id}")
async def read_mod(mod_id: int) -> object:
    mod_data = read_db_mod(mod_id)
    return mod_data


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')
    read_db_mod(0)
