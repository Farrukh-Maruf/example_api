import psycopg2
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings

# this is example of getting url SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        # conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '03092002Df', cursor_factory = RealDictCursor)
        conn = psycopg2.connect(
        host=settings.database_hostname,
        database=settings.database_name,
        user=settings.database_username,
        password=settings.database_password,
        cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print('Database success')
        break
    except Exception as error:
        print(f"Error {error}")
        time.sleep(2)