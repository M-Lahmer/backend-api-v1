"""from fastapi import FastAPI
from api.monitoring_api import router as monitoring_router
from api.health import router as health_router
from messanging.rabbitmq_consumer import start_consumer_thread
from core.socket import sio

import socketio

app = FastAPI(title="Monitoring Microservice")

app.include_router(health_router)
app.include_router(monitoring_router)

# Socket.IO ASGI
socket_app = socketio.ASGIApp(sio, app)

@app.on_event("startup")
def startup():
    start_consumer_thread()
"""


from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.monitoring_api import router as monitoring_router
from app.messanging.rabbitmq_consumer import start_consumer_thread
from app.core.socket import sio

import socketio

app = FastAPI(title="Monitoring Microservice")

# include routers
app.include_router(health_router)
app.include_router(monitoring_router)

# wrap FastAPI app with Socket.IO ASGI
socket_app = socketio.ASGIApp(sio, app)

@app.on_event("startup")
def startup_event():
    # démarre le consumer RabbitMQ dans un thread daemon
    start_consumer_thread()
