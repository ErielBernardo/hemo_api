# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from html import parser

from fastapi import FastAPI, Path
from pymongo import MongoClient
from typing import Optional, Union
from pydantic import BaseModel
import os
from datetime import datetime as dt
from dateutil import parser

app = FastAPI()

# var_mongopass = os.getenv('admin')
var_mongopass = 'admin'
var_url = f"mongodb+srv://admin:{var_mongopass}@cluster0.3g8z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(var_url)
# db = client.test
mydb = client['tests-db']
mycol = mydb['test1']

@app.get("/")
def read_root():
    return {"Hellow": "New world"}


@app.post("/Insert_TEMP/")
def insert_temp(TEMP: float, Data: Union[str, dt]=dt.now()):
    if isinstance(Data, str):
        try:
            Data = parser.parse(Data)
        except:
            pass
    record_dict = dict()
    record_dict ={
        "Temperature": TEMP,
        "Timestamp": Data
    }
    mydb.mycol.insert_one(record_dict)
    return "Success"

@app.post("/Insert_TEMP/{TEMP}/{Data}")
def insert_temp_date(TEMP: float, Data: Union[str, dt]=dt.now()):
    if isinstance(Data, str):
        try:
            Data = parser.parse(Data)
        except:
            pass
    record_dict = dict()
    record_dict ={
        "Temperature": TEMP,
        "Timestamp": Data
    }
    mydb.mycol.insert_one(record_dict)
    return "Success"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
