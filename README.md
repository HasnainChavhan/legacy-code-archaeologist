# Legacy Code Archaeologist

A GenAI-powered developer tool that explains, visualizes, and debugs old codebases using Gemini 1.5 Pro.

## 🎯 Project Overview

Legacy Code Archaeologist transforms static codebases into interactive knowledge graphs. Unlike standard coding assistants that only see the "current file," this solution leverages Gemini 1.5 Pro's massive 2M token context window to ingest entire repositories at once.

### Key Features

- **Generative Visualization**: Automatically generates real-time architectural diagrams (Mermaid.js) that visualize dependencies and data flow
- **Semantic Excavation**: Ask high-level questions like "Where is the race condition in the payment module?" and get precise answers with code citations
- **Interactive Chat**: Natural language interface to explore codebases
- **Beautiful UI**: Modern dark theme with glassmorphism effects and smooth animations

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI for high-performance API
- **GitHub Integration**: PyGithub for repository fetching
- **AI Model**: Gemini 1.5 Pro via Google Generative AI SDK
- **Context Stuffing**: Entire codebases loaded into Gemini's 2M token context window

### Frontend (Next.js/React)
- **Framework**: Next.js 14 with App Router
- **UI Library**: Shadcn/UI for premium components
- **Visualization**: Mermaid.js for interactive diagrams
- **Styling**: Tailwind CSS with custom dark theme
- **Animations**: Framer Motion for smooth transitions

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- GitHub Token (optional, for higher rate limits)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run server
uvicorn main:app --reload
```

Backend will run at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.local.example .env.local

# Run development server
npm run dev
```

Frontend will run at `http://localhost:3000`

## 📖 Usage

1. **Open the application** at `http://localhost:3000`
2. **Enter a GitHub URL** (e.g., `https://github.com/facebook/react`)
3. **Wait for analysis** - The system will:
   - Fetch repository files
   - Analyze code structure
   - Generate interactive visualization
4. **Explore the graph** - View the architectural diagram
5. **Ask questions** - Use the chat interface to query the codebase

### Example Questions

- "Where is the authentication logic?"
- "Explain the data flow in this application"
- "Are there any potential bugs or race conditions?"
- "How does the payment processing work?"
- "Map the user registration flow"

## 📁 Project Structure

```
legacy-code-archaeologist/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── models.py              # Pydantic models
│   ├── services/
│   │   ├── github_service.py  # GitHub integration
│   │   └── gemini_service.py  # Gemini AI integration
│   ├── requirements.txt       # Python dependencies
│   └── README.md
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # Main page
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── RepoInput.tsx      # URL input component
│   │   ├── GraphViewer.tsx    # Mermaid visualization
│   │   ├── ChatInterface.tsx  # Chat component
│   │   └── LoadingState.tsx   # Loading animation
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   └── utils.ts           # Utilities
│   ├── package.json
│   └── README.md
└── README.md                   # This file
```

## 🎨 Features in Detail

### 1. Repository Analysis
- Fetches up to 50 files from any public GitHub repository
- Supports multiple programming languages (.py, .js, .ts, .java, .go, .rs, .cpp, .c, .h)
- Intelligently skips irrelevant directories (node_modules, venv, etc.)

### 2. AI-Powered Visualization
- Generates Mermaid.js diagrams showing code architecture
- Groups related files into logical modules
- Shows data flow and dependencies
- Fallback to simple file structure if AI generation fails

### 3. Interactive Chat
- Ask natural language questions about the codebase
- Get detailed answers with file citations
- View relevant code snippets with syntax highlighting
- Context-aware responses based on entire repository

### 4. Premium UI/UX
- Dark theme with glassmorphism effects
- Smooth animations and transitions
- Responsive design
- Loading states with visual feedback

## 🔧 API Endpoints

### POST `/api/analyze`
Analyze a GitHub repository

**Request:**
```json
{
  "repo_url": "https://github.com/owner/repo",
  "max_files": 50,
  "file_extensions": [".py", ".js"]
}
```

**Response:**
```json
{
  "repo_name": "repo",
  "total_files": 25,
  "mermaid_graph": "graph TD\n...",
  "summary": "Architecture summary",
  "files_analyzed": ["file1.py", "file2.js"]
}
```

### POST `/api/chat`
Ask questions about the codebase

**Request:**
```json
{
  "repo_url": "https://github.com/owner/repo",
  "question": "Where is the authentication logic?"
}
```

**Response:**
```json
{
  "answer": "Detailed explanation...",
  "relevant_files": ["auth.py"],
  "code_snippets": [...]
}
```

## 🌟 Tech Stack

- **Backend**: Python, FastAPI, PyGithub, Google Generative AI
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **UI Components**: Shadcn/UI, Lucide Icons
- **Visualization**: Mermaid.js
- **Animations**: Framer Motion
- **Code Highlighting**: React Syntax Highlighter

## 🚧 Production Deployment

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
npm start
```

For production, consider:
- Using a process manager (PM2, systemd)
- Setting up reverse proxy (Nginx)
- Enabling HTTPS
- Using a proper database for caching (Redis)
- Implementing rate limiting
- Adding authentication

## 📝 Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token_optional
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤝 Contributing

This project was built for a hackathon. Contributions are welcome!

## 📄 License

MIT License

## 🎓 Hackathon Submission

**Title**: Legacy Code Archaeologist — The GenAI Technical Debt Solver

**Problem**: Developers spend up to 50% of their time deciphering legacy code rather than writing new features.

**Solution**: An agentic IDE companion that transforms static codebases into interactive knowledge graphs using Gemini 1.5 Pro's 2M token context window.

**Innovation**: 
- Generative visualization with real-time architectural diagrams
- Semantic excavation across entire repositories
- Context-aware debugging assistance

---

Built with ❤️ for developers who love archaeology
