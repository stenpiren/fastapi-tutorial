from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from time import time
import psycopg2
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency: call the function everytime there is a request for the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host="172.28.48.1", database="fastapi", user="postgres", password="dbsuperpwd", cursor_factory=RealDictCursor)
#         # RealDictCursor returns all fields when queried not just names, but columns (value, colum)
#         cursor = conn.cursor()
#         print("Database connection was sucessful!")
#         break

#     except Exception as error:
#         print("Connecting to database failed! Try again.")
#         print("Error:\n", error)
#         time.sleep(2)