from fastapi import APIRouter, Depends, HTTPException
from ..auth import get_current_user
from ..db import db
from ..models import Message, Status
from datetime import datetime
import uuid, logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/')
async def create_message(payload: Message, user: dict = Depends(get_current_user)):
    msg = payload.dict(by_alias=True)
    msg['message_id'] = msg.get('message_id') or str(uuid.uuid4())
    msg['timestamp'] = msg.get('timestamp') or datetime.utcnow()
    await db.messages.insert_one(msg)
    logger.info(f"message sent: {msg['message_id']} by {msg['sender']}")
    # simplistic bot: if recipient is bot@whasease.local trigger bot reply
    if msg['recipient'] == 'bot@whasease.local':
        from ..bot import handle_bot_reply
        await handle_bot_reply(msg)
    return {'status':'ok','message_id': msg['message_id']}

@router.get('/')
async def list_messages(user: dict = Depends(get_current_user)):
    docs = db.messages.find({'$or':[{'sender':user['email']},{'recipient':user['email']}]})
    res = []
    async for d in docs:
        d['id'] = str(d.get('_id'))
        res.append(d)
    return res

@router.get('/{message_id}')
async def get_message(message_id: str, user: dict = Depends(get_current_user)):
    doc = await db.messages.find_one({'message_id':message_id})
    if not doc:
        raise HTTPException(status_code=404, detail='not found')
    return doc

@router.put('/{message_id}')
async def update_message(message_id: str, payload: dict, user: dict = Depends(get_current_user)):
    update = {}
    if 'status' in payload:
        update['status'] = payload['status']
    if 'content' in payload:
        update['content'] = payload['content']
    if not update:
        raise HTTPException(status_code=400, detail='nothing to update')
    await db.messages.update_one({'message_id':message_id}, {'$set': update})
    logger.info(f"message updated {message_id}: {update}")
    return {'status':'ok'}
