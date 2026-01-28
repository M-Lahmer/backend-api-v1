import socketio
from app.core.config import SOCKETIO_CORS

# Async Server (ASGI)
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=SOCKETIO_CORS
)

# Optionally you can register connect/disconnect handlers here
@sio.event
async def connect(sid, environ):
    print("Socket.IO - client connected:", sid)

@sio.event
async def disconnect(sid):
    print("Socket.IO - client disconnected:", sid)
