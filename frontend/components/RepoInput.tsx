'use client';

import React, { useState } from 'react';
import { Github, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface RepoInputProps {
    onSubmit: (repoUrl: string) => void;
    isLoading: boolean;
}

export default function RepoInput({ onSubmit, isLoading }: RepoInputProps) {
    const [repoUrl, setRepoUrl] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (repoUrl.trim()) {
            onSubmit(repoUrl.trim());
        }
    };

    return (
        <Card className="w-full max-w-2xl glass-effect glow-border">
            <CardHeader className="text-center">
                <CardTitle className="text-4xl font-bold gradient-text mb-2">
                    Legacy Code Archaeologist
                </CardTitle>
                <CardDescription className="text-lg">
                    Unearth the secrets of any codebase with AI-powered visualization
                </CardDescription>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex flex-col space-y-2">
                        <label htmlFor="repo-url" className="text-sm font-medium text-muted-foreground">
                            GitHub Repository URL
                        </label>
                        <div className="flex gap-2">
                            <div className="relative flex-1">
                                <Github className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-5 w-5" />
                                <Input
                                    id="repo-url"
                                    type="text"
                                    placeholder="https://github.com/username/repository"
                                    value={repoUrl}
                                    onChange={(e) => setRepoUrl(e.target.value)}
                                    disabled={isLoading}
                                    className="pl-10 h-12 text-base"
                                />
                            </div>
                            <Button
                                type="submit"
                                disabled={isLoading || !repoUrl.trim()}
                                className="h-12 px-8 text-base font-semibold"
                            >
                                {isLoading ? (
                                    <>
                                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                        Excavating...
                                    </>
                                ) : (
                                    'Analyze'
                                )}
                            </Button>
                        </div>
                    </div>

                    <div className="pt-4 border-t border-border">
                        <p className="text-xs text-muted-foreground text-center">
                            Try examples:
                            <button
                                type="button"
                                onClick={() => setRepoUrl('https://github.com/facebook/react')}
                                className="ml-2 text-primary hover:underline"
                                disabled={isLoading}
                            >
                                facebook/react
                            </button>
                            {' • '}
                            <button
                                type="button"
                                onClick={() => setRepoUrl('https://github.com/vercel/next.js')}
                                className="text-primary hover:underline"
                                disabled={isLoading}
                            >
                                vercel/next.js
                            </button>
                        </p>
                    </div>
                </form>
            </CardContent>
        </Card>
    );
}
