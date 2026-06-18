# 🔐 AI Chatbot API with JWT Authentication

> Added real security to my backend. Now only logged-in users 
> can access the chatbot — and everyone gets their own private 
> conversation history.
> Day 18 of my 4-month AI Engineering journey.

---

## 🌱 Why I Built This

Day 17's API was wide open — anyone could call `/chat` and use 
my AI without any restriction. That's not how real products work.

Day 18 was about locking the doors and handing out keys only to 
people who prove who they are.

---

## 💭 Thought Process

I needed:
- A way for users to create an account (register)
- A way to prove who they are (login)
- A way to stay "logged in" without re-sending passwords (JWT)
- A way to block anyone without a valid token (protected routes)
- Separate chat history per user (no more shared memory)

---

## 🛠️ What This Project Does

A secured REST API that:
- Lets users register with a hashed password (never stored as plain text)
- Issues a JWT token on successful login
- Requires that token for every chat-related action
- Keeps each user's conversation history completely separate
- Rejects any request without a valid token (401 Unauthorized)

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| FastAPI | REST API framework |
| python-jose | JWT creation and verification |
| passlib + bcrypt | Secure password hashing |
| Groq API (LLaMA 3.3 70B) | AI response generation |
| python-dotenv | Environment variable management |

---

## 🚀 How to Run Locally

1. Clone the repository
- git clone https://github.com/PrashikSawant/day18-jwt-auth.git
- cd day18-jwt-auth

2. Install dependencies

- pip install -r requirements.txt

3. Create a `.env` file

- GROQ_API_KEY=your_groq_api_key_here
- SECRET_KEY=your_random_secret_key_here

4. Run the server

- uvicorn main:app --reload

