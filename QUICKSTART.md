# 🚀 Quick Setup & Testing Guide

## ✅ Your Credentials Are Configured!

I've set up your Qdrant and Neon credentials. You just need to add your **OpenAI API key**.

## 📝 Step 1: Add OpenAI API Key

Edit `backend/.env` and replace this line:
```
OPENAI_API_KEY=your_openai_api_key_here
```

With your actual key from https://platform.openai.com/api-keys

## 🧪 Step 2: Test Backend Setup

```bash
cd d:\Projects\Testing\physical-ai-textbook\backend
python test_setup.py
```

This will test:
- ✅ Qdrant connection
- ✅ Neon database connection
- ✅ OpenAI API (once you add the key)

## 🗄️ Step 3: Initialize Database

```bash
python -c "from database import init_db; init_db()"
```

## 📚 Step 4: Ingest Content into Qdrant

```bash
python ingest_content.py
```

This will:
- Read all textbook content
- Create embeddings
- Store in Qdrant

## 🚀 Step 5: Run the Application

**Terminal 1 - Backend:**
```bash
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd ..
npm start
```

## 🧪 Step 6: Test Features

### Test Chatbot
1. Open http://localhost:3000
2. Click 💬 button
3. Ask: "What is ROS 2?"

### Test Auth
1. Go to http://localhost:3000/signup
2. Create account
3. Login at http://localhost:3000/login

### Test Personalization
1. Login first
2. Go to any module
3. Click "✨ Personalize for Me"

### Test Translation
1. Go to any module
2. Click "🌐 اردو میں (Urdu)"

## 🎯 Quick Test Commands

```bash
# Test Qdrant connection
python -c "from qdrant_service import qdrant_service; qdrant_service.create_collection(); print('✅ Qdrant working!')"

# Test Database
python -c "from database import init_db, SessionLocal; init_db(); db = SessionLocal(); print('✅ Database working!'); db.close()"

# Test API endpoint
curl http://localhost:8000/
```

## ⚠️ Important Notes

1. **OpenAI API Key Required** - Get from platform.openai.com
2. **Qdrant & Neon** - Already configured! ✅
3. **Port 8000** - Backend runs here
4. **Port 3000** - Frontend runs here

## 🐛 Troubleshooting

### If Qdrant fails:
- Check the URL has `:6333` port
- Verify API key is correct

### If Database fails:
- Check connection string
- Ensure `sslmode=require` is included

### If OpenAI fails:
- Add your API key to `.env`
- Check you have credits

---

**Everything is ready! Just add your OpenAI API key and run the tests!** 🚀
