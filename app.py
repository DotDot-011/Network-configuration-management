from ctypes import Union
from dataclasses import field
from fastapi import FastAPI, File, UploadFile, Header, status, Response
from NetworkMethod.Model import AccessPointModel, Cisco, Dell, Huawei, Zyxel
from pydantic import parse_obj_as
from utils.Enums import AvailableDevice
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from DBprocess.UserProcess import IsUsernameExist, createUser, updateToken, getUserInfo, isTokenCorrect
from DBprocess.RepositoryProcess import createRepository
from DBprocess.LogProcess import createLog
from utils.RequestModel import UserModel, UserInfoModel, RepositoryInfoModel
from utils.Convertor import makeCorrectResponsePackage, makeFailResponsePackage, hashText
import logging
import jwt
import datetime

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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

def GenerateToken(username: str):
    # define the payload for the JWT
    payload = {
        "user": username,  # issuer
        "iat": datetime.datetime.utcnow(),  # issued at time
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),  # expiration time
    }

    # generate the JWT
    jwt_token = jwt.encode(payload, "secret", algorithm="HS256")

    # print the JWT
    return jwt_token

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

def isTokenValid(token):
    
    if token is None:
        return False

    payload = jwt.decode(token, "secret", algorithms=["HS256"])

    if payload.exp > datetime.datetime.utcnow():
        return False

    if not isTokenCorrect(token, payload.user):
        return False

    return True


def matchedPassword(password, hashedPassword):

    return hashText(password) == hashedPassword    

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

@app.post("/register")
async def register(userInfo : UserInfoModel, response: Response):
    
    try:
        logging.info(IsUsernameExist(userInfo.username))
        if IsUsernameExist(userInfo.username): 
            
            createLog(username=userInfo.username, 
            method='register', 
            response=makeCorrectResponsePackage({"isSuccess": False, "message": "This username have been used"}).__str__(),
            )

            return makeCorrectResponsePackage({"isSuccess": False, "message": "This username have been used"})
        
        createUser(userInfo)

        createLog(username=userInfo.username, 
        method='register', 
        response=makeCorrectResponsePackage({"isSuccess": True, "message": "Created User"}).__str__(),
        )
        
        return makeCorrectResponsePackage({"isSuccess": True, "message": "Created User"})
    
    except Exception as e:
        createLog(username=userInfo.username, 
            method='register', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        return makeFailResponsePackage(e.__str__()) 
    
@app.post("/login")
async def login(userInfo : UserInfoModel, response: Response):
    
    try:
        if not IsUsernameExist(userInfo.username):

            return makeCorrectResponsePackage({"isSuccess": False, "message" : "This username is not exist"})
        
        logging.info("Username exist")
        user = getUserInfo(userInfo.username)

        if not matchedPassword(userInfo.Password, user["userPassword"]):
            
            createLog(username=userInfo.username, 
            method='login', 
            response=makeCorrectResponsePackage({"isSuccess": False, "message" : "Password incorrect"}).__str__(),
            )

            return makeCorrectResponsePackage({"isSuccess": False, "message" : "Password incorrect"})

        logging.info("Password is matched")

        token = GenerateToken(userInfo.username)

        logging.info(f"Generate token {token}")
        updateToken(userInfo, token)
        logging.info(f"Update token success")

        createLog(username=userInfo.username, 
            method='login', 
            response=makeCorrectResponsePackage({"isSuccess": True, "token": token}).__str__(),
            )
        
        return makeCorrectResponsePackage({"isSuccess": True, "token": token})

    except Exception as e:
        createLog(username=userInfo.username, 
            method='login', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        return makeFailResponsePackage(e.__str__()) 

@app.post("/createRepository")
async def createRepository(RepoInfo: RepositoryInfoModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    if isTokenValid(TOKEN):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=RepositoryInfoModel.username, 
            method='createRepository', 
            response=makeCorrectResponsePackage({"isSuccess": False, "message" : "TOKEN invalid"}).__str__(),
            )

        return makeCorrectResponsePackage({"isSuccess": False, "message" : "TOKEN invalid"})

    try :
        createRepository(RepoInfo)

        createLog(username=RepositoryInfoModel.username, 
            method='createRepository', 
            response=makeCorrectResponsePackage({"isSuccess": True, "message" : "created Repository"}).__str__(),
            )

        return makeCorrectResponsePackage({"isSuccess": True, "message" : "created Repository"})
    
    except Exception as e:
        createLog(username=RepositoryInfoModel.username, 
            method='createRepository', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        return makeFailResponsePackage(e.__str__())

if __name__ == "__main__":
    
    try :
        print(GenerateToken("admin"))
    
    except Exception as e:
        print(e.__str__())