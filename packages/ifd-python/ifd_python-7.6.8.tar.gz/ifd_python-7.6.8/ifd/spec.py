import os
import pymssql
RABBITMQ_USERNAME = str(os.environ.get('RABBITMQ_USERNAME'))
RABBITMQ_PASSWORD = str(os.environ.get('RABBITMQ_PASSWORD'))
RABBITMQ_DNS = str(os.environ.get('RABBITMQ_DNS'))

DB_HOST = str(os.environ.get('DB_HOST'))
DB_NAME = str(os.environ.get('DB_NAME'))
DB_USER = str(os.environ.get('DB_USER'))
DB_PASSWORD = str(os.environ.get('DB_PASSWORD'))

RESULT_FOLDER = "C:/Users/LucienM/source/InfradeepBackV2/csv"

def createConnection():
    """Create a connection to the database"""
    return pymssql.connect(
        server=DB_HOST, 
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
        )