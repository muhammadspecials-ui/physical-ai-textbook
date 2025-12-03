# Physical AI & Humanoid Robotics Textbook

An AI-native textbook for learning Physical AI and Humanoid Robotics with integrated RAG chatbot, authentication, and content personalization.

## 🚀 Features

- ✅ **Comprehensive Textbook**: 4 modules covering ROS 2, Gazebo/Unity, NVIDIA Isaac, and VLA
- ✅ **RAG Chatbot**: AI assistant powered by OpenAI and Qdrant vector database
- ✅ **User Authentication**: Signup/Login with user profiling (Better Auth)
- ✅ **Content Personalization**: Adapt content based on user experience level
- ✅ **Urdu Translation**: Translate content to Urdu on demand
- ✅ **Modern UI**: Glassmorphism design with smooth animations

## 📚 Course Modules

1. **Module 1**: The Robotic Nervous System (ROS 2)
2. **Module 2**: The Digital Twin (Gazebo & Unity)
3. **Module 3**: The AI-Robot Brain (NVIDIA Isaac™)
4. **Module 4**: Vision-Language-Action (VLA)

## 🛠️ Tech Stack

### Frontend
- **Docusaurus** - Static site generator
- **React** - UI components
- **TypeScript** - Type safety
- **Axios** - API client

### Backend
- **FastAPI** - Python web framework
- **OpenAI** - LLM for RAG and personalization
- **Qdrant** - Vector database for RAG
- **Neon** - Serverless Postgres database
- **Better Auth** - Authentication system

## 📦 Installation

### Prerequisites
- Node.js 18+
- Python 3.10+
- OpenAI API key
- Qdrant Cloud account (free tier)
- Neon Database account (free tier)

### Frontend Setup

```bash
cd physical-ai-textbook
npm install
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file in `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=postgresql://user:password@host/database
AUTH_SECRET=your_secret_key
FRONTEND_URL=http://localhost:3000
```

## 🚀 Running the Application

### Start Backend

```bash
cd backend
python main.py
```

Backend runs on `http://localhost:8000`

### Start Frontend

```bash
npm start
```

Frontend runs on `http://localhost:3000`

## 📖 Ingesting Content

To populate the RAG chatbot with textbook content:

```bash
python backend/ingest_content.py
```

This will:
1. Read all markdown files from `docs/`
2. Chunk the content
3. Generate embeddings
4. Store in Qdrant

## 🎯 Usage

### Chatbot
- Click the floating chat button (💬) in the bottom-right
- Ask questions about the textbook content
- Select text on the page and ask questions about it

### Authentication
- Navigate to `/signup` to create an account
- Provide your software and hardware experience level
- Login at `/login`

### Content Personalization
- Login first
- Click "Personalize for Me" button at the top of any chapter
- Content will be adapted to your experience level

### Translation
- Click "اردو میں (Urdu)" button at the top of any chapter
- Content will be translated to Urdu

## 🏗️ Project Structure

```
physical-ai-textbook/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # Database models
│   ├── auth_service.py      # Authentication
│   ├── rag_service.py       # RAG logic
│   ├── qdrant_service.py    # Vector DB
│   └── requirements.txt     # Python dependencies
├── docs/
│   ├── intro.md             # Introduction
│   ├── module1/             # ROS 2 content
│   ├── module2/             # Simulation content
│   ├── module3/             # NVIDIA Isaac content
│   └── module4/             # VLA content
├── src/
│   ├── components/
│   │   ├── Chatbot/         # Chat component
│   │   ├── Auth/            # Auth forms
│   │   └── ContentActions/  # Personalization
│   ├── contexts/
│   │   └── AuthContext.tsx  # Auth state
│   └── utils/
│       └── api.ts           # API client
└── docusaurus.config.ts     # Docusaurus config
```

## 🎨 Customization

### Styling
- Edit `src/css/custom.css` for global styles
- Component styles are in `.module.css` files

### Content
- Add new chapters in `docs/` directory
- Update `sidebars.ts` for navigation

## 🚢 Deployment

### GitHub Pages

1. Update `docusaurus.config.ts`:
```typescript
url: 'https://yourusername.github.io',
baseUrl: '/physical-ai-textbook/',
organizationName: 'yourusername',
projectName: 'physical-ai-textbook',
```

2. Deploy:
```bash
npm run build
npm run deploy
```

### Backend Deployment
Deploy backend to:
- **Vercel** (recommended for FastAPI)
- **Railway**
- **Render**
- **AWS Lambda**

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact

For questions or support, please open an issue.

---

Built with ❤️ for the Physical AI community
