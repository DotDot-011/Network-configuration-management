from pydantic import BaseModel

class AccessPointModel(BaseModel):

    device_type: str
    host: str
    username: str
    password: str