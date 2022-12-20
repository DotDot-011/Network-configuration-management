from fileinput import filename
import string
from pydantic import BaseModel
from NetworkMethod.Model import AccessPointModel
from utils.Enums import AvailableDevice

class UserModel(BaseModel):
    
    AccessPoint : AccessPointModel
    Repository : str

class UserInfoModel(BaseModel):

    username : str
    Password : str

class RepositoryInfoModel(BaseModel):

    repositoryName : str
    username : str
    Host : str
    DeviceType : AvailableDevice