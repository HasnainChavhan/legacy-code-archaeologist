import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface RepoAnalysisRequest {
    repo_url: string;
    max_files?: number;
    file_extensions?: string[];
}

export interface RepoAnalysisResponse {
    repo_name: string;
    total_files: number;
    mermaid_graph: string;
    summary: string;
    files_analyzed: string[];
    tech_stack?: {
        languages: string[];
        frameworks: string[];
        tools: string[];
    };
    tech_stack_analysis?: string;
    repo_summary?: string;
}

export interface ChatRequest {
    repo_url: string;
    question: string;
    context?: string;
}

export interface ChatResponse {
    answer: string;
    relevant_files?: string[];
    code_snippets?: Array<{
        file: string;
        lines: string;
        snippet: string;
        explanation: string;
    }>;
}

export const api = {
    analyzeRepository: async (data: RepoAnalysisRequest): Promise<RepoAnalysisResponse> => {
        const response = await axios.post(`${API_BASE_URL}/api/analyze`, data);
        return response.data;
    },

    chatAboutCode: async (data: ChatRequest): Promise<ChatResponse> => {
        const response = await axios.post(`${API_BASE_URL}/api/chat`, data);
        return response.data;
    },
};
