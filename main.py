import os
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from typing import List, Dict

from auth import hash_password, verify_password, create_access_token, decode_access_token

# ── Setup ──────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(
    title="AI Chatbot API with Auth",
    description="A secured REST API with JWT authentication",
    version="2.0.0"
)

# ── Fake in-memory user database (Day 18 — simple, no real DB yet) ──
fake_users_db: Dict[str, dict] = {}

# ── Per-user chat history ────────────────────────────────────
user_chat_history: Dict[str, List[Dict[str, str]]] = {}

# ── Tells FastAPI where to find the token (used by Depends) ──
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ── Pydantic Models ───────────────────────────────────────────
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str


# ── Dependency: Get current logged-in user from token ────────
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    This function runs automatically on any route that uses
    Depends(get_current_user). It checks the token and returns
    the username, or rejects the request.
    """
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ── Routes ────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "AI Chatbot API with Auth is running. Visit /docs"}


@app.post("/register")
def register(user: UserRegister):
    """Creates a new user account with a hashed password"""
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hash_password(user.password)
    }
    user_chat_history[user.username] = []

    return {"message": f"User '{user.username}' registered successfully"}


@app.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Verifies credentials and returns a JWT token"""
    stored_user = fake_users_db.get(form_data.username)

    if not stored_user or not verify_password(form_data.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(data={"sub": form_data.username})
    return TokenResponse(access_token=token)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, current_user: str = Depends(get_current_user)):
    """
    Protected route — requires a valid JWT token.
    Only logged-in users can chat.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    history = user_chat_history[current_user]
    history.append({"role": "user", "content": request.message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history[-10:],
            max_tokens=1024,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@app.get("/history")
def get_history(current_user: str = Depends(get_current_user)):
    """Protected route — returns only the logged-in user's history"""
    return {"username": current_user, "history": user_chat_history[current_user]}


@app.delete("/history")
def clear_history(current_user: str = Depends(get_current_user)):
    """Protected route — clears only the logged-in user's history"""
    user_chat_history[current_user].clear()
    return {"message": "Chat history cleared successfully"}


@app.get("/me")
def get_my_profile(current_user: str = Depends(get_current_user)):
    """Returns the currently logged-in username"""
    return {"username": current_user}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)