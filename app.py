from ctypes import Union
from fastapi import FastAPI
from NetworkMethod.Model import AccessPointModel, Cisco, Dell, Huawei, Zyxel
from pydantic import parse_obj_as
from utils.Enums import AvailableDevice

app = FastAPI()

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

@app.post("/")
async def test(access_point : AccessPointModel):
    
    try:
        t = parse_model(access_point)
        return t

    except TypeError as e:
        return {'status' : False,
                'error' : e
                }

@app.post("/Getconfig")
async def create_item(access_point: AccessPointModel):
    
    try:
        point = parse_model(access_point)
        
    except TypeError as e:
        return {'status' : False,
                'error' : e
                }

    config = point.GetConfig()
    return config
    # f = open("demofile2.txt", "w")
    # f.write(config)
    # f.close()

    