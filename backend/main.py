import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import time
from models import (
    RepoAnalysisRequest, 
    RepoAnalysisResponse, 
    ChatRequest, 
    ChatResponse
)
from services.github_service import GitHubService
from services.gemini_service import GeminiService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Legacy Code Archaeologist API",
    description="GenAI-powered tool to explain, visualize, and debug old codebases",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

github_service = GitHubService(github_token=GITHUB_TOKEN)
gemini_service = GeminiService(api_key=GEMINI_API_KEY)

# In-memory cache for repository data (in production, use Redis or similar)
repo_cache = {}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Legacy Code Archaeologist API",
        "version": "1.0.0"
    }


@app.post("/api/analyze", response_model=RepoAnalysisResponse)
def analyze_repository(request: RepoAnalysisRequest):
    """
    Analyze a GitHub repository and generate visualization
    """
    total_start = time.time()  # Start timing
    print(f"\n{'='*60}", flush=True)
    print(f"[API] Received analyze request for: {request.repo_url}", flush=True)

    # ... implementation (no changes needed inside) ...
    try:
        # Fetch repository metadata
        print(f"[API] Fetching repo metadata...", flush=True)
        repo_metadata = github_service.get_repo_metadata(request.repo_url)
        print(f"[API] Repo name: {repo_metadata['name']}", flush=True)
        
        # Fetch repository files
        print(f"[API] Fetching repository files...", flush=True)
        files_content = github_service.fetch_repository_files(
            repo_url=request.repo_url,
            max_files=50
        )
        print(f"[API] Fetched {len(files_content)} files", flush=True)
        
        if not files_content:
            raise HTTPException(
                status_code=404, 
                detail="No files found in repository with specified extensions"
            )
        
        # Detect technology stack (LOCAL - FAST)
        print(f"[API] Detecting technology stack...", flush=True)
        tech_stack = gemini_service.detect_tech_stack(files_content)
        print(f"[API] Tech stack: {tech_stack}", flush=True)
        
        # LOCAL tech stack analysis (NO AI - INSTANT)
        print(f"[API] Generating tech stack description...", flush=True)
        tech_parts = []
        if tech_stack["languages"]:
            tech_parts.append(f"Built with {', '.join(tech_stack['languages'][:2])}")
        if tech_stack["frameworks"]:
            tech_parts.append(f"using {', '.join(tech_stack['frameworks'][:2])}")
        tech_stack_analysis = ". ".join(tech_parts) + "." if tech_parts else "Software application."
        print(f"[API] ✅ Tech stack: {tech_stack_analysis}", flush=True)
        
        # LOCAL repository summary (NO AI - INSTANT)
        print(f"[API] Generating repository summary...", flush=True)
        file_count = len(files_content)
        file_types = {}
        for path in files_content.keys():
            ext = path.split('.')[-1] if '.' in path else 'other'
            file_types[ext] = file_types.get(ext, 0) + 1
        top_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:3]
        type_desc = ", ".join([f"{count} {ext} files" for ext, count in top_types])
        lang_desc = ', '.join(tech_stack['languages'][:2]) if tech_stack['languages'] else 'various technologies'
        repo_summary = f"{repo_metadata['name']} is a software repository containing {file_count} files ({type_desc}). The project uses {lang_desc} and includes components for software development. This codebase appears to be a {tech_stack['frameworks'][0] if tech_stack['frameworks'] else 'general'} application with well-organized structure."
        print(f"[API] ✅ Summary generated", flush=True)
        
        # Generate Mermaid visualization
        print(f"[API] Generating visualization...", flush=True)
        result = gemini_service.generate_mermaid_graph(files_content, repo_metadata['name'])
        print(f"[API] Visualization generated", flush=True)
        
        # Cache the result to avoid repeated API calls
        repo_cache[request.repo_url] = {
            'files_content': files_content,
            'result': result,
            'tech_stack': tech_stack,
            'tech_stack_analysis': tech_stack_analysis,
            'repo_summary': repo_summary
        }
        
        total_time = time.time() - total_start
        print(f"\n[API] ✅ Analysis complete!")
        print(f"[API] 📊 Total time: {total_time:.2f}s")
        print(f"{'='*60}\n", flush=True)
        
        return RepoAnalysisResponse(
            repo_name=repo_metadata['name'],
            total_files=len(files_content),
            mermaid_graph=result['mermaid_graph'],
            summary=result['summary'],
            files_analyzed=list(files_content.keys()),
            tech_stack=tech_stack,
            tech_stack_analysis=tech_stack_analysis,
            repo_summary=repo_summary
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/chat", response_model=ChatResponse)
def chat_about_code(request: ChatRequest):
    """
    Answer questions about a repository's code
    """
    try:
        # Get files from cache or fetch them
        if request.repo_url not in repo_cache:
            files_content = github_service.fetch_repository_files(
                repo_url=request.repo_url,
                max_files=50
            )
            repo_cache[request.repo_url] = {'files_content': files_content}
        else:
            # Access files_content from the cache dictionary
            cached_data = repo_cache[request.repo_url]
            if isinstance(cached_data, dict) and 'files_content' in cached_data:
                files_content = cached_data['files_content']
            else:
                # Old cache format, use directly
                files_content = cached_data
        
        if not files_content:
            raise HTTPException(
                status_code=404,
                detail="Repository not found or no files available"
            )
        
        # Get answer from Gemini
        result = gemini_service.answer_question(
            question=request.question,
            files_content=files_content,
            context=request.context
        )
        
        return ChatResponse(
            answer=result["answer"],
            relevant_files=result.get("relevant_files", []),
            code_snippets=result.get("code_snippets", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/api/repo/{owner}/{repo}/metadata")
def get_repo_metadata(owner: str, repo: str):
    """
    Get metadata for a GitHub repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        
    Returns:
        Repository metadata
    """
    try:
        repo_url = f"https://github.com/{owner}/{repo}"
        metadata = github_service.get_repo_metadata(repo_url)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch metadata: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
