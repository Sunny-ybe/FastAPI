from time import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
from urllib.parse import quote_plus

password = quote_plus(settings.database_password)


# db variable name = 'type of db://<username>:<password>@<ip-address/hostname>/database-name-to-connect

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#engine for SQL alchemy to connect to db
engine = create_engine(SQLALCHEMY_DATABASE_URL) 

sessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base()

#createing Dependancy copy-pasted
def get_db():
    db = sessionLocal() #uhaha
    try:
        yield db
    finally:
        db.close()

#connecting to database (postgres) using psycopg2 driver mannually - old way now using sqlalchemy
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi', #match the name of our db created in postgres my case fastapi,
#             user='postgres',
#             password='1115@xxx',
#             cursor_factory=RealDictCursor
#             )
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print(f"Error: {error}")
#         time.sleep(0)
#         break