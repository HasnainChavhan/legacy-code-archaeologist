'use client';

import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';
import { toPng } from 'html-to-image';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download } from 'lucide-react';

interface GraphViewerProps {
    mermaidGraph: string;
    repoName: string;
    summary: string;
}

export default function GraphViewer({ mermaidGraph, repoName, summary }: GraphViewerProps) {
    const mermaidRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const renderDiagram = async () => {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'dark',
                themeVariables: {
                    primaryColor: '#3b82f6',
                    primaryTextColor: '#fff',
                    primaryBorderColor: '#1e40af',
                    lineColor: '#6366f1',
                    secondaryColor: '#8b5cf6',
                    tertiaryColor: '#ec4899',
                },
            });

            if (mermaidRef.current && mermaidGraph) {
                try {
                    const id = `mermaid-${Date.now()}`;
                    const { svg } = await mermaid.render(id, mermaidGraph);
                    mermaidRef.current.innerHTML = svg;
                } catch (error) {
                    console.error('Mermaid rendering error:', error);
                    mermaidRef.current.innerHTML = `<pre>${mermaidGraph}</pre>`;
                }
            }
        };

        renderDiagram();
    }, [mermaidGraph]);

    const exportDiagram = async () => {
        if (mermaidRef.current) {
            try {
                const dataUrl = await toPng(mermaidRef.current, {
                    backgroundColor: '#1a1a2e',
                    quality: 1.0,
                });
                const link = document.createElement('a');
                link.download = `${repoName}-architecture.png`;
                link.href = dataUrl;
                link.click();
            } catch (error) {
                console.error('Export failed:', error);
            }
        }
    };

    return (
        <Card className="w-full glass-effect animate-fade-in">
            <CardHeader>
                <div className="flex items-center justify-between">
                    <div>
                        <CardTitle className="text-2xl font-bold flex items-center gap-2">
                            <span className="gradient-text">{repoName}</span>
                            <span className="text-sm font-normal text-muted-foreground">Architecture</span>
                        </CardTitle>
                        <CardDescription className="text-base">{summary}</CardDescription>
                    </div>
                    <Button
                        onClick={exportDiagram}
                        variant="outline"
                        size="sm"
                        className="gap-2"
                    >
                        <Download className="w-4 h-4" />
                        Export PNG
                    </Button>
                </div>
            </CardHeader>
            <CardContent>
                <div className="bg-background/50 rounded-lg p-6 overflow-auto max-h-[600px]">
                    <div ref={mermaidRef} className="mermaid" />
                </div>
            </CardContent>
        </Card>
    );
}
