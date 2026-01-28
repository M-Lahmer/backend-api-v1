
from typing import Optional
from entities.user import User
from sqlalchemy.orm import Session

def create_user(session:Session,user:User):
    # Fix: correct filter syntax
    filtred_user=session.query(User).filter(User.email == user.email).one_or_none()
    if filtred_user != None :
        return False
    session.add(user)
    try :
        session.commit()
        session.refresh(user)
        return True
    except Exception as e:
        session.rollback()   
        return False
def get_all_users(session:Session):
    return session.query(User).all()

def authenticate(session:Session,user:User):
    filtred_user:User=session.query(User).filter(
        User.email==user.email,User.password==user.password
        ).one_or_none()
    if filtred_user:
        return filtred_user
    return False