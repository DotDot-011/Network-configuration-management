from distutils.cmd import Command
from fastapi import FastAPI
from utils.NetworkModel import AccessPointModel
import NetworkMethod.Method as configMethod

app = FastAPI()

@app.post("/")
async def test(access_point: AccessPointModel):
    
    print(access_point.__dict__)
    return access_point

@app.post("/Getconfig")
async def create_item(access_point: AccessPointModel):
    
    config = configMethod.GetConfig(access_point)
    f = open("demofile2.txt", "w")
    f.write(config)
    f.close()