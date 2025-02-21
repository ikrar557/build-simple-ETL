import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_database_url():
    default_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT')
    }
    
    return f"postgresql://{default_params['user']}:{default_params['password']}@{default_params['host']}:{default_params['port']}/{default_params['database']}"

def create_db_engine():
    return create_engine(get_database_url())