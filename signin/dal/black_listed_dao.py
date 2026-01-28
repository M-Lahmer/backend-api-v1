from entities.user import *
from sqlalchemy.orm import Session
def is_blacklist_token(session:Session, token:str):
    filtred_token= session.query(BlacklistToken).filter(BlacklistToken.token == token).one_or_none()
    if filtred_token:
        return True
    return False
def add_token_to_blacklist(session:Session, token:str):
    blacklisted_token= BlacklistToken(token=token)
    session.add(blacklisted_token)
    try:
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
