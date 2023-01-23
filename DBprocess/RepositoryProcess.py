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

def insertRepository(RepoInfo: RepositoryInfoModel):
    
    engine = mysql.connector.connect(
    **connectionConfig)
    TableName = 'Repository'

    try:
        sql = f'''
        INSERT INTO {TableName} (repositoryName, repositoryOwnerName, repositoryHost, repositoryDeviceType, repositoryTimestamp, IsSnmpEnable)
        VALUES (%s, %s, %s, %s, now())
        '''
        
        rs = engine.cursor().execute(sql,
                                     (
                                        RepoInfo.repositoryName,
                                        RepoInfo.username,
                                        RepoInfo.Host,
                                        RepoInfo.DeviceType.value,
                                        0
                                      )
                                     )

        engine.commit()
        engine.close()

    except Exception as e:
        engine.close()
        logging.info(e)
        
        raise e

def queryRepositories(username: str):

    engine = mysql.connector.connect(
    **connectionConfig)
    TableName = 'Repository'

    try:
        sql = f'''
        SELECT * FROM {TableName} WHERE repositoryOwnerName = '{username}'
        '''

        data = pd.read_sql(sql, engine)
        json_data = json.loads(data.to_json(orient='records'))

        engine.close()

        return json_data

    except Exception as e:
        engine.close()
        logging.info(e)

        raise e

def updateEnableSnmp(repositoryId: int, snmpCommunity: str):
    
    engine = mysql.connector.connect(
    **connectionConfig)
    TableName = 'Repository'

    try:
        sql = f'''
        UPDATE {TableName}
        SET SnmpCommunity = %s, IsSnmpEnable = %s
        WHERE repositoryId = %s;
        '''
        
        rs = engine.cursor().execute(sql,
                                     (
                                        snmpCommunity,
                                        1,
                                        repositoryId
                                      )
                                     )

        engine.commit()
        engine.close()

    except Exception as e:
        engine.close()
        logging.info(e)
        
        raise e