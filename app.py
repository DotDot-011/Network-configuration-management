from ctypes import Union
from dataclasses import field
from fastapi import FastAPI, File, UploadFile
from NetworkMethod.Model import AccessPointModel, Cisco, Dell, Huawei, Zyxel
from pydantic import parse_obj_as
from utils.Enums import AvailableDevice
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.RequestModel import UserModel
import mysql.connector
import pandas as pd
import json

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_model(access_point : AccessPointModel):
    if access_point.device_type is AvailableDevice.cisco:

        return parse_obj_as(Cisco, access_point)
    
    elif access_point.device_type is AvailableDevice.huawei:

        return parse_obj_as(Huawei, access_point)

    elif access_point.device_type is AvailableDevice.dell:

        return parse_obj_as(Dell, access_point)

    elif access_point.device_type is AvailableDevice.zyxel:

        return parse_obj_as(Zyxel, access_point)

    raise TypeError

@app.get("/test")
async def check():
    return "test"

# @app.post("/")
# async def test(access_point : AccessPointModel):
    
#     try:
#         t = parse_model(access_point)
#         return t

#     except TypeError as e:
#         return {'status' : False,
#                 'error' : e
#                 }

async def create_item(user: UserModel):
    
    try:
        point = parse_model(user.AccessPoint)
        
    except TypeError as e:
        return {'status' : False,
                'error' : e
                }

    filename = "demofile2.txt"

    config = point.GetConfig()
    f = open(f"./AllFile/{filename}", "w")
    f.write(config)
    f.close()    

    return filename

@app.post("/GetFilePath")
async def get_file_path(user: UserModel):
    filename = await create_item(user)
    # filename = "demofile2.txt"

    return filename

@app.get("/file/{filename}")
async def create_file(filename: str):
    # await create_item(access_point)

    fileRes = FileResponse(path=f"./AllFile/{filename}", media_type='text/mp4')
    return fileRes

@app.get("/getdb")
async def getdata():
    # await create_item(access_point)


    engine = mysql.connector.connect(
        database='students', user='root', host='thor', password='test', port='3306')
    
    try:
        sql = f'''
        SELECT * FROM students_info
        '''

        data = pd.read_sql(sql, engine)

        json_data = json.loads(data.to_json(orient='index'))
        return json_data

    except Exception as e:
        
        engine.close()
        return "error"