# Legacy Code Archaeologist - Backend

FastAPI backend for analyzing GitHub repositories using Gemini 1.5 Pro.

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   - `GEMINI_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - `GITHUB_TOKEN`: (Optional) Get from [GitHub Settings](https://github.com/settings/tokens)

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

   Server will start at `http://localhost:8000`

## API Endpoints

### POST `/api/analyze`
Analyze a GitHub repository and generate visualization.

**Request:**
```json
{
  "repo_url": "https://github.com/owner/repo",
  "max_files": 50,
  "file_extensions": [".py", ".js", ".ts"]
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
Ask questions about the codebase.

**Request:**
```json
{
  "repo_url": "https://github.com/owner/repo",
  "question": "Where is the authentication logic?",
  "context": "Optional additional context"
}
```

**Response:**
```json
{
  "answer": "Detailed explanation...",
  "relevant_files": ["auth.py", "middleware.js"],
  "code_snippets": [
    {
      "file": "auth.py",
      "lines": "10-20",
      "snippet": "code here",
      "explanation": "why relevant"
    }
  ]
}
```

## Project Structure

```
backend/
├── main.py                 # FastAPI entry point
├── models.py              # Pydantic models
├── services/
│   ├── github_service.py  # GitHub API integration
│   └── gemini_service.py  # Gemini AI integration
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```
