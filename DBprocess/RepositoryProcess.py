import mysql.connector
import pandas as pd
import json
from utils.RequestModel import RepositoryInfoModel
import hashlib
import logging

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

def createRepository(RepoInfo: RepositoryInfoModel):
    
    engine = mysql.connector.connect(
    **connectionConfig)
    TableName = 'Repository'

    try:
        sql = f'''
        INSERT INTO {TableName} (repositoryName, repositoryOwnerId, repositoryHost, repositoryDeviceType, repositoryTimestamp)
        VALUES (%s, %s, %s, %s, now())
        '''
        
        rs = engine.cursor().execute(sql,
                                     (
                                        RepoInfo.repositoryName,
                                        RepoInfo.userId,
                                        RepoInfo.Host,
                                        RepoInfo.DeviceType,
                                      )
                                     )

        engine.commit()
        engine.close()

    except Exception as e:
        engine.close()
        logging.info(e)
