# Deployment Guide - Legacy Code Archaeologist

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn
- Gemini API Key
- (Optional) GitHub Personal Access Token

## Step 1: Clone/Setup Project

```bash
cd c:/Users/91932/Downloads/proje
```

## Step 2: Backend Setup

### 2.1 Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2.2 Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables

1. Copy the example file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your keys:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   GITHUB_TOKEN=your_github_token_here_optional
   ```

   **Get API Keys:**
   - Gemini API Key: https://makersuite.google.com/app/apikey
   - GitHub Token: https://github.com/settings/tokens (optional, for higher rate limits)

### 2.5 Run Backend Server

```bash
uvicorn main:app --reload
```

Backend will be available at: `http://localhost:8000`

Test it: Open `http://localhost:8000` in browser - you should see:
```json
{
  "status": "online",
  "service": "Legacy Code Archaeologist API",
  "version": "1.0.0"
}
```

## Step 3: Frontend Setup

### 3.1 Open New Terminal

Keep the backend running, open a new terminal window.

### 3.2 Navigate to Frontend

```bash
cd c:/Users/91932/Downloads/proje/frontend
```

### 3.3 Install Dependencies

**If you have Node.js installed:**
```bash
npm install
```

**If Node.js is not installed:**
1. Download and install Node.js from: https://nodejs.org/
2. Choose LTS version (18.x or higher)
3. After installation, run: `npm install`

### 3.4 Configure Environment (Optional)

The frontend is pre-configured to use `http://localhost:8000`. If your backend runs on a different URL:

```bash
copy .env.local.example .env.local
```

Edit `.env.local` if needed.

### 3.5 Run Frontend Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Step 4: Test the Application

1. **Open Browser**: Navigate to `http://localhost:3000`

2. **Enter a GitHub URL**: Try one of these:
   - `https://github.com/facebook/react`
   - `https://github.com/vercel/next.js`
   - Any public GitHub repository

3. **Click "Analyze"**: Wait for the analysis to complete

4. **View Results**:
   - See the architectural diagram
   - Ask questions in the chat interface

## Troubleshooting

### Backend Issues

**Error: "GEMINI_API_KEY environment variable is required"**
- Make sure you created `.env` file in the `backend` folder
- Verify the API key is correct

**Error: "Failed to fetch repository"**
- Check your internet connection
- Verify the GitHub URL is correct and the repo is public
- If using a GitHub token, ensure it's valid

**Port 8000 already in use:**
```bash
# Run on different port
uvicorn main:app --reload --port 8001
```
Then update frontend `.env.local` to use `http://localhost:8001`

### Frontend Issues

**Error: "node is not recognized"**
- Install Node.js from https://nodejs.org/
- Restart your terminal after installation

**Error: "Cannot connect to backend"**
- Ensure backend is running on `http://localhost:8000`
- Check if `.env.local` has correct backend URL
- Verify no firewall is blocking the connection

**Port 3000 already in use:**
```bash
# Next.js will automatically suggest port 3001
# Or specify manually:
npm run dev -- -p 3001
```

## Production Deployment

### Backend Production

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Production

```bash
cd frontend
npm run build
npm start
```

### Recommended Production Setup

1. **Use Process Manager**: PM2 or systemd
2. **Reverse Proxy**: Nginx or Apache
3. **HTTPS**: Let's Encrypt SSL certificates
4. **Database**: Redis for caching repository data
5. **Rate Limiting**: Implement API rate limits
6. **Authentication**: Add user authentication if needed

### Docker Deployment (Optional)

Create `Dockerfile` for backend:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `Dockerfile` for frontend:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## Environment Variables Reference

### Backend (.env)
```bash
GEMINI_API_KEY=your_gemini_api_key          # Required
GITHUB_TOKEN=your_github_token              # Optional
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000   # Backend URL
```

## Quick Start Script (Windows)

Create `start.bat` in project root:
```batch
@echo off
echo Starting Legacy Code Archaeologist...

start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload"
timeout /t 3
start cmd /k "cd frontend && npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
```

Run: `start.bat`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the README.md files in backend and frontend folders
3. Ensure all prerequisites are installed
4. Verify environment variables are set correctly

---

**Happy Code Archaeology! 🔍**
