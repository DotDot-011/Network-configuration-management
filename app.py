from typing import Union
from dataclasses import field
from fastapi import FastAPI, File, UploadFile, Header, status, Response
from NetworkMethod.Model import AccessPointModel, Cisco, Dell, Huawei, Zyxel
from pydantic import parse_obj_as
from utils.Enums import AvailableDevice
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from DBprocess.UserProcess import IsUsernameExist, createUser, updateToken, getUserInfo, isTokenCorrect
from DBprocess.RepositoryProcess import insertRepository, queryRepositories, updateEnableSnmp
from DBprocess.LogProcess import createLog
from DBprocess.FileProcess import uploadFile, listFileName, queryFile
from utils.RequestModel import HostModel, UserInfoModel, RepositoryInfoModel, FileModel, EnableSnmpModel, AnalyzeModel
from utils.Convertor import makeCorrectResponsePackage, makeFailResponsePackage, hashText, textToCommands
import logging
import jwt
import datetime
from ccat import AnalyzeFile

app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG,
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='Server.log'
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

def isTokenValid(token, username):
    
    if token is None:

        logging.info("There is no token")

        return False

    try :
        payload = jwt.decode(token, "secret", algorithms=["HS256"])

    except: 
        logging.info("Token format not correct")

        return False

    if payload["user"] != username:
        logging.info("Token username not correct")

        return False

    if datetime.datetime.fromtimestamp(payload["exp"]) < datetime.datetime.utcnow():
        logging.info("Token expired")

        return False

    if not isTokenCorrect(token, payload["user"]):
        logging.info("Token unregis")

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

# async def create_item(user: UserModel):
    
#     try:
#         point = parse_model(user.AccessPoint)
        
#     except TypeError as e:
#         return {'status' : False,
#                 'error' : e
#                 }

#     filename = "demofile2.txt"

#     config = point.GetConfig()
#     f = open(f"./AllFile/{filename}", "w")
#     f.write(config)
#     f.close()    

#     return filename

# @app.post("/GetFilePath")
# async def get_file_path(user: UserModel):
#     filename = await create_item(user)
#     # filename = "demofile2.txt"

#     return filename

# @app.get("/file/{filename}")
# async def create_file(filename: str):
#     # await create_item(access_point)

#     fileRes = FileResponse(path=f"./AllFile/{filename}", media_type='text/mp4')
#     return fileRes

@app.get("/getFile/{username}/{fileId}")
async def getFile(username: str, fileId: int, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    if not isTokenValid(TOKEN, username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=username, 
            method='getFile', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")

    try:
        file = queryFile(fileId)

        return makeCorrectResponsePackage(file)

    except Exception as e:
        createLog(username=username, 
            method='getFile', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return makeFailResponsePackage(e.__str__())

@app.get("/getFileNames/{username}/{repository}")
async def getFileNames(username: str, repository: str, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    if not isTokenValid(TOKEN, username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=username, 
            method='getFileNames', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")

    try:
        fileNames = listFileName(repository)

        return makeCorrectResponsePackage(fileNames)

    except Exception as e:
        createLog(username=username, 
            method='getFileNames', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )
    
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

@app.post("/saveConfig")
async def uploadConfig(file: FileModel, hostObject: HostModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    if not isTokenValid(TOKEN, hostObject.username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=hostObject.username, 
            method='saveConfig', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")

    try:
        uploadFile(fileName=file.name, userName=hostObject.username, data=file.data, fileType=hostObject.AccessPoint.device_type, fileRepositoryId=hostObject.Repository)
        
        return makeCorrectResponsePackage("save complete")

    except Exception as e:
        createLog(username=hostObject.username, 
            method='saveConfig', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

@app.post("/uploadConfig")
async def uploadConfig(file: FileModel, hostObject: HostModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    if not isTokenValid(TOKEN, hostObject.username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=hostObject.username, 
            method='uploadConfig', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")

    try:
        accessPoint = parse_model(hostObject.AccessPoint)
        oldConfig = accessPoint.GetConfig()
        oldCommands = textToCommands(oldConfig)

        commands = textToCommands(file.data)
        accessPoint.UploadConfig(commands)
        accessPoint.CopyRunToStartup()
        newConfig = accessPoint.GetConfig()

        uploadFile(fileName=file.name, userName=hostObject.username, data=newConfig, fileType=hostObject.AccessPoint.device_type, fileRepositoryId=hostObject.Repository)

        return makeCorrectResponsePackage("upload complete")

    except Exception as e:
        accessPoint.UploadConfig(oldCommands)
        accessPoint.CopyRunToStartup()
        createLog(username=hostObject.username, 
            method='getConfig', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )
        
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

@app.post("/getConfig")
async def getConfig(hostObject: HostModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):

    if not isTokenValid(TOKEN, hostObject.username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=hostObject.username, 
            method='getConfig', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")

    try:
        accessPoint = parse_model(hostObject.AccessPoint)

        config = accessPoint.GetConfig()

        return makeCorrectResponsePackage(config)

    except Exception as e:
        createLog(username=hostObject.username, 
            method='getConfig', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

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

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

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

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__()) 

@app.post("/createRepository")
async def createRepository(RepoInfo: RepositoryInfoModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    if not isTokenValid(TOKEN, RepoInfo.username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=RepoInfo.username, 
            method='createRepository', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")

    try :
        insertRepository(RepoInfo)

        createLog(username=RepoInfo.username, 
            method='createRepository', 
            response=makeCorrectResponsePackage({"isSuccess": True, "message" : "created Repository"}).__str__(),
            )

        return makeCorrectResponsePackage({"isSuccess": True, "message" : "created Repository"})
    
    except Exception as e:
        createLog(username=RepoInfo.username, 
            method='createRepository', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )
        
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

@app.get("/getRepositories/{username}")
async def getRepositories(username: str, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    if not isTokenValid(TOKEN, username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=username, 
            method='getRepositories', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")
    
    try: 
        Repositories = queryRepositories(username)

        createLog(username=username, 
            method='getRepositories', 
            response=makeCorrectResponsePackage(Repositories).__str__(),
            )

        return makeCorrectResponsePackage(Repositories)
    
    except Exception as e:
        createLog(username=username, 
            method='getRepositories', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

@app.post("/AnalyzeConfig")
async def AnalyzeConfig(request: AnalyzeModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    try: 
        Repositories = queryRepositories(request.username)

        createLog(username=request.username, 
            method='AnalyzeConfig', 
            response=makeCorrectResponsePackage(Repositories).__str__(),
            )

        return makeCorrectResponsePackage(AnalyzeFile(request.config))
    
    except Exception as e:
        createLog(username=request.username, 
            method='AnalyzeConfig', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

@app.post("/EnableSnmp")
async def EnableSnmp(host: EnableSnmpModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):

    if not isTokenValid(TOKEN, host.username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=host.username, 
            method='EnableSnmp', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")
    
    try: 
        accessPoint = parse_model(host.AccessPoint)
        oldConfig = accessPoint.GetConfig()
        oldCommands = textToCommands(oldConfig)

        output = accessPoint.EnableSnmp(community=host.community)
        nowConfig = accessPoint.GetConfig()  
        print(nowConfig)
        accessPoint.CopyRunToStartup()
        uploadFile(fileName="EnableSnmp", userName=host.username, data=nowConfig, fileType=host.AccessPoint.device_type, fileRepositoryId=host.Repository)

        if("Invalid" in output):
            raise SyntaxError

        
        updateEnableSnmp(host.Repository, host.community)

        createLog(username=host.username, 
            method='EnableSnmp', 
            response=makeCorrectResponsePackage("update successful").__str__(),
            )

        return makeCorrectResponsePackage("update successful")
    
    except Exception as e:
        accessPoint.UploadConfig(oldCommands)
        accessPoint.CopyRunToStartup()
        createLog(username=host.username, 
            method='AnalyzeConfig', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

@app.post("/getInformation")
async def getInformation(host: EnableSnmpModel, response: Response, TOKEN: Union[str, None] = Header(default=None)):
    
    print(host)

    if not isTokenValid(TOKEN, host.username):
        
        response.status_code = status.HTTP_401_UNAUTHORIZED

        createLog(username=host.username, 
            method='getInformation', 
            response=makeFailResponsePackage("TOKEN invalid").__str__(),
            )

        return makeFailResponsePackage("TOKEN invalid")
    
    try: 
        accessPoint = parse_model(host.AccessPoint)
        
        uptime = accessPoint.getUptime(community=host.community)
        location = accessPoint.getLocation(community=host.community)
        description = accessPoint.getDescr(community=host.community)

        package = {

            "uptime" : uptime,
            "location" : location,
            "description" : description
        }

        createLog(username=host.username, 
            method='getInformation', 
            response=makeCorrectResponsePackage(package).__str__(),
            )

        return makeCorrectResponsePackage(package)
    
    except Exception as e:
        createLog(username=host.username, 
            method='getInformation', 
            response=makeFailResponsePackage(e.__str__()).__str__(),
            )

        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

        return makeFailResponsePackage(e.__str__())

if __name__ == "__main__":
    
    try :
        print(GenerateToken("admin"))
    
    except Exception as e:
        print(e.__str__())