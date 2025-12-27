import os
from typing import List, Dict, Optional
from github import Github, Repository, GithubException
import base64
import re


class GitHubService:
    """Service to fetch and parse files from GitHub repositories"""
    
    def __init__(self, github_token: Optional[str] = None):
        """Initialize GitHub service with optional token for higher rate limits"""
        # Treat empty string as None
        token = github_token if github_token and github_token.strip() else None
        self.github = Github(token) if token else Github()
    
    def parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """
        Parse GitHub URL to extract owner and repo name
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo_name)
        """
        # Handle various GitHub URL formats
        patterns = [
            r'github\.com/([^/]+)/([^/]+?)(?:\.git)?$',
            r'github\.com/([^/]+)/([^/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                owner, repo = match.groups()
                return owner, repo.rstrip('/')
        
        raise ValueError(f"Invalid GitHub URL: {repo_url}")
    
    def get_repository(self, repo_url: str) -> Repository.Repository:
        """
        Get GitHub repository object
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            PyGithub Repository object
        """
        owner, repo_name = self.parse_repo_url(repo_url)
        try:
            return self.github.get_repo(f"{owner}/{repo_name}")
        except GithubException as e:
            raise Exception(f"Failed to fetch repository: {str(e)}")
    
    def get_file_content(self, repo: Repository.Repository, file_path: str) -> str:
        """
        Get content of a specific file from repository
        
        Args:
            repo: PyGithub Repository object
            file_path: Path to file in repository
            
        Returns:
            File content as string
        """
        try:
            content = repo.get_contents(file_path)
            if isinstance(content, list):
                return ""
            
            # Decode base64 content
            return base64.b64decode(content.content).decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return ""
    
    def fetch_repository_files(
        self, 
        repo_url: str, 
        max_files: int = 50,
        file_extensions: List[str] = None
    ) -> Dict[str, str]:
        """
        Fetch all relevant files from a GitHub repository
        
        Args:
            repo_url: GitHub repository URL
            max_files: Maximum number of files to fetch
            file_extensions: List of file extensions to include
            
        Returns:
            Dictionary mapping file paths to their contents
        """
        if file_extensions is None:
            # Expanded list for Hackathon demo compatibility
            file_extensions = [
                ".py", ".js", ".ts", ".tsx", ".jsx", 
                ".java", ".go", ".rs", ".cpp", ".c", ".h", 
                ".css", ".html", ".md", ".json", ".yml", ".yaml"
            ]
        
        repo = self.get_repository(repo_url)
        files_content = {}
        
        try:
            # Start traversing from root
            import time
            start_time = time.time()
            
            # Helper with timeout check
            def traverse_contents_with_timeout(contents, current_count=0):
                if time.time() - start_time > 5: # 5s timeout (reduced from 20s)
                    print("⚠️ GitHub fetch timeout reached (5s)")
                    return current_count
                
                if current_count >= max_files:
                    return current_count
                
                for content in contents:
                    if time.time() - start_time > 5:  # Check timeout in loop too
                        break
                        
                    if current_count >= max_files:
                        break
                    
                    if content.type == "dir":
                        # Skip common directories
                        if content.path.startswith(('node_modules', 'venv', '.git', 'dist', 'build', '__pycache__', 'test', 'docs')):
                            continue
                        
                        try:
                            current_count = traverse_contents_with_timeout(
                                repo.get_contents(content.path), 
                                current_count
                            )
                        except Exception as e:
                            print(f"Error traversing directory {content.path}: {str(e)}")
                            continue
                    else:
                        # Check ext or special files
                        param_ext = any(content.path.endswith(ext) for ext in file_extensions)
                        special_file = content.name.lower().startswith(('readme', 'license', 'dockerfile', 'makefile'))
                        
                        if param_ext or special_file:
                            file_content = self.get_file_content(repo, content.path)
                            if file_content:
                                files_content[content.path] = file_content
                                current_count += 1
                return current_count

            contents = repo.get_contents("")
            traverse_contents_with_timeout(contents)
        except Exception as e:
            # If we found at least some files, don't crash
            if files_content:
                print(f"Partial fetch success: {str(e)}")
            else:
                raise Exception(f"Failed to fetch repository files: {str(e)}")
        
        return files_content
    
    def get_repo_metadata(self, repo_url: str) -> Dict[str, any]:
        """
        Get repository metadata
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Dictionary with repository metadata
        """
        repo = self.get_repository(repo_url)
        
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "url": repo.html_url
        }
