import os
from typing import Optional, Union, List
from pymongo import MongoClient
import motor.motor_asyncio

# db_password = os.getenv('db_password')
# db_login = os.getenv('db_login')
db_password = 'admin'
db_login = 'admin'

db_url = f"mongodb+srv://{db_login}:{db_password}@cluster0.3g8z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# client = MongoClient(db_url)
client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
db = client['HemoDB']
mycol = db['Temperatures']
mycol_teste = db['TemperaturesTest']


async def insert_db_temp(record_dict: dict, teste: bool = False):
    if teste:
        await mycol_teste.insert_one(record_dict)
    else:
        await mycol.insert_one(record_dict)
    return True


async def insert_db_multi_temp(record_list: list, teste: bool = False):
    if teste:
        await mycol_teste.insert_many(record_list)
    else:
        await mycol.insert_many(record_list)
    return True


async def read_db_mod(mod_id: Optional[int] = None) -> List:
    if mod_id is None:
        mod_data = mycol_teste.find().to_list(1000)
    else:
        mod_data = mycol_teste.find({"ModuleID": mod_id}).to_list(length=10)  # .sort([({"Timestamp": -1})])

    return mod_data


async def insert_db_temp_test(record_dict: dict):
    mycol_teste.insert_one(record_dict)
    return True
