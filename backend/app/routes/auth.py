from fastapi import APIRouter, HTTPException, status, Depends, Form
from ..auth import get_password_hash, _fake_users_db, create_access_token, verify_password
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@router.post('/register')
async def register(user: UserCreate):
    if user.email in _fake_users_db:
        raise HTTPException(status_code=400, detail='User already exists')
    hashed = get_password_hash(user.password)
    _fake_users_db[user.email] = {'email': user.email, 'password': hashed}
    return {'msg':'registered'}

@router.post('/token')
async def token(email: EmailStr = Form(...), password: str = Form(...)):
    user = _fake_users_db.get(email)
    if not user or not verify_password(password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    access = create_access_token({'sub': email})
    return {'access_token': access, 'token_type': 'bearer'}
