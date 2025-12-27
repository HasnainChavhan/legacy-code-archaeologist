'use client';

import React, { useState } from 'react';
import { Send, Loader2, FileCode } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import type { ChatResponse } from '@/lib/api';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    relevantFiles?: string[];
    codeSnippets?: Array<{
        file: string;
        lines: string;
        snippet: string;
        explanation: string;
    }>;
}

interface ChatInterfaceProps {
    repoName: string;
    onSendMessage: (message: string) => Promise<any>;
}

export default function ChatInterface({ onSendMessage, repoName }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await onSendMessage(input);
            const assistantMessage: Message = {
                role: 'assistant',
                content: response.answer,
                relevantFiles: response.relevant_files,
                codeSnippets: response.code_snippets,
            };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            const errorMessage: Message = {
                role: 'assistant',
                content: 'Sorry, I encountered an error processing your question. Please try again.',
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <Card className="w-full glass-effect animate-fade-in">
            <CardHeader>
                <CardTitle className="text-xl font-bold">Ask About the Code</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {/* Messages */}
                <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
                    {messages.length === 0 ? (
                        <div className="text-center text-muted-foreground py-8">
                            <p className="text-lg mb-2">Start exploring the codebase!</p>
                            <p className="text-sm">Try asking:</p>
                            <ul className="text-sm mt-2 space-y-1">
                                <li>• "Where is the authentication logic?"</li>
                                <li>• "Explain the data flow in this application"</li>
                                <li>• "Are there any potential bugs or issues?"</li>
                            </ul>
                        </div>
                    ) : (
                        messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-[80%] rounded-lg p-4 ${message.role === 'user'
                                        ? 'bg-primary text-primary-foreground'
                                        : 'bg-muted'
                                        }`}
                                >
                                    <p className="whitespace-pre-wrap">{message.content}</p>

                                    {/* Relevant Files */}
                                    {message.relevantFiles && message.relevantFiles.length > 0 && (
                                        <div className="mt-3 pt-3 border-t border-border/50">
                                            <p className="text-xs font-semibold mb-2 flex items-center gap-1">
                                                <FileCode className="h-3 w-3" />
                                                Relevant Files:
                                            </p>
                                            <div className="flex flex-wrap gap-1">
                                                {message.relevantFiles.map((file, i) => (
                                                    <span
                                                        key={i}
                                                        className="text-xs bg-background/50 px-2 py-1 rounded"
                                                    >
                                                        {file}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Code Snippets */}
                                    {message.codeSnippets && message.codeSnippets.length > 0 && (
                                        <div className="mt-3 space-y-3">
                                            {message.codeSnippets.map((snippet, i) => (
                                                <div key={i} className="bg-background/50 rounded p-2">
                                                    <p className="text-xs font-semibold mb-1">
                                                        {snippet.file} (Lines {snippet.lines})
                                                    </p>
                                                    <SyntaxHighlighter
                                                        language="javascript"
                                                        style={vscDarkPlus}
                                                        customStyle={{
                                                            margin: 0,
                                                            borderRadius: '4px',
                                                            fontSize: '0.75rem',
                                                        }}
                                                    >
                                                        {snippet.snippet}
                                                    </SyntaxHighlighter>
                                                    <p className="text-xs mt-2 text-muted-foreground">
                                                        {snippet.explanation}
                                                    </p>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))
                    )}

                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="bg-muted rounded-lg p-4">
                                <Loader2 className="h-5 w-5 animate-spin" />
                            </div>
                        </div>
                    )}
                </div>

                {/* Input */}
                <div className="flex gap-2">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask a question about the code..."
                        disabled={isLoading}
                        className="flex-1"
                    />
                    <Button onClick={handleSend} disabled={isLoading || !input.trim()}>
                        <Send className="h-4 w-4" />
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}
