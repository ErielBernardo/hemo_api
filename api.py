import uvicorn
from fastapi import APIRouter, HTTPException, Request, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, Union, List, Dict

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson.codec_options import CodecOptions

from Model import ModuleData, DateRange
from config import settings

from datetime import datetime as dt
import pytz
from dateutil import parser
from dateutil.tz import gettz

gmt3 = pytz.timezone('America/Sao_Paulo')

router = APIRouter()

mongodb_client: AsyncIOMotorClient
db: AsyncIOMotorDatabase


@router.on_event("startup")
async def startup_db_client():
    global mongodb_client
    mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    global db
    db = mongodb_client[settings.DB_NAME]


@router.on_event("shutdown")
async def shutdown_db_client():
    mongodb_client.close()


@router.get("/read_mod/{mod_id}", tags=["Reads"], response_description="List a specific module data",
            response_model=List[ModuleData])
async def read_mod(mod_id: int, top: int = 1000):
    if (
            mod_data := await db['TemperaturesTest'].find({"ModuleID": mod_id}).sort('Timestamp',
                                                                                     pymongo.DESCENDING).to_list(
                top)) is not None:
        return mod_data
    return HTTPException(status_code=404, detail=f"Module {mod_id} not found")


@router.post("/read_mods/", tags=["Reads"], response_description="Returns a collection of modules data by period",
             response_model=List[ModuleData])
async def read_mods(data: Optional[DateRange] = None, top: int = 1000):  # request: Request,
    print(data)
    if data is not None:
        data = jsonable_encoder(data)
        star_date = parser.parse(data['StartDate'], tzinfos={None: gettz('America/Sao_Paulo')})
        end_date = parser.parse(data['EndDate'], tzinfos={None: gettz('America/Sao_Paulo')})
        mod_data = await db['TemperaturesTest'].with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('America/Sao_Paulo'))).find(
            {'Timestamp': {'$gte': star_date, '$lt': end_date}}).sort('Timestamp', pymongo.DESCENDING).to_list(top)
    else:
        mod_data = await db['TemperaturesTest'].with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('America/Sao_Paulo'))).find().sort(
            'Timestamp', pymongo.DESCENDING).to_list(top)
    # mod_data = mod_data.apply(lambda x: parser.parse(x['Timestamp'], tzinfos={None: gettz('America/Sao_Paulo')}))
    return mod_data


@router.post("/Insert_TEMP_TEST/", tags=["Inserts"])
async def insert_temp_test(storage_temp: float, ambient_temp: float, ldr: Optional[int] = None,
                           mod_id: Optional[int] = None,
                           timestamp: Union[str, dt] = dt.now(tz=pytz.timezone('America/Sao_Paulo'))) -> bool:
    if isinstance(timestamp, str):
        try:
            timestamp = parser.parse(timestamp, tzinfos={None: gettz('America/Sao_Paulo')})
        except Exception as e:
            pass
    print(f"/Insert_TEMP_TEST/ - Timestamp {timestamp}, R {storage_temp}°C, A {ambient_temp}°C, LDR {ldr}")
    record_dict = {
        "AmbientTemperature": ambient_temp,
        "StorageTemperature": storage_temp,
        "LDRStatus": ldr,
        "Timestamp": timestamp,
        "ModuleID": mod_id
    }
    await db['TemperaturesTest'].insert_one(record_dict)
    return True


@router.post("/Insert_TEMP/", tags=["Inserts"], response_description="Insert an unique read data")
async def insert_temp(data: ModuleData, teste: bool = False) -> bool:
    data = jsonable_encoder(data)
    if isinstance(data['Timestamp'], str):
        try:
            data['Timestamp'] = parser.parse(data['Timestamp'], tzinfos={None: gettz('America/Sao_Paulo')})
        except Exception as e:
            pass
    print(data)
    if teste:
        await db['TemperaturesTest'].insert_one(data)
    else:
        await db['Temperatures'].insert_one(data)
    return True


@router.post("/Insert_MULTI_TEMP/", tags=["Inserts"], response_description="Insert multiple read data")
async def insert_multi_temp(data: list[ModuleData], teste: bool = False) -> bool:
    data = jsonable_encoder(data)
    for document in data:
        if isinstance(document['Timestamp'], str):
            try:
                document['Timestamp'] = parser.parse(document['Timestamp'], tzinfos={None: gettz('America/Sao_Paulo')})
            except Exception as e:
                pass
        print(document)
    if teste:
        await db['TemperaturesTest'].insert_many(data)
    else:
        await db['Temperatures'].insert_many(data)
    return True


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == "__main__":
    uvicorn.run(
        "api:router",
        host="127.0.0.1",
        reload=True,
        port=8000
    )
