# Evolution of Todo - Project Structure

This document provides a high-level overview of the project's architecture, organized as a modern Monorepo containing a Next.js Frontend and a FastAPI Backend.

## 📂 Root Directory
The entry point for the application, configuration, and deployments.

| File / Folder | Description |
| :--- | :--- |
| **`src/frontend/`** | The Next.js 15 application source code. |
| **`src/backend/`** | The FastAPI (Python) application source code. |
| **`api/`** | Vercel Serverless Function bridge (Connects Vercel to FastAPI). |
| **`vercel.json`** | Vercel deployment configuration (routes, builds, rewrites). |
| **`package.json`** | Root Node.js configuration (Workspace management). |
| **`pyproject.toml`** | Python dependency management (uv/pip). |
| **`components/`** | Shared UI components (if applicable). |
| **`history/`** | Project conversation logs and memory archives. |
| **`guide.md`** | Comprehensive setup and deployment guide. |
| **`ENVIRONMENT.md`** | Environment variable documentation template. |

---

## 🖥️ Frontend Architecture (`src/frontend`)
Built with **Next.js 15**, **React 19**, **TailwindCSS**, and **Better Auth**.

```text
src/frontend/
├── app/                  # Next.js App Router
│   ├── api/              # Frontend API routes (e.g., /api/auth/)
│   ├── auth/             # Authentication pages (Sign In / Sign Up)
│   ├── dashboard/        # Protected User Dashboard
│   ├── globals.css       # Global Tailwind styles
│   ├── layout.tsx        # Root layout with Metadata & Fonts
│   └── page.tsx          # Landing Page (Hero Section)
├── components/           # Reusable UI Components
│   ├── TaskInterface.tsx # Main Task Management UI
│   ├── SignOutButton.tsx # Auth State Management
│   └── GuestButton.tsx   # Quick Access Action
├── lib/                  # Utilities & Configurations
│   └── auth.ts           # Better Auth configuration
├── auth_v3.ts            # Build-Safe Auth Configuration (Vercel-optimized)
└── public/               # Static assets (images, icons)
```

---

## ⚙️ Backend Architecture (`src/backend`)
Built with **FastAPI**, **SQLModel**, **PostgreSQL (Neon)**, and **Typer**.

```text
src/backend/
├── main.py               # FastAPI Application Entry & Routing
├── models.py             # Database Schema (Users, Tasks)
├── connection.py         # Database Connection Logic (Pooling)
├── tests/                # Pytest Test Suite
└── requirements.txt      # Python Dependencies (if not using pyproject.toml)
```

---

## 🚀 Deployment & Config (`Root`)
Configuration files ensuring seamless Full-Stack deployment on Vercel.

- **`vercel.json`**: orchestrates the build process, directing `/api/*` traffic to the Python backend and serving the Next.js frontend statically.
- **`flatten_project.py` (Archived)**: Utility used to optimize structure for Vercel.
- **`api/index.py`**: The "Bridge" file. Vercel looks here to start the Python serverless function.

---
**Hackathon Submission Info**
- **Phase**: 2 (Full Stack Integration)
- **Stack**: Next.js 15 + FastAPI + Neon DB
- **Focus**: Authentication, CRUD, and Seamless Deployment.
