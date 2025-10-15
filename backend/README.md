WhatsEase Backend (FastAPI + MongoDB)

Setup:
1. Install dependencies: pip install -r requirements.txt
2. Copy .env.example to .env and set values (MONGODB_URI, JWT_SECRET)
3. Run: uvicorn app.main:app --reload --port 8000

Notes:
- Uses an in-memory user store for demo. Replace with a users collection for production.
- WebSocket endpoint: /api/ws/ws/{email}
