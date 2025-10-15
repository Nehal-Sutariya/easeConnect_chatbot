easeConnect_chatbot

On vercel:  https://ease-connect-chatbot.vercel.app/

Contents:
- backend/: FastAPI app using MongoDB (motor)
- frontend/: Minimal React app (no UI libraries)

Run backend:
1. Install Python dependencies: pip install -r backend/requirements.txt
2. Copy backend/.env.example to backend/.env and set MONGODB_URI and JWT_SECRET
3. Run: uvicorn app.main:app --reload --port 8000


