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

5. Open the interactive docs
- http://localhost:8000/docs

---

## 🔌 API Endpoints

| Method | Endpoint | Auth Required | Purpose |
|---|---|---|---|
| GET | `/` | No | Confirms API is running |
| POST | `/register` | No | Create a new account |
| POST | `/login` | No | Get a JWT token |
| POST | `/chat` | ✅ Yes | Send message, get AI reply |
| GET | `/history` | ✅ Yes | View your conversation history |
| DELETE | `/history` | ✅ Yes | Clear your conversation history |
| GET | `/me` | ✅ Yes | View your username |

---

## 📚 What I Learned

- The difference between authentication and authorization
- How JWT tokens work (header, payload, signature)
- Why passwords must be hashed, never stored as plain text
- How FastAPI's `Depends()` system protects routes
- How OAuth2PasswordBearer integrates with Swagger docs
- How to give each user their own isolated data

---

## 🗺️ What's Next

- 🔜 Connect a Frontend to this Backend (Day 19)
- 🔜 Rate Limiting + Usage Tracking (Day 20)
- 🔜 Deploy Full Stack App (Day 21)

---

## 👨‍💻 About Me

I am Prashik — an aspiring AI Engineer on a 4-month intensive
journey to become job-ready in Generative AI Engineering.

Follow my journey on [LinkedIn](https://www.linkedin.com/in/prashik-sawant-ds/)

---

*Started: June 18, 2026 | Status: ✅ Complete*
