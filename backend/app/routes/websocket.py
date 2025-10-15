from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
router = APIRouter()
logger = logging.getLogger(__name__)

connections = {}  # email -> websocket

@router.websocket('/ws/{email}')
async def ws_endpoint(websocket: WebSocket, email: str):
    await websocket.accept()
    connections[email] = websocket
    logger.info(f"ws connected: {email}")
    try:
        while True:
            data = await websocket.receive_json()
            # Expecting {"type":"send","message": {...}}
            if data.get('type') == 'send':
                # broadcast to recipient if connected
                msg = data.get('message')
                recipient = msg.get('recipient')
                if recipient in connections:
                    await connections[recipient].send_json({'type':'message','message':msg})
                # echo back status
                await websocket.send_json({'type':'ack','message_id': msg.get('message_id')})
    except WebSocketDisconnect:
        logger.info(f"ws disconnected: {email}")
        connections.pop(email, None)
