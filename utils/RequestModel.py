from fileinput import filename
import string
from pydantic import BaseModel
from NetworkMethod.Model import AccessPointModel
from utils.Enums import AvailableDevice

class HostModel(BaseModel):
    
    AccessPoint : AccessPointModel
    username : str
    Repository : str

class FileModel(BaseModel):

    name: str
    data: str
    fileType: AvailableDevice

class UserInfoModel(BaseModel):

    username : str
    Password : str

class RepositoryInfoModel(BaseModel):

    repositoryName : str
    username : str
    Host : str
    DeviceType : AvailableDevice