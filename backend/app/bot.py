# very simple intent-response bot (rule-based)
import asyncio
from .db import db
from datetime import datetime
import uuid, logging

logger = logging.getLogger(__name__)

INTENTS = {
    'hello': ['hi','hello','hey'],
    'hours': ['hours','open','close','time'],
    'help': ['help','support','assist'],
}

RESPONSES = {
    'hello': 'Hello! I am WhatsEase bot. How can I help you today?',
    'hours': 'We are available 24/7 in chat — how can I assist?',
    'help': 'You can ask about hours, account, or say hello.',
    'fallback': 'Sorry, I did not understand. Can you rephrase?'
}

async def handle_bot_reply(msg):
    text = msg.get('content','').lower()
    intent = None
    for k, tokens in INTENTS.items():
        for t in tokens:
            if t in text:
                intent = k
                break
        if intent:
            break
    response = RESPONSES.get(intent,'fallback')
    bot_msg = {
        'message_id': str(uuid.uuid4()),
        'sender': 'bot@whasease.local',
        'recipient': msg['sender'],
        'content': response,
        'timestamp': datetime.utcnow(),
        'status': 'Sent',
        'is_bot_response': True
    }
    await asyncio.sleep(0.5)  # simulate thinking
    await db.messages.insert_one(bot_msg)
    logger.info(f"bot replied to {msg['sender']}")
