from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:sdkfhkj234ou23o4ldfsdn@database/FastAPI'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)

Base = declarative_base()

#Alchemy database Connection method
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Database Connection without using ORM
# while True:
#     try:
#         # Connect to your postgres DB
#         conn = psycopg2.connect(host="database", database="FastAPI" ,user="postgres",password="sdkfhkj234ou23o4ldfsdn", cursor_factory=RealDictCursor)
#         # Open a cursor to perform database operations
#         cur = conn.cursor()
#         print("Connection to the database sucessful.")
#         break
#     except Exception as error:
#         print('Failed', error)
#         time.sleep(5)