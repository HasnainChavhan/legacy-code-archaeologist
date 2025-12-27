from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any


class RepoAnalysisRequest(BaseModel):
    """Request model for repository analysis"""
    repo_url: str
    max_files: Optional[int] = 50
    file_extensions: Optional[List[str]] = [".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c", ".h"]


class RepoAnalysisResponse(BaseModel):
    """Response model for repository analysis"""
    repo_name: str
    total_files: int
    mermaid_graph: str
    summary: str
    files_analyzed: List[str]
    tech_stack: Optional[Dict[str, List[str]]] = None
    tech_stack_analysis: Optional[str] = None
    repo_summary: Optional[str] = None


class ChatRequest(BaseModel):
    """Request model for chat/question about code"""
    repo_url: str
    question: str
    context: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat"""
    answer: str
    relevant_files: Optional[List[str]] = []
    code_snippets: Optional[List[Dict[str, Any]]] = []
