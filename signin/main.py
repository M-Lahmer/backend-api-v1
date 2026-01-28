import uvicorn

from fastapi import FastAPI
from controllers.auth_controller import router
from helpers.config import Base,engine
app=FastAPI(
title="Authentication app",
description="Micro service signing app "
)
#create one time
Base.metadata.create_all(bind=engine)
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run("main:app",host="0.0.0.0",reload=True)