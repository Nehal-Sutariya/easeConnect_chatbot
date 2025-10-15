from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, messages, websocket
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsEase - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(messages.router, prefix="/api/messages")
app.include_router(websocket.router, prefix="/api/ws")

@app.get("/")
async def root():
    return {"status":"ok", "service":"WhatsEase backend"}
