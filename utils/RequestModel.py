from fileinput import filename
import string
from pydantic import BaseModel
from NetworkMethod.Model import AccessPointModel

class UserModel(BaseModel):
    
    AccessPoint : AccessPointModel
    Repository : str