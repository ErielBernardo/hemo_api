from fastapi import FastAPI
from pymongo import MongoClient
import os

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


async def insert_db_temp(record_dict: dict):
    mycol.insert_one(record_dict)
    return True


async def insert_db_temp_test(record_dict: dict):
    mycol_teste.insert_one(record_dict)
    return True


def read_db_mod(mod_id: int) -> object:
    mod_data = {}
    for x in mycol.find({"mod_id": mod_id}):
        mod_data[x['Timestamp']] = {"Temperature": x["Temperature"], "mod_id": x["mod_id"]}
    return mod_data
