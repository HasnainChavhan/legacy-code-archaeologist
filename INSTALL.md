# Installation & Setup Instructions

## ✅ Already Completed
- Backend virtual environment created
- Backend Python dependencies installed

## 🔧 Required Actions

### 1. Install Node.js (5 minutes)

**You need to do this manually:**

1. Open browser and go to: **https://nodejs.org/**
2. Download the **LTS version** (recommended - currently 18.x or 20.x)
3. Run the installer (.msi file)
4. Follow installation wizard (use default settings)
5. **Restart your terminal/PowerShell** after installation
6. Verify installation: `node --version`

### 2. Get Gemini API Key (2 minutes)

**Steps:**
1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"** button
4. Copy the generated API key
5. Open `backend/.env` file (I've created it for you)
6. Replace `your_gemini_api_key_here` with your actual key
7. Save the file

**Example `.env` file:**
```
GEMINI_API_KEY=AIzaSyC_your_actual_key_here_abc123xyz
GITHUB_TOKEN=optional
```

## 🚀 After Setup - Run the Application

Once you've completed steps 1 and 2 above:

### Option A: Quick Start (Recommended)
```bash
# Just double-click this file in Windows Explorer:
start.bat
```

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📍 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ❓ Why Can't I Auto-Install Node.js?

Node.js requires:
- Administrative privileges
- System PATH modifications
- Windows registry changes
- Downloading from external sources

These actions require manual user approval for security reasons.

## 🆘 Troubleshooting

**"Node.js still not found after install"**
- Restart your terminal/PowerShell
- Restart VS Code if using it
- Log out and log back in to Windows

**"GEMINI_API_KEY error"**
- Make sure you saved the `.env` file
- Check there are no extra spaces in the key
- Verify the key is valid at Google AI Studio

**Need more help?**
- See [DEPLOYMENT.md](file:///c:/Users/91932/Downloads/proje/DEPLOYMENT.md) for detailed guide
- Check [README.md](file:///c:/Users/91932/Downloads/proje/README.md) for project overview

---

**⏱️ Total Setup Time: ~7 minutes**
