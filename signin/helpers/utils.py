from argon2 import PasswordHasher

from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from helpers.config import EXPIRE_TIME,SECRET_KEY
pwd_hash=PasswordHasher()

def hash_pwd(password:str):
    return pwd_hash.hash(password)
def verify_pwd(hash_password:str,password:str):
    return pwd_hash.verify(hash_password,password)

def create_token(data:dict):
    payload=data.copy()
    expire_time=datetime.now(timezone.utc) + timedelta(minutes=int(EXPIRE_TIME))
    payload.update({"exp":expire_time,
                    "iat":datetime.now(timezone.utc)})
    return jwt.encode(payload,SECRET_KEY,algorithm='HS256')
def decode_token(token:str):

    try:
        payload:dict=jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        if payload :return payload
    except JWTError as e :
        print("Faild token decoding")
        return False
    
   
if __name__ =='__main__':
    hash=hash_pwd('1234')
    print(hash)
    print(verify_pwd(hash,'1234'))
    token=create_token({"sub":'m.lahmer@esisa.ac.ma'})+'1'
    print(decode_token(token))
    

    