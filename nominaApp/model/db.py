import os
from pymongo.mongo_client import MongoClient

MONGO_URI =  os.environ.get("MONGO_URI")
MONGO_DB = os.environ.get("MONGO_DB") 

class ConnectDB:
    def __init__(self):
       try:
           self.conn = MongoClient(MONGO_URI)
       except Exception as e:
           print('Error al conectar a la base de datos: ', e)
        
    def get_conn(self):
        return self.conn.get_database(MONGO_DB)
    
    def close_conn(self):
        return self.conn.close()

    def  ping(self):
        return self.conn.admin.command('ping')