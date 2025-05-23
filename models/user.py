
from sqlalchemy import Column,Integer,String,ForeignKey
from database.connection import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    password = Column(String,nullable=False)
    
    organization_id = Column(Integer,ForeignKey("organization.id"))
    organization = relationship("Organization", back_populates="users")
    
    user_roles = relationship("UserRole",back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    
    users = relationship("UserRole",back_populates="roles")
    

class UserRole(Base):
    __tablename__ = "user_role"
    id = Column(Integer,primary_key=True,index=True)

    role_id = Column(Integer,ForeignKey("roles.id"),nullable=False)   
    roles = relationship("Role",back_populates="users")

    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    users = relationship("User",back_populates="user_roles")
    
           
    



