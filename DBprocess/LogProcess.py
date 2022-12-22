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
                    
def createLog(username: str, method: str, response: str, repositoryId = None):
    
    engine = mysql.connector.connect(
    **connectionConfig)
    TableName = 'APILog'

    try:
        sql = f'''
        INSERT INTO {TableName} (username, repositoryId, method, response, logTimestamp)
        VALUES (%s, %s, %s, %s, now())
        '''
        
        rs = engine.cursor().execute(sql,
                                     (
                                        username,
                                        repositoryId,
                                        method,
                                        response,
                                      )
                                     )

        engine.commit()
        engine.close()

    except Exception as e:
        engine.close()
        logging.info(e)

        raise e
