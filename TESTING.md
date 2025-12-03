# Testing Guide - Physical AI & Humanoid Robotics Textbook

## 🧪 Complete Testing Instructions

This guide walks you through testing all features of the project.

## Prerequisites

Before testing, ensure you have:
- ✅ Node.js 18+ installed
- ✅ Python 3.10+ installed
- ✅ API keys configured (see Setup section)

## 📋 Quick Setup for Testing

### 1. Install Dependencies

**Frontend:**
```bash
cd d:\Projects\Testing\physical-ai-textbook
npm install
```

**Backend:**
```bash
cd d:\Projects\Testing\physical-ai-textbook\backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `backend/.env` file:

```env
# Required for testing
OPENAI_API_KEY=sk-your-key-here
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
DATABASE_URL=postgresql://user:password@host/database
AUTH_SECRET=your-secret-key-here
FRONTEND_URL=http://localhost:3000
```

**How to get these:**

1. **OpenAI API Key**: 
   - Go to https://platform.openai.com/api-keys
   - Create new secret key
   - Copy and paste into `.env`

2. **Qdrant** (Free Tier):
   - Go to https://cloud.qdrant.io
   - Sign up and create a cluster
   - Copy cluster URL and API key

3. **Neon Database** (Free Tier):
   - Go to https://neon.tech
   - Create a project
   - Copy connection string

4. **Auth Secret**:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### 3. Initialize Database

```bash
cd backend
python -c "from database import init_db; init_db()"
```

This creates the necessary tables (users, chat_history, content_personalization).

### 4. Ingest Content into Qdrant

```bash
cd backend
python ingest_content.py
```

This will:
- Read all markdown files from `docs/`
- Split them into chunks
- Generate embeddings
- Store in Qdrant

Expected output:
```
Found 5 markdown files
Processing: intro.md
Processing: module1/ros2-fundamentals.md
...
Total chunks created: 87
Ingesting into Qdrant...
✅ Ingestion complete!
```

## 🚀 Running the Application

### Terminal 1: Start Backend

```bash
cd d:\Projects\Testing\physical-ai-textbook\backend
python main.py
```

Expected output:
```
✅ Database and Qdrant initialized
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start Frontend

```bash
cd d:\Projects\Testing\physical-ai-textbook
npm start
```

Expected output:
```
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

## 🧪 Testing Checklist

### ✅ 1. Test Homepage

1. Open http://localhost:3000
2. **Verify:**
   - ✅ Title: "Physical AI & Humanoid Robotics"
   - ✅ Tagline: "Master the Future of Embodied Intelligence"
   - ✅ 6 feature cards displayed
   - ✅ "Start Learning 🚀" button works
   - ✅ Gradient background visible

### ✅ 2. Test Textbook Content

1. Click "Start Learning" or navigate to `/docs/intro`
2. **Verify:**
   - ✅ Introduction page loads
   - ✅ Sidebar shows all modules
   - ✅ Module 1: ROS 2 content accessible
   - ✅ Module 2: Simulation content accessible
   - ✅ Module 3: NVIDIA Isaac content accessible
   - ✅ Module 4: VLA content accessible
   - ✅ Code blocks are syntax-highlighted
   - ✅ Navigation between pages works

### ✅ 3. Test RAG Chatbot

1. **Open Chatbot:**
   - Click the 💬 floating button (bottom-right)
   - ✅ Chat window opens with glassmorphism effect

2. **Test Basic Questions:**
   ```
   Question: "What is ROS 2?"
   Expected: Answer about Robot Operating System 2
   ```
   
   ```
   Question: "How does Gazebo work?"
   Expected: Answer about physics simulation
   ```
   
   ```
   Question: "Explain NVIDIA Isaac"
   Expected: Answer about Isaac platform
   ```

3. **Test Selected Text Feature:**
   - Go to any module page
   - Select/highlight a paragraph of text
   - Open chatbot
   - Ask: "Explain this in simple terms"
   - ✅ Answer should be specific to selected text

4. **Verify:**
   - ✅ Responses appear within 3-5 seconds
   - ✅ Sources are shown below answers
   - ✅ Chat history persists during session
   - ✅ Loading animation shows while waiting

### ✅ 4. Test Authentication

#### Signup Flow

1. Navigate to http://localhost:3000/signup (you may need to create this page or use the component directly)
2. Fill in form:
   - Name: "Test User"
   - Email: "test@example.com"
   - Password: "password123"
   - Software Experience: "Intermediate"
   - Hardware Experience: "Beginner"
3. Click "Sign Up"
4. **Verify:**
   - ✅ Success message appears
   - ✅ Redirected to homepage
   - ✅ User badge shows "Logged in" in chatbot

#### Login Flow

1. Logout (if logged in)
2. Navigate to login page
3. Enter credentials:
   - Email: "test@example.com"
   - Password: "password123"
4. Click "Sign In"
5. **Verify:**
   - ✅ Login successful
   - ✅ User state persists on page refresh

#### Test API Directly

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test2@example.com",
    "name": "Test User 2",
    "password": "password123",
    "software_experience": "advanced",
    "hardware_experience": "intermediate"
  }'

# Expected response:
# {"message": "User created successfully", "token": "...", "user": {...}}

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test2@example.com",
    "password": "password123"
  }'
```

### ✅ 5. Test Content Personalization

**Note:** You need to integrate the ContentActions component into your doc pages first.

1. **Login** with a user account
2. Go to any module page (e.g., Module 1)
3. Click "✨ Personalize for Me" button
4. **Verify:**
   - ✅ Loading bar appears
   - ✅ Personalized content displays
   - ✅ Content is adapted to user's experience level
   - ✅ Badge shows "Personalized for your experience level"

**Test Different Experience Levels:**

Create users with different profiles:
- Beginner/Beginner: Should get more detailed explanations
- Advanced/Advanced: Should get concise, technical content

### ✅ 6. Test Urdu Translation

1. Go to any module page
2. Click "🌐 اردو میں (Urdu)" button
3. **Verify:**
   - ✅ Loading bar appears
   - ✅ Content translates to Urdu
   - ✅ Text direction changes to RTL (right-to-left)
   - ✅ Technical terms remain in English
   - ✅ Badge shows "Urdu Translation"

### ✅ 7. Test Backend API Endpoints

#### Health Check
```bash
curl http://localhost:8000/
# Expected: {"message": "Physical AI Textbook API", "status": "running", "version": "1.0.0"}
```

#### Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is ROS 2?",
    "session_id": "test-session"
  }'

# Expected: {"answer": "...", "sources": [...], "session_id": "test-session"}
```

#### Personalize Endpoint (requires auth)
```bash
# First login to get token
TOKEN="your-jwt-token-here"

curl -X POST http://localhost:8000/api/personalize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "content": "ROS 2 is a middleware for robotics...",
    "page_path": "/docs/module1/ros2"
  }'
```

#### Translate Endpoint
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "content": "ROS 2 is the Robot Operating System version 2."
  }'

# Expected: {"translated_content": "ROS 2 روبوٹ آپریٹنگ سسٹم ورژن 2 ہے۔"}
```

## 🐛 Troubleshooting

### Issue: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: Database connection error

**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution:**
- Check your `DATABASE_URL` in `.env`
- Ensure Neon database is running
- Test connection: `psql "your-database-url"`

### Issue: Qdrant connection error

**Error:** `qdrant_client.http.exceptions.UnexpectedResponse`

**Solution:**
- Verify `QDRANT_URL` and `QDRANT_API_KEY`
- Check Qdrant cluster status at cloud.qdrant.io
- Ensure collection is created: `python -c "from qdrant_service import qdrant_service; qdrant_service.create_collection()"`

### Issue: OpenAI API error

**Error:** `openai.error.AuthenticationError: Incorrect API key`

**Solution:**
- Verify your OpenAI API key
- Check you have credits: https://platform.openai.com/usage
- Ensure key is correctly set in `.env`

### Issue: Chatbot not appearing

**Solution:**
- Check browser console for errors (F12)
- Verify `Root.tsx` is wrapping the app
- Check if `Chatbot` component is imported correctly

### Issue: CORS errors

**Error:** `Access-Control-Allow-Origin` error in browser

**Solution:**
- Ensure backend is running on port 8000
- Check `FRONTEND_URL` in backend `.env`
- Verify CORS middleware in `main.py`

## 📊 Performance Testing

### Test Response Times

```bash
# Install httpie for better testing
pip install httpie

# Test chat endpoint
time http POST http://localhost:8000/api/chat question="What is ROS 2?"

# Expected: < 3 seconds
```

### Test Concurrent Requests

```bash
# Install Apache Bench
# Windows: Download from Apache website
# Linux: sudo apt-get install apache2-utils

# Test 100 requests, 10 concurrent
ab -n 100 -c 10 -p question.json -T application/json http://localhost:8000/api/chat
```

## ✅ Final Verification Checklist

Before submitting:

- [ ] All 4 modules load correctly
- [ ] Chatbot responds to questions
- [ ] Selected text queries work
- [ ] Signup/Login functional
- [ ] Content personalization works
- [ ] Urdu translation works
- [ ] No console errors in browser
- [ ] Backend API responds correctly
- [ ] Database stores user data
- [ ] Qdrant returns relevant results
- [ ] GitHub Pages deployment configured
- [ ] README.md is complete
- [ ] All environment variables documented

## 🎥 Creating Demo Video

For hackathon submission (< 90 seconds):

1. **Show Homepage** (5 sec)
   - Highlight features

2. **Navigate Textbook** (10 sec)
   - Show all 4 modules

3. **Demo Chatbot** (20 sec)
   - Ask a question
   - Show selected text query

4. **Demo Auth** (15 sec)
   - Quick signup/login

5. **Demo Personalization** (20 sec)
   - Click personalize button
   - Show adapted content

6. **Demo Translation** (15 sec)
   - Click Urdu button
   - Show translated content

7. **Closing** (5 sec)
   - Show GitHub repo

## 📝 Test Results Template

```
# Test Results - Physical AI Textbook

Date: [DATE]
Tester: [NAME]

## Frontend Tests
- [ ] Homepage loads: PASS/FAIL
- [ ] All modules accessible: PASS/FAIL
- [ ] Navigation works: PASS/FAIL

## Chatbot Tests
- [ ] Basic questions: PASS/FAIL
- [ ] Selected text queries: PASS/FAIL
- [ ] Sources displayed: PASS/FAIL

## Auth Tests
- [ ] Signup: PASS/FAIL
- [ ] Login: PASS/FAIL
- [ ] Token persistence: PASS/FAIL

## Advanced Features
- [ ] Personalization: PASS/FAIL
- [ ] Translation: PASS/FAIL

## Performance
- [ ] Response time < 3s: PASS/FAIL
- [ ] No console errors: PASS/FAIL

Notes:
[Any issues or observations]
```

---

**Ready to test and win! 🚀**
