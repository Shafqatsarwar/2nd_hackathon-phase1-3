# The Evolution of Todo

This project documents the complete evolution of a Todo application from a simple local CLI to a cloud-native, full-stack web system with AI capabilities. This **Product Architect** demonstration showcases three complete phases built strictly using Agentic Dev Stack principles.

## 📜 Constitution & Rules
All development is governed by the [Constitution](./constitution.md) and tracked in the `.specify/memory/` folder.
- **Mandate**: No manual coding allowed. All code is generated via Specs and Plans.
- **Structure**:
  - `.specify/memory/`: Memory files for Claude Code context.
  - `.specify/history/`: Prompt History Records (PHR) and ADRs.
  - `specs/`: Feature specifications and architectural plans.
  - `src/`: Verified source code.

## 🚀 Phases

### Phase I: In-Memory Python CLI
A command-line tool for managing tasks in local memory.
- **Run**: `uv run src/cli/main.py`
- **Package Manager**: UV

### Phase II: Full-Stack Web App (FastAPI + Next.js)
A multi-user system with persistent storage (Neon PostgreSQL) and JWT Authentication (Better Auth).
- **Backend**: Python FastAPI + SQLModel (Port 800).
- **Frontend**: Next.js 15+ (App Router, Port 3000).
- **Deployment**: Unified Vercel deployment (frontend + backend combined).
- **Setup**: See [guide.md](./guide.md) for detailed instructions.

### Phase III: AI-Powered Todo Chatbot (Completed)
An AI chatbot interface using OpenAI Agents SDK and MCP (Model Context Protocol) server architecture.
- **Frontend**: OpenAI ChatKit style beautiful chat interface at `/chat`.
- **Backend**: Python FastAPI + OpenAI Agents SDK with MCP tools.
- **MCP Server**: Lightweight implementation that provides task management tools to the AI agent.
- **Features**: Natural language task management (add, list, complete, delete, update); conversational persistence in database.
- **State**: Use the `guest_token`, `admin_token`, or a Better Auth-issued JWT via `/auth` when exercising `/api/{user_id}` routes. Refer to `guide.md` for deployment steps.

### Intermediate & Advanced Features (Planned)
- **Intermediate**: Priorities, Tags, Search, Filter, Sort (see `specs/intermediate-features/`)
- **Advanced**: Recurring Tasks, Due Dates & Reminders (see `specs/advanced-features/`)

## 📁 Repository Structure
```text
.
├── api/
│   └── index.py               # Vercel serverless entry point (bridges to backend)
├── .claude/                   # Claude Code MCP configuration
│   ├── mcp-config.json        # MCP tools for Better Auth
│   ├── project-config.json    # Project configuration for Claude
│   └── settings.json          # Claude Code settings
├── .specify/                  # Claude Code memory and history
│   ├── memory/                # Current context for Claude
│   └── history/               # Prompt History Records (PHR) and ADRs
├── specs/                     # SDD Specifications
│   ├── 001-add-task/          # Phase I: Add Task feature
│   ├── phase-ii-architecture/ # Phase II: Architecture specifications
│   ├── phase-iii-ai-chatbot/  # Phase III: AI Chatbot specifications
│   ├── intermediate-features/ # Intermediate features specifications
│   └── advanced-features/     # Advanced features specifications
├── src/
│   ├── cli/                   # Phase I CLI App
│   ├── backend/               # Phase II FastAPI service
│   └── frontend/              # Phase II Next.js application
├── vercel.json                # Vercel routing configuration
├── constitution.md            # Governing Rules
├── CLAUDE.md                  # Claude Code instructions
├── guide.md                   # Setup and deployment guide
└── pyproject.toml             # Project Workspace
```

## 🚀 Deployment Architecture

This project uses a **unified deployment** approach on Vercel:
- **Frontend & Backend Combined**: Both deployed as a single Vercel application
- **`api/index.py`**: Bridges Vercel serverless functions to FastAPI backend
- **`vercel.json`**: Routes `/api/*` requests to Python backend, all other routes to Next.js
- **Result**: Single URL serves both frontend UI and backend API

**Live Endpoints** (after deployment):
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-app.vercel.app/api/*`
- API Docs: `https://your-app.vercel.app/docs`

## 🤖 MCP Integration

This project includes Model Context Protocol (MCP) integration for Claude Code:
- **Better Auth MCP Tools**: Pre-configured tools for authentication operations
- **Project Context**: Claude Code understands the project structure and specifications
- **Enhanced Development**: Claude can interact with authentication system directly

## 📋 Deployment Checklist

See [VERCEL_DEPLOYMENT_CHECKLIST.md](./VERCEL_DEPLOYMENT_CHECKLIST.md) for a complete checklist before deploying to Vercel.

## 🚀 Quick Deployment to Vercel

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Configure as Next.js project with root directory `./`
   - Add environment variables (see guide.md)

3. **Set Environment Variables**:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: 32+ character random string
   - `NEXT_PUBLIC_BACKEND_URL`: `https://your-app.vercel.app` (rewrites add `/api`, so including `/api` is optional)
   - `NEXT_PUBLIC_BETTER_AUTH_URL`: `https://your-app.vercel.app`
   - `OPENAI_API_KEY`: OpenAI API key for Phase III AI chatbot functionality

4. **Verify Deployment**:
   - Frontend: `https://your-app-name.vercel.app`
   - API Health: `https://your-app-name.vercel.app/api/health`
   - API Docs: `https://your-app-name.vercel.app/docs`

See [guide.md](./guide.md) for complete deployment instructions.
