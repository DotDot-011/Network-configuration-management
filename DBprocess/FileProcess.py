import mysql.connector
import pandas as pd
import json
import logging
from utils.Enums import AvailableDevice

database = 'ConfigService'
user = 'root'
host = 'thor'
# host = '127.0.0.1'
password = 'test'
port = '3306'
# port = '8888'

connectionConfig = {
                    'database': database, 
                    'user': user, 
                    'host': host, 
                    'password': password, 
                    'port': port
                    }

def uploadFile(
                fileName: str,
                userName: str,
                data: str,
                fileType: AvailableDevice,
                fileRepositoryId: int,
                    
                ):

    engine = mysql.connector.connect(
        **connectionConfig)

    TableName = 'File'
    
    try:
        sql = f'''
        INSERT  INTO {TableName} (fileOwnerName, 
                                    fileName, 
                                    fileType, 
                                    fileRepositoryId, 
                                    fileData, 
                                    fileTimestamp)
                VALUES (%s, %s, %s, %s, %s, now()) 
        '''

        print(sql)

        rs = engine.cursor().execute(sql,
                                     (
                                        userName,
                                        fileName,
                                        fileType.value,
                                        fileRepositoryId,
                                        data
                                      )
                                     )

        engine.commit()
        engine.close()

        return True

    except Exception as e:
        
        engine.close()
        raise e

def queryFile(fileId: int):
    
    engine = mysql.connector.connect(
        **connectionConfig)
    TableName = 'File'

    try:
        sql = f'''
        SELECT * FROM {TableName} WHERE fileId = {fileId}
        '''

        data = pd.read_sql(sql, engine)

        json_data = json.loads(data.to_json(orient='index'))['0']
        return json_data

    except Exception as e:
        
        engine.close()
        raise e

def listFileName(repository: str):

    engine = mysql.connector.connect(
        **connectionConfig)
    TableName = 'File'

    try:
        sql = f'''
        SELECT fileId, fileName, fileTimestamp FROM {TableName} WHERE fileRepositoryId = {repository}
        '''

        data = pd.read_sql(sql, engine)
        fileNames = json.loads(data.to_json(orient = 'records'))

        return fileNames

    except Exception as e:
        
        engine.close()
        raise e

# rint(getdata()File