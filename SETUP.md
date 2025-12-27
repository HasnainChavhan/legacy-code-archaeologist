# Quick Setup Guide

## ⚠️ Prerequisites Required

Before running the application, you need:

### 1. Node.js (Required for Frontend)
**Status**: ❌ Not Installed

**Install:**
1. Download from: https://nodejs.org/
2. Choose LTS version (18.x or higher)
3. Run installer and follow prompts
4. Restart your terminal after installation

### 2. Gemini API Key (Required for Backend)
**Status**: ⚠️ Needs Configuration

**Get API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

**Configure:**
1. Open: `backend/.env.example`
2. Copy it to `backend/.env`
3. Replace `your_gemini_api_key_here` with your actual API key

### 3. GitHub Token (Optional)
For higher API rate limits, get a token from: https://github.com/settings/tokens

---

## 🚀 Running the Application

### Option 1: Automatic (After Prerequisites)

**Windows:**
```bash
start.bat
```

This will automatically:
- Start backend on http://localhost:8000
- Start frontend on http://localhost:3000

### Option 2: Manual Setup

#### Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1
# Make sure .env file has your GEMINI_API_KEY
uvicorn main:app --reload
```

#### Frontend (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

---

## ✅ Current Status

- ✅ Backend virtual environment created
- ✅ Backend dependencies installed
- ❌ Node.js needs to be installed
- ⚠️ GEMINI_API_KEY needs to be configured in `backend/.env`

---

## 📝 Next Steps

1. **Install Node.js** from https://nodejs.org/
2. **Get Gemini API Key** from https://makersuite.google.com/app/apikey
3. **Create `backend/.env`** file with your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
4. **Run the application** using `start.bat` or manual commands

---

## 🆘 Need Help?

See [DEPLOYMENT.md](file:///c:/Users/91932/Downloads/proje/DEPLOYMENT.md) for detailed troubleshooting.
