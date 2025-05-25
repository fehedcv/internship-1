from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('username')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
database = os.getenv('database')
if user == "":
    print("Please set the username in the .env file")
    exit()
if password == "":
    print("Please set the password in the .env file")
    exit()
if host == "":
    host = "localhost"
if port == "":
    port = 5432
if database == "":
    print("Please set the database name in the .env file")
    exit()


DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
