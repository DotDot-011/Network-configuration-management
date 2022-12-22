import mysql.connector
import pandas as pd
import json
from utils.RequestModel import UserInfoModel
import logging
from utils.Convertor import hashText

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

def IsUsernameExist(username: str):
    
    engine = mysql.connector.connect(
        **connectionConfig)
    TableName = 'User'

    try:
        sql = f'''
        SELECT * FROM {TableName} WHERE username = '{username}'
        '''

        data = pd.read_sql(sql, engine)

        engine.close()

        return not data.empty

    except Exception as e:
        engine.close()
        logging.info(e)
        
        raise e

def createUser(userInfo: UserInfoModel):
    
    engine = mysql.connector.connect(
    **connectionConfig)
    TableName = 'User'

    hashedPassword = hashText(userInfo.Password)

    try:
        sql = f'''
        INSERT INTO {TableName} (username, userPassword)
        VALUES (%s, %s)
        '''
        
        rs = engine.cursor().execute(sql,
                                     (
                                        userInfo.username,
                                        hashedPassword,
                                      )
                                     )

        engine.commit()
        engine.close()

    except Exception as e:
        engine.close()
        logging.info(e)

        raise e

def updateToken(userInfo: UserInfoModel, token: str):
    
    engine = mysql.connector.connect(
    **connectionConfig)
    TableName = 'User'

    try:
        sql = f'''
        UPDATE {TableName}
        SET token = %s, lastLogin = now()
        WHERE username = %s;
        '''
        
        rs = engine.cursor().execute(sql,
                                     (
                                        token,
                                        userInfo.username
                                      )
                                     )

        engine.commit()
        engine.close()

    except Exception as e:
        engine.close()
        logging.info(e)

        raise e

def getUserInfo(username: str):

    engine = mysql.connector.connect(
        **connectionConfig)
    TableName = 'User'

    try:
        sql = f'''
        SELECT * FROM {TableName} WHERE username = '{username}'
        '''

        data = pd.read_sql(sql, engine)

        engine.close()

        json_data = json.loads(data.to_json(orient='index'))['0']

        return json_data

    except Exception as e:
        engine.close()
        logging.info(e.__str__())
        
        raise e

def isTokenCorrect(token: str, username: str):
    
    try:
        userInfo = getUserInfo(username)

    except Exception as e:
        logging.info(e.__str__())

        raise e

    return userInfo["token"] == token