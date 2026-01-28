from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException,Security,Request,Response
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from helpers.config import session_factory
from dal.user_dao import get_all_users,create_user,authenticate
from dto.users_dto import UserResponse,UserRequest,TokenResponse,TokenRequest
from entities.user import User
from helpers.utils import create_token,decode_token
from helpers.config import logger
from dal.black_listed_dao import add_token_to_blacklist,is_blacklist_token
router=APIRouter(prefix="/users",tags=["users"])  
http_bearer=HTTPBearer()

def check_token(session=Depends(session_factory),token:HTTPAuthorizationCredentials=Security(http_bearer)):
    credentials=token.credentials
    payload=decode_token(credentials)
    if is_blacklist_token(session,credentials):
        raise HTTPException(status_code=401,detail='Token is blacklisted')
    if not payload :
        raise HTTPException(status_code=404,detail='Invalid token')
    return payload

@router.get("/",response_model=list[UserResponse])
def get_all(session=Depends(session_factory),
            payload=Depends(check_token)
            ):
    
    
    users:list[User]=get_all_users(session)
    results:list[UserResponse]=[]
    for user in users:
        results.append(UserResponse(
            email=str(user.email),
            is_admin=bool(user.is_admin),
            created_at=str(user.created_at),
            updated_at=str(user.updated_at)
        ))
    logger.info('get all users from ip :')
    return results
@router.post("/add",response_model=UserResponse)
def register_user(userRequest:UserRequest,session=Depends(session_factory)):
    user_entity=User(
        email=userRequest.email,
        password=userRequest.password
    )
    add_ok=create_user(session,user_entity)
    if add_ok :
        logger.info('user register ok %s',userRequest.email)
        return UserResponse(
            email=str(user_entity.email),
            is_admin=bool(user_entity.is_admin),
            created_at=str(user_entity.created_at),
            updated_at=str(user_entity.updated_at)
        )
        
    logger.error('registration faild for user %s',userRequest.email)
    raise HTTPException(status_code=401,detail="registration faild")

@router.post("/auth",response_model=TokenResponse)
def authenticate_user(userRequest:UserRequest,
                        session=Depends(session_factory),
                        ):
    user_entity=User(
        email=userRequest.email,
        password=userRequest.password
    )
    auth_user=authenticate(session,user_entity)
    if auth_user != False :
        claims:dict={
                "sub":auth_user.email,
                "role":auth_user.is_admin
        }
        token=create_token(claims)
        logger.info('Authetication for user ; %s',userRequest.email)
        return TokenResponse(token=token,
                             payload=claims)
    logger.error('Authentication faild fro user : %s',userRequest.email)
    raise HTTPException(status_code=401,detail="Authentication faild")
@router.post("/verify-token",response_model=TokenResponse)
def verify_token(tokenRequest:TokenRequest):
    payload=decode_token(token=tokenRequest.token)
    if not payload :
        raise HTTPException(status_code=404,detail="Invalid token")
    return TokenResponse(token=tokenRequest.token,payload=payload)

@router.post("/logout")
def logout_user(token:HTTPAuthorizationCredentials=Security(http_bearer),
                session=Depends(session_factory)
                ):
    credentials=token.credentials
    
    add_ok=add_token_to_blacklist(session,credentials)
    if add_ok :
        logger.info('user logged out')
        return Response(status_code=200,content="logout successful")
    logger.error('logout faild')
    raise HTTPException(status_code=500,detail="logout faild")