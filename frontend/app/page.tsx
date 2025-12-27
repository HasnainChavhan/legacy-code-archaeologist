'use client';

import React, { useState } from 'react';
import RepoInput from '@/components/RepoInput';
import GraphViewer from '@/components/GraphViewer';
import ChatInterface from '@/components/ChatInterface';
import LoadingState from '@/components/LoadingState';
import TechStackBadge from '@/components/TechStackBadge';
import { api, type RepoAnalysisResponse } from '@/lib/api';

export default function Home() {
    const [isLoading, setIsLoading] = useState(false);
    const [analysisData, setAnalysisData] = useState<RepoAnalysisResponse | null>(null);
    const [currentRepoUrl, setCurrentRepoUrl] = useState('');
    const [error, setError] = useState<string | null>(null);

    const handleAnalyze = async (repoUrl: string) => {
        setIsLoading(true);
        setError(null);
        setCurrentRepoUrl(repoUrl);

        try {
            const data = await api.analyzeRepository({
                repo_url: repoUrl,
                max_files: 15, // Reduced for faster analysis
            });
            setAnalysisData(data);
        } catch (err: any) {
            console.error('Analysis error:', err);
            setError(err.response?.data?.detail || 'Failed to analyze repository. Please check the URL and try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleSendMessage = async (message: string) => {
        return await api.chatAboutCode({
            repo_url: currentRepoUrl,
            question: message,
        });
    };

    const handleReset = () => {
        setAnalysisData(null);
        setCurrentRepoUrl('');
        setError(null);
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Background effects */}
            <div className="fixed inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />

            <div className="relative z-10 container mx-auto px-4 py-8">
                {/* Header */}
                <header className="text-center mb-12">
                    <h1 className="text-5xl md:text-6xl font-bold gradient-text mb-4">
                        Legacy Code Archaeologist
                    </h1>
                    <p className="text-xl text-muted-foreground">
                        Unearth the secrets of legacy codebases with AI-powered analysis
                    </p>
                </header>

                {/* Main Content */}
                <div className="max-w-7xl mx-auto space-y-8">
                    {!analysisData && !isLoading && (
                        <div className="flex justify-center">
                            <RepoInput onSubmit={handleAnalyze} isLoading={isLoading} />
                        </div>
                    )}

                    {isLoading && <LoadingState />}

                    {error && (
                        <div className="max-w-2xl mx-auto">
                            <div className="bg-destructive/10 border border-destructive rounded-lg p-6 text-center">
                                <h3 className="text-lg font-semibold text-destructive mb-2">Analysis Failed</h3>
                                <p className="text-sm text-muted-foreground mb-4">{error}</p>
                                <button
                                    onClick={handleReset}
                                    className="text-sm text-primary hover:underline"
                                >
                                    Try another repository
                                </button>
                            </div>
                        </div>
                    )}

                    {analysisData && (
                        <>
                            {/* Reset button */}
                            <div className="flex justify-center">
                                <button
                                    onClick={handleReset}
                                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                                >
                                    ← Analyze another repository
                                </button>
                            </div>

                            {/* Repository Summary */}
                            {analysisData.repo_summary && (
                                <div className="glass-effect p-6 rounded-lg animate-fade-in border-l-4 border-blue-500">
                                    <h3 className="text-lg font-bold gradient-text mb-3 flex items-center gap-2">
                                        <span className="text-2xl">📚</span>
                                        Repository Overview
                                    </h3>
                                    <div className="text-base text-foreground leading-relaxed whitespace-pre-line max-h-none overflow-visible">
                                        {analysisData.repo_summary}
                                    </div>
                                </div>
                            )}

                            {/* Tech Stack Display - Moved here for better flow */}
                            {analysisData.tech_stack && (
                                <div className="space-y-4 glass-effect p-6 rounded-lg animate-fade-in">
                                    <h3 className="text-xl font-bold gradient-text">Technology Stack</h3>

                                    {/* AI Analysis */}
                                    {analysisData.tech_stack_analysis && (
                                        <p className="text-sm text-muted-foreground italic border-l-2 border-purple-500 pl-4 py-2">
                                            🤖 {analysisData.tech_stack_analysis}
                                        </p>
                                    )}

                                    {/* Badges */}
                                    <div className="space-y-3">
                                        {analysisData.tech_stack.languages.length > 0 && (
                                            <TechStackBadge
                                                category="Languages"
                                                items={analysisData.tech_stack.languages}
                                            />
                                        )}
                                        {analysisData.tech_stack.frameworks.length > 0 && (
                                            <TechStackBadge
                                                category="Frameworks"
                                                items={analysisData.tech_stack.frameworks}
                                            />
                                        )}
                                        {analysisData.tech_stack.tools.length > 0 && (
                                            <TechStackBadge
                                                category="Tools"
                                                items={analysisData.tech_stack.tools}
                                            />
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* Architecture Diagram */}
                            <GraphViewer
                                mermaidGraph={analysisData.mermaid_graph}
                                repoName={analysisData.repo_name}
                                summary={analysisData.summary}
                            />

                            {/* Chat Interface */}
                            <ChatInterface
                                onSendMessage={handleSendMessage}
                                repoName={analysisData.repo_name}
                            />

                            {/* Files Info */}
                            <div className="text-center text-sm text-muted-foreground">
                                Analyzed {analysisData.total_files} files from {analysisData.repo_name}
                            </div>
                        </>
                    )}
                </div>

                {/* Footer */}
                <footer className="mt-16 text-center text-sm text-muted-foreground">
                    <p>Powered by Gemini • Built for developers who love archaeology</p>
                </footer>
            </div>
        </main>
    );
}
