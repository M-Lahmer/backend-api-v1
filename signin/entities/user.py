
from helpers.config import Base
from sqlalchemy import Column, String,Integer,DateTime,func,Boolean

class User(Base):
    __tablename__='t_users'
    id=Column(Integer, primary_key=True,autoincrement=True,nullable=False,index=True)
    email=Column(String,unique=True,index=True,nullable=False)
    password=Column(String(128),nullable=False)
    is_admin=Column(Boolean,default=False)
    created_at=Column(DateTime,server_default=func.now())
    updated_at=Column(DateTime,server_default=func.now(),server_onupdate=func.now())
class BlacklistToken(Base):
    __tablename__='t_blacklist_tokens'
    id=Column(Integer, primary_key=True,autoincrement=True,nullable=False,index=True)
    token=Column(String(500),unique=True,nullable=False)
    blacklisted_on=Column(DateTime,server_default=func.now())