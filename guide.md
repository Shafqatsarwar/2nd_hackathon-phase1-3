# 🚀 The Evolution of Todo - Complete Deployment Guide (Phases I, II & III)

## 🌟 Project Overview
This project represents the evolution of a simple CLI Todo list into a full-stack AI-powered Web Application.
- **Frontend**: Next.js 15, TailwindCSS, Framer Motion (Glassmorphic UI)
- **Backend**: FastAPI, SQLModel, Neon (PostgreSQL)
- **Auth**: Better Auth (Secure, Self-hosted logic)
- **AI**: OpenAI Agents with MCP (Model Context Protocol) server architecture (Phase III)

---

## 📋 Phase Overview
- **Phase I**: In-Memory Python Console App
- **Phase II**: Full-Stack Web Application with persistent storage and authentication
- **Phase III**: AI-Powered Chatbot with natural language processing

## 🛠️ Quick Start (Development)

### 1. Start the Backend (The Core)
The backend powers the logic and database connections.
```powershell
cd src/backend
uv run uvicorn main:app --host 0.0.0.0 --port 800 --reload
```
*   **Health Check**: Open `http://localhost:800/health` → `{"status": "healthy"}`
*   **Docs**: Open `http://localhost:800/docs` for Swagger UI.

### Tip: Quickly validate the API
If you hit a 500 from `TaskInterface`, run this curl from project root to confirm the backend is healthy before chasing frontend issues:

```powershell
curl -H "Authorization: Bearer guest_token" http://127.0.0.1:800/api/guest_user/tasks
```

If the response returns JSON, the backend system is up and responding with the expected task list.

### 2. Start the Frontend (The Interface)
The frontend provides the premium user experience.
```powershell
# From project root
npm run dev
```
*   **App**: Open `http://localhost:3000`
*   **Note**: The root `npm run dev` now automatically starts the frontend from its subdirectory. It connects to the backend on port 800.

### 3. Phase III - AI Chatbot Setup
The AI-powered chatbot is fully integrated and functional.
*   **Chat Interface**: Navigate to `http://localhost:3000/chat`
*   **Environment**: Ensure `OPENAI_API_KEY` is set in your `.env.local` or `.env.vercel` file.
*   **Features**: Natural language task management with OpenAI GPT integration.
*   **Status**: The backend implementation provides a robust MCP tool layer for the AI agent to manage your tasks effectively.

---

### 4. 🔐 Master Admin Access (Bypass Login)
For development and demonstration purposes, we have a built-in Master Admin Access.

*   **Master Token**: `admin_token`
*   **How to use (Frontend UI)**:
    1.  Go to the `/dashboard` directly or via the "Start the Evolution" button.
    2.  If prompted with a login, you can use the **special admin login** (if implemented in your local UI) or bypass by setting `admin_access=true` in your browser's LocalStorage.
*   **How to use (API/Swagger)**:
    1.  Go to `https://your-app.vercel.app/docs`.
    2.  Click **Authorize**.
    3.  Enter `admin_token` in the value field.
    4.  Now all `/api/{user_id}/...` requests will treat you as the `admin` user regardless of the `user_id` provided.
*   **Security Note**: This is enabled for the Hackathon Phase II to facilitate easy judging. In a real production app, this would be removed.

---

### 4. � Contribution & CLI
Legacy Phase I CLI tools are preserved in `src/cli`.
To run the original CLI:
```powershell
uv run python src/cli/main.py
# cd src/cli
# uv run main.py
```

---

##  Key Features & Usage

### 1. Guest Mode (The Sandbox)
*   Click the **'G' Badge** in the bottom-right## 📘 Environment Variables Master Class

This section explains every key you need, why you need it, and where to get it.

### 1. `DATABASE_URL` (The Memory)
*   **What it is**: The address where your data lives.
*   **Local Development**: Use `sqlite:///todo.db`. This works instantly and saves data to a file on your laptop.
*   **Production (Cloud)**: You need a cloud database. We recommend **Neon**.
    1.  Go to [Neon Console](https://console.neon.tech).
    2.  Create a Project.
    3.  Copy the **Connection String** (Pooled).
    4.  It looks like: `postgresql://user:pass@ep-host.neon.tech/neondb?sslmode=require`

### 2. `BETTER_AUTH_SECRET` (The Security)
*   **What it is**: A secret password used to encrypt user session cookies.
*   **How to get it**: You generate this yourself.
    *   **Option A**: Run `openssl rand -base64 32` in terminal.
    *   **Option B**: Type a random long string (e.g., `my_super_secure_hackathon_secret_key_2025`).

### 3. `NEXT_PUBLIC_BACKEND_URL` (The Bridge)
*   **What it is**: Tells the Frontend where the Backend lives.
*   **Local**: `http://127.0.0.1:800` (uvicorn runs here and rewrites append `/api` automatically).
*   **Vercel**: `https://your-app-name.vercel.app` (rewrites append `/api`; including `/api` in the variable is optional).

### 4. `NEXT_PUBLIC_BETTER_AUTH_URL` (The Home)
*   **What it is**: The URL of your website itself.
*   **Local**: `http://localhost:3000`
*   **Vercel**: `https://your-app-name.vercel.app`

### 5. `OPENAI_API_KEY` (The AI Engine) - Phase III
*   **What it is**: Your OpenAI API key for the AI-powered chatbot functionality.
*   **How to get it**:
    1. Go to [OpenAI Platform](https://platform.openai.com/)
    2. Navigate to "API Keys" section
    3. Create a new secret key
    4. Copy the key (format: `sk-...`)
*   **Security**: Never commit this key to version control. It's already in `.gitignore`.

---


## 📝 Configuration Cheatsheet

**Scenario A: Running Locally (Copy to `.env`)**
```env
DATABASE_URL="sqlite:///todo.db"
BETTER_AUTH_SECRET="local_dev_secret"
NEXT_PUBLIC_BACKEND_URL="http://127.0.0.1:800"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
OPENAI_API_KEY="sk-...your-openai-api-key-here..."
```

**Scenario B: Deploying to Vercel (Add to Vercel Env Vars)**
```env
DATABASE_URL="postgresql://neondb_owner:..." (From Neon)
BETTER_AUTH_SECRET="complex_random_string"
NEXT_PUBLIC_BACKEND_URL="https://your-app.vercel.app"
NEXT_PUBLIC_BETTER_AUTH_URL="https://your-app.vercel.app"
OPENAI_API_KEY="sk-...your-openai-api-key-here..." (For Phase III AI Chatbot)
```

---

## 🚀 Deploying to Vercel (Combined Frontend + Backend)

This project uses a **unified deployment architecture** where both the Next.js frontend and FastAPI backend are deployed together on Vercel as a single application.

### 🏗️ Architecture Overview

The combined deployment works through these key components:

1. **`api/index.py`** (Root Level)
   - Acts as a bridge/entry point for Vercel serverless functions
   - Imports and exposes the FastAPI app from `src/backend/main.py`
   - Vercel automatically detects this as a Python serverless function

2. **`vercel.json`** (Root Level)
   - Configures URL rewrites to route API requests to the Python backend
   - Routes `/api/*`, `/docs`, and `/openapi.json` to `api/index.py`
   - All other routes are handled by Next.js frontend

3. **`src/frontend/`**
   - Contains the Next.js application
   - Vercel automatically detects and builds this as the main application
   - Frontend makes API calls to `/api/*` which are routed to the backend

### 📂 Deployment File Structure
```text
.
├── api/
│   └── index.py          # Vercel serverless function entry point
├── vercel.json           # Routing configuration
├── src/
│   ├── backend/          # FastAPI application
│   │   ├── main.py       # Main FastAPI app
│   │   └── ...
│   └── frontend/         # Next.js application (build root)
│       ├── app/
│       ├── package.json
│       └── ...
└── pyproject.toml        # Python dependencies
```

### 🔧 Vercel Project Configuration

When setting up your Vercel project:

1. **Root Directory**: Leave as `.` (project root)
2. **Build Command**: Vercel auto-detects from `src/frontend/package.json`
3. **Output Directory**: `.next` (auto-detected)
4. **Install Command**: `npm install` (in `src/frontend`)

### 📝 Environment Variables (Vercel Dashboard)

Add these in your Vercel project settings:

```env
DATABASE_URL=postgresql://neondb_owner:xxxxx@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=your_complex_random_string_here
NEXT_PUBLIC_BACKEND_URL=https://your-app-name.vercel.app
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app-name.vercel.app
```

> [!IMPORTANT]
> - `DATABASE_URL`: Get from [Neon Console](https://console.neon.tech) (use Pooled connection string)
> - `BETTER_AUTH_SECRET`: Generate with `openssl rand -base64 32`
> - `NEXT_PUBLIC_BACKEND_URL`: Your Vercel URL (rewrites add `/api`, so including `/api` is optional)
> - `NEXT_PUBLIC_BETTER_AUTH_URL`: Your Vercel URL

### 🚀 Deployment Steps

#### Option A: Deploy via Vercel Dashboard

1. **Push to GitHub**:
   ```powershell
   git add .
   git commit -m "Ready for deployment"
   git push origin master
   ```

2. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel auto-detects Next.js configuration

3. **Configure Settings**:
   - **Framework Preset**: Next.js
   - **Root Directory**: `./` (leave default)
   - **Build Command**: (leave default - auto-detected)
   - **Output Directory**: (leave default - auto-detected)

4. **Add Environment Variables**:
   - Add all 4 environment variables listed above
   - Make sure to use your actual Neon database URL

5. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)

#### Option B: Deploy via Vercel CLI

**Starting Directory**: Project root (`d:\Panaverse\Hackathon\2nd_hackathon-phase1-2`)

```powershell
# Navigate to project root (if not already there)
cd d:\Panaverse\Hackathon\2nd_hackathon-phase1-2

# Install Vercel CLI (one-time setup)
npm i -g vercel

# Login to Vercel (one-time setup)
vercel login

# Deploy from project root
vercel

# Follow prompts and add environment variables when asked
```

### ✅ Verify Deployment

After deployment, test these endpoints:

1. **Frontend**: `https://your-app.vercel.app`
2. **Backend Health**: `https://your-app.vercel.app/api/health`
3. **API Docs**: `https://your-app.vercel.app/docs`
4. **OpenAPI Spec**: `https://your-app.vercel.app/openapi.json`

### 🧭 Swagger Authorization Help
When you open `/docs` (locally or on Vercel) you can authorize requests with one of the demo tokens:

1. Click the `bearerAuth (http, Bearer)` entry under “Available authorizations”.
2. In the **Value** field paste:
   * `Bearer guest_token` – shared guest vault with read-only data.
   * `Bearer admin_token` – impersonates `khansarwar1@hotmail.com` with full access.
   * `Bearer <your JWT>` – any Better Auth session token exported from the frontend (must share `BETTER_AUTH_SECRET`).
3. Press **Authorize**, then **Close**; Swagger now sends that bearer token with every `/api/{user_id}/*` request until you clear it.

Use the “Try it out” buttons after authorizing to exercise the CRUD/chat endpoints, and copy the Authorization value from Swagger to make sure it matches what the UI is sending if you still see 400/401 responses.

### 🧪 Local Production Build Test

Before deploying, test the production build locally:

```powershell
cd src/frontend
npm run build
npm start
```

### 🔍 Troubleshooting

**Build Fails**:
- Check that all environment variables are set in Vercel dashboard
- Verify `api/index.py` correctly imports from `src.backend.main`
- Ensure `pyproject.toml` includes all Python dependencies

**API Routes Not Working**:
- Verify `vercel.json` rewrites are configured correctly
- Ensure `NEXT_PUBLIC_BACKEND_URL` matches your app host (rewrites add `/api`; including `/api` is still accepted)
- Review Vercel function logs in dashboard

**Database Connection Issues**:
- Ensure using Neon's **Pooled** connection string (not Direct)
- Verify `sslmode=require` is in the connection string
- Check Neon database is not paused/suspended

**Phase III AI Chatbot Issues**:
- Verify `OPENAI_API_KEY` is correctly set in environment variables
- Check that your OpenAI account has sufficient credits
- Ensure the chat endpoint `/api/{user_id}/chat` is accessible
- Confirm that MCP server dependencies are properly installed

### 🔐 Master Admin Access (Bypass Login)
For development and demonstration purposes, we have a built-in Master Admin Access.

*   **Prebuilt Admin Account**: 
    *   **Email**: `khansarwar1@hotmail.com`
    *   **Role**: Admin
*   **Master Token**: `admin_token`
*   **How to use (Frontend UI)**:
    1.  Go to the Dashboard.
    2.  If not logged in, you can manually set the local storage key `better-auth.session-token` to `admin_token` OR use the "Guest Access" link if available which uses this token.
    3.  The backend will automatically recognize this token and provide full access to the `admin` account seeded on startup.

## 🏛️ Architecture & Standards
This project follows strict **Agentic Development** principles.

*   **Isolation**: Logic is separated into `src/cli`, `src/backend`, and `src/frontend`.
*   **SDD Loop**: All features are Spec-Driven. See `specs/` for architectural decisions.
*   **Security**: Use path/JWT based user isolation in all API endpoints.
---

## 📤 Pushing to GitHub

1. **Create Repository**: Go to GitHub and create a new repository (e.g., `evolution-of-todo`).

2. **Push Code**:
   ```powershell
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M master
   git push -u origin master
   ```

3. **Next Steps**: After pushing, you can deploy to Vercel (see deployment section above).
