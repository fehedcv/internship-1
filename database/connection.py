from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "postgresql://postgres:123456@localhost:5432/invoice"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind = engine,autoflush=False,autocommit=False)
Base = declarative_base()

