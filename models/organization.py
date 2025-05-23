from sqlalchemy import Column,Integer,String,ForeignKey
from database.connection import Base
from sqlalchemy.orm import relationship



class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    users = relationship("User",back_populates="organization")
    
