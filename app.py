from ctypes import Union
from fastapi import FastAPI
from NetworkMethod.Model import AccessPointModel, Cisco, Huawei
from pydantic import parse_obj_as
from utils.Enums import AvailableDevice

app = FastAPI()

def parse_model(access_point : AccessPointModel):
    match access_point.device_type:

        case AvailableDevice.cisco:
            return parse_obj_as(Cisco, access_point)

        case AvailableDevice.huawei:
            return parse_obj_as(Huawei, access_point)

    raise TypeError

@app.post("/")
async def test(access_point : AccessPointModel):
    
    try:
        t = parse_model(access_point)
        return t.test()

    except TypeError:
        return {'status' : False}

@app.post("/Getconfig")
async def create_item(access_point: AccessPointModel):
    
    try:
        point = parse_model(access_point)
        
    except TypeError:
        return {'status' : False}

    config = point.GetConfig()
    return config
    # f = open("demofile2.txt", "w")
    # f.write(config)
    # f.close()

    