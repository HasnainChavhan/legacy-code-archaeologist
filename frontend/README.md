# Legacy Code Archaeologist - Frontend

Next.js frontend for the Legacy Code Archaeologist application.

## Prerequisites

- Node.js 18+ and npm
- Backend server running (see `../backend/README.md`)

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Edit `.env.local` if your backend runs on a different URL.

3. **Run development server:**
   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Features

- **Repository Analysis**: Enter any GitHub URL to analyze the codebase
- **Interactive Visualization**: View Mermaid.js diagrams of code architecture
- **AI Chat**: Ask questions about the codebase and get detailed answers
- **Code Snippets**: See relevant code snippets with explanations
- **Dark Theme**: Beautiful dark mode UI with glassmorphism effects

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main page
│   └── globals.css         # Global styles
├── components/
│   ├── ui/                 # Reusable UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── card.tsx
│   ├── RepoInput.tsx       # Repository URL input
│   ├── GraphViewer.tsx     # Mermaid graph visualization
│   ├── ChatInterface.tsx   # Chat component
│   └── LoadingState.tsx    # Loading animation
├── lib/
│   ├── api.ts              # API client
│   └── utils.ts            # Utility functions
└── package.json
```

## Building for Production

```bash
npm run build
npm start
```

## Technologies Used

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Shadcn/UI**: High-quality UI components
- **Mermaid.js**: Diagram visualization
- **Framer Motion**: Smooth animations
- **Axios**: HTTP client
