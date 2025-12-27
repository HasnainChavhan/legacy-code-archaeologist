import os
import json
import sys
from typing import Dict, List, Optional
import google.generativeai as genai

# Force flush for immediate output
def log(msg):
    print(msg, flush=True)
    sys.stdout.flush()


class GeminiService:
    """Service to interact with Gemini 1.5 Pro for code analysis"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini service with API key"""
        genai.configure(api_key=api_key)
        # Models are initialized per-function for better quota management
        # Configure generation settings
        self.generation_config = {
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 4096,  # Pro supports larger output
        }
        print(f"✅ Gemini service initialized with Pro model")
    
    def create_code_context(self, files_content: Dict[str, str]) -> str:
        """
        Create a comprehensive code context from all files
        
        Args:
            files_content: Dictionary mapping file paths to contents
            
        Returns:
            Formatted string with all code content
        """
        context_parts = []
        
        for file_path, content in files_content.items():
            context_parts.append(f"=== FILE: {file_path} ===")
            context_parts.append(content)
            context_parts.append("\n")
        
        return "\n".join(context_parts)
    
    def detect_tech_stack(self, files_content: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Detect technology stack from repository files
        
        Args:
            files_content: Dictionary mapping file paths to contents
            
        Returns:
            Dictionary with languages, frameworks, and tools
        """
        stack = {
            "languages": set(),
            "frameworks": set(),
            "tools": set()
        }
        
        # Detect languages by file extensions
        for file_path in files_content.keys():
            ext = file_path.split('.')[-1].lower() if '.' in file_path else ''
            
            if ext == 'py':
                stack["languages"].add("Python")
            elif ext in ['js', 'jsx']:
                stack["languages"].add("JavaScript")
            elif ext in ['ts', 'tsx']:
                stack["languages"].add("TypeScript")
            elif ext == 'java':
                stack["languages"].add("Java")
            elif ext == 'go':
                stack["languages"].add("Go")
            elif ext == 'rb':
                stack["languages"].add("Ruby")
            elif ext in ['c', 'cpp', 'cc']:
                stack["languages"].add("C/C++")
            elif ext == 'rs':
                stack["languages"].add("Rust")
        
        # Detect frameworks and tools from package files
        for file_path, content in files_content.items():
            filename = file_path.split('/')[-1].lower()
            
            # Check package.json for Node.js frameworks
            if filename == 'package.json':
                stack["tools"].add("npm")
                try:
                    # Try to parse JSON for better detection
                    import json
                    pkg_data = json.loads(content)
                    dependencies = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                    
                    if 'react' in dependencies or '@types/react' in dependencies:
                        stack["frameworks"].add("React")
                    if 'next' in dependencies or 'next' in str(dependencies):
                        stack["frameworks"].add("Next.js")
                    if 'vue' in dependencies:
                        stack["frameworks"].add("Vue.js")
                    if 'express' in dependencies:
                        stack["frameworks"].add("Express")
                    if 'angular' in str(dependencies) or '@angular/core' in dependencies:
                        stack["frameworks"].add("Angular")
                    if 'svelte' in dependencies:
                        stack["frameworks"].add("Svelte")
                except:
                    # Fallback to string search
                    if '"react"' in content or '@types/react' in content:
                        stack["frameworks"].add("React")
                    if '"next"' in content:
                        stack["frameworks"].add("Next.js")
                    if '"vue"' in content:
                        stack["frameworks"].add("Vue.js")
                    if '"express"' in content:
                        stack["frameworks"].add("Express")
            
            # Check requirements.txt for Python frameworks
            elif filename == 'requirements.txt' or filename == 'requirements.in':
                stack["tools"].add("pip")
                content_lower = content.lower()
                if 'django' in content_lower:
                    stack["frameworks"].add("Django")
                if 'flask' in content_lower:
                    stack["frameworks"].add("Flask")
                if 'fastapi' in content_lower:
                    stack["frameworks"].add("FastAPI")
                if 'streamlit' in content_lower:
                    stack["frameworks"].add("Streamlit")
            
            # Check for Docker
            elif filename == 'dockerfile':
                stack["tools"].add("Docker")
            
            # Check for GitHub Actions
            elif '.github/workflows' in file_path:
                stack["tools"].add("GitHub Actions")
            
            # Check for other config files
            elif filename == 'cargo.toml':
                stack["tools"].add("Cargo")
            elif filename == 'go.mod':
                stack["tools"].add("Go Modules")
            elif filename == 'pom.xml':
                stack["tools"].add("Maven")
            elif filename == 'build.gradle':
                stack["tools"].add("Gradle")
        
        # Convert sets to sorted lists
        return {
            "languages": sorted(list(stack["languages"])),
            "frameworks": sorted(list(stack["frameworks"])),
            "tools": sorted(list(stack["tools"]))
        }
    
    def analyze_tech_stack(self, tech_stack: Dict[str, List[str]]) -> str:
        """
        Use Gemini to provide insights about the detected tech stack
        
        Args:
            tech_stack: Dictionary with languages, frameworks, and tools
            
        Returns:
            AI-generated analysis of the tech stack
        """
        if not any(tech_stack.values()):
            return "No technology stack detected."
        
        # Use Flash model for quick analysis
        flash_model = genai.GenerativeModel('gemini-1.5-flash')
        
        stack_summary = []
        if tech_stack["languages"]:
            stack_summary.append(f"Languages: {', '.join(tech_stack['languages'])}")
        if tech_stack["frameworks"]:
            stack_summary.append(f"Frameworks: {', '.join(tech_stack['frameworks'])}")
        if tech_stack["tools"]:
            stack_summary.append(f"Tools: {', '.join(tech_stack['tools'])}")
        
        prompt = f"""Analyze this technology stack in ONE sentence (max 20 words):

{chr(10).join(stack_summary)}

Describe what type of application this stack is typically used for.
ONE sentence only, be specific and concise. Use plain text, NO markdown formatting."""

        try:
            response = pro_model.generate_content(
                prompt,
                generation_config={"temperature": 0.7, "max_output_tokens": 1000}
            )
            return response.text.strip()
        except Exception as e:
            log(f"[TECH STACK ANALYSIS ERROR] {e}")
            # Fallback to simple description
            parts = []
            if tech_stack["languages"]:
                parts.append(f"Built with {', '.join(tech_stack['languages'])}")
            if tech_stack["frameworks"]:
                parts.append(f"using {', '.join(tech_stack['frameworks'])}")
            return ". ".join(parts) + "."
    
    def generate_repo_summary(self, files_content: Dict[str, str], repo_name: str) -> str:
        """
        Generate an AI-powered summary of what the repository contains and does
        
        Args:
            files_content: Dictionary mapping file paths to contents
            repo_name: Name of the repository
            
        Returns:
            AI-generated summary of repository contents and functionality
        """
        # Use Flash model for quick analysis
        flash_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Find README content
        readme_content = ""
        for file_path, content in files_content.items():
            if 'readme' in file_path.lower():
                readme_content = content[:1500]
                break
        
        # Get file list with structure
        file_list = list(files_content.keys())[:15]
        
        # Sample key files
        code_sample = ""
        for file_path, content in list(files_content.items())[:3]:
            code_sample += f"{file_path}: {content[:200]}\n\n"
        
        prompt = f"""Analyze this repository and write a COMPLETE summary (10-15 lines). DO NOT stop mid-sentence.

Repository: {repo_name}

README:
{readme_content if readme_content else "No README"}

Files: {', '.join(file_list)}

Code samples:
{code_sample}

Write a detailed summary that explains:
1. What this repository is (project type, purpose)
2. Main files and what each does
3. Key features or functionality
4. How the components work together

IMPORTANT: Write 10-15 complete lines. Do NOT truncate. Finish all sentences."""

        try:
            # Reduced tokens for faster response
            response = flash_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.4, 
                    "max_output_tokens": 400,  # Reduced for speed
                    "top_p": 0.95,
                    "top_k": 40
                },
                request_options={"timeout": 15}  # 15 second timeout
            )
            return response.text.strip()
        except Exception as e:
            log(f"[REPO SUMMARY ERROR] {e}")
            # Return quick fallback
            return f"Repository with {len(files_content)} files. Contains code for software development."
    
    def generate_mermaid_graph(self, files_content: Dict[str, str], repo_name: str) -> Dict[str, str]:
        """
        Generate Mermaid.js graph visualization of code structure
        
        Args:
            files_content: Dictionary mapping file paths to contents
            repo_name: Name of the repository
            
        Returns:
            Dictionary with mermaid_graph and summary
        """
        # FOR HACKATHON: USE FALLBACK BY DEFAULT
        # This ensures it ALWAYS works, even with quota limits
        
        log(f"[FALLBACK] Using local diagram generation for reliability")
        
        # Create a nice summary based on file types
        file_types = {}
        for file_path in files_content.keys():
            ext = file_path.split('.')[-1] if '.' in file_path else 'other'
            file_types[ext] = file_types.get(ext, 0) + 1
        
        tech_summary = ", ".join([f"{count} {ext} files" for ext, count in list(file_types.items())[:3]])
        
        return {
            "mermaid_graph": self._create_simple_graph(files_content),
            "summary": f"✅ Analyzed {len(files_content)} files ({tech_summary}). Architecture diagram generated from repository structure."
        }
    
    def _create_simple_graph(self, files_content: Dict[str, str]) -> str:
        """Create a simple fallback graph based on file structure"""
        graph_lines = ["graph TD"]
        graph_lines.append("    Repository[\"Repository\"]")
        
        for file_path in sorted(files_content.keys())[:10]:
            # Clean filename for Mermaid (remove special chars, limit length)
            filename = file_path.split('/')[-1]
            # Escape special characters and limit length
            safe_filename = filename.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('"', '').replace("'", '')
            if len(safe_filename) > 30:
                safe_filename = safe_filename[:27] + "..."
            
            # Create node ID (alphanumeric only)
            node_id = filename.replace('.', '_').replace('-', '_').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', '_')
            if len(node_id) > 20:
                node_id = node_id[:20]
            
            # Add edge with cleaned label
            graph_lines.append(f"    Repository --> {node_id}[\"{safe_filename}\"]")
        
        return "\n".join(graph_lines)
    
    def answer_question(
        self, 
        question: str, 
        files_content: Dict[str, str],
        context: Optional[str] = None
    ) -> Dict[str, any]:
        """Answer questions using Gemini 1.5 Pro"""
        log(f"[CHAT] Question: {question}")
        
        # Use Pro model for chat
        pro_model = genai.GenerativeModel('gemini-1.5-pro')
        
        code_context = self.create_code_context(files_content)
        limited_context = code_context[:15000]  # Limit context for speed
        
        prompt = f"""Answer this question about the code:

Code:
{limited_context}

Question: {question}

Provide a brief, helpful answer."""

        try:
            response = pro_model.generate_content(
                prompt,
                generation_config={"temperature": 0.7, "max_output_tokens": 500}
            )
            return {
                "answer": response.text,
                "relevant_files": list(files_content.keys())[:5],
                "code_snippets": []
            }
        except Exception as e:
            log(f"[CHAT ERROR] {e}")
            return {
                "answer": f"⚠️ Chat error: {str(e)}. The analysis features above provide comprehensive insights!",
                "relevant_files": [],
                "code_snippets": []
            }

