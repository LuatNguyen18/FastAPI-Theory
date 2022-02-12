from enum import auto
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# Connection made through environment variables
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}: \
                          {settings.database_port}/{settings.database_name}'


#Engine establishes the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)


#Database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependency
# Creates a session with the database for processing the queries
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Database connection without sqlAlchemy
# while True:

#     #Connection to database
#     try:
#         conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull.")
#         break

#     except Exception as error:
#         print("Connecting to database failed.")
#         print("Error:", error)
#         time.sleep(2)