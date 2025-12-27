'use client';

import React from 'react';

interface TechStackBadgeProps {
    category: string;
    items: string[];
}

export default function TechStackBadge({ category, items }: TechStackBadgeProps) {
    if (!items || items.length === 0) return null;

    const getCategoryColor = (cat: string) => {
        switch (cat.toLowerCase()) {
            case 'languages':
                return 'bg-blue-500/20 text-blue-300 border-blue-500/50';
            case 'frameworks':
                return 'bg-purple-500/20 text-purple-300 border-purple-500/50';
            case 'tools':
                return 'bg-green-500/20 text-green-300 border-green-500/50';
            default:
                return 'bg-gray-500/20 text-gray-300 border-gray-500/50';
        }
    };

    return (
        <div className="flex flex-wrap gap-2 items-center">
            <span className="text-sm font-semibold text-muted-foreground">
                {category}:
            </span>
            {items.map((item, index) => (
                <span
                    key={index}
                    className={`px-3 py-1 rounded-full text-xs font-medium border ${getCategoryColor(category)} transition-all hover:scale-105`}
                >
                    {item}
                </span>
            ))}
        </div>
    );
}
