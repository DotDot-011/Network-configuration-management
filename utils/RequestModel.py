from fileinput import filename
import string
from pydantic import BaseModel
from NetworkMethod.Model import AccessPointModel

class UserModel(BaseModel):
    
    AccessPoint : AccessPointModel
    Repository : str

class UserInfoModel(BaseModel):

    Username : str
    Password : str

class RepositoryInfoModel(BaseModel):

    repositoryName : str
    userId : int
    Host : str
    DeviceType : AccessPointModel
    token : str