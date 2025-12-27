'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

export default function LoadingState() {
    return (
        <div className="flex flex-col items-center justify-center space-y-6 py-12">
            <motion.div
                animate={{
                    scale: [1, 1.2, 1],
                    rotate: [0, 180, 360],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="relative"
            >
                <Loader2 className="h-16 w-16 text-primary animate-spin" />
                <div className="absolute inset-0 animate-pulse-glow rounded-full" />
            </motion.div>

            <div className="text-center space-y-2">
                <motion.h3
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="text-2xl font-bold gradient-text"
                >
                    Excavating Repository...
                </motion.h3>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.4 }}
                    className="space-y-1"
                >
                    <p className="text-sm text-muted-foreground">Fetching files from GitHub</p>
                    <p className="text-sm text-muted-foreground">Analyzing code structure</p>
                    <p className="text-sm text-muted-foreground">Generating visualization</p>
                </motion.div>
            </div>

            <motion.div
                className="flex gap-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
            >
                {[0, 1, 2].map((i) => (
                    <motion.div
                        key={i}
                        className="w-3 h-3 bg-primary rounded-full"
                        animate={{
                            y: [0, -10, 0],
                        }}
                        transition={{
                            duration: 0.6,
                            repeat: Infinity,
                            delay: i * 0.2,
                        }}
                    />
                ))}
            </motion.div>
        </div>
    );
}
