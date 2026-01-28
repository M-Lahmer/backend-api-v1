
from typing import Final
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import logging
import os
#environement variables
EXPIRE_TIME:Final[str]=os.getenv("EXPIRE_TIME","30")
SECRET_KEY:Final[str]=os.getenv("SECRET_KEY","$argon2id$v=19$m=65536,t=3,p=4$hT18aCPZ5AFxQ2ncYkRkWg$5UvBttA1brZmn6Bmf1T0NgKaYaqUzMV1pvWNxDp5pFc")
USER_DB:Final[str]=os.getenv('USER_DB','admin')
PASSWORD_DB:Final[str]=os.getenv('PASSWORD_DB','1234')
NAME_DB:Final[str]=os.getenv('NAME_DB','db_auth')
SERVER_DB:Final[str]=os.getenv('SERVER_DB','localhost')
URL_DB:Final[str]='postgresql+psycopg2://'+USER_DB+':'+PASSWORD_DB+'@'+SERVER_DB+':5432/'+NAME_DB
#sqlalchemy
engine=create_engine(URL_DB,pool_size=10)
LocalSession=sessionmaker(bind=engine)
Base=declarative_base()
def session_factory():
    session=LocalSession()
    try:
        yield session
    finally:
        session.close()
#logs
formater=logging.Formatter(fmt='%(asctime)s-%(levelname)s-%(message)s')
handler=logging.FileHandler('./logs/auth.log')
handler.setFormatter(formater)
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
