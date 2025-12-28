# CLAUDE.md - The Evolution of Todo

## Project Overview
This is the "The Evolution of Todo" project, implementing a todo application that evolves from a simple CLI tool to a full-stack web application with AI capabilities. This project follows the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

## Spec-Driven Development (SDD) Workflow
All development in this project follows the SDD principles:
- Specifications are stored in `/specs/`
- Implementation plans are in `/specs/plan.md` files
- Tasks are defined in `/specs/tasks.md` files
- All code is generated via Claude Code based on these specs

## Project Structure
- `/specs` - Feature specifications and architectural plans
- `/src` - Verified source code
- `/src/cli` - Phase I: In-Memory Python CLI App
- `/src/backend` - Phase II: Python FastAPI service
- `/src/frontend` - Phase II: Next.js application
- `/api/index.py` - Vercel serverless entry point
- `/history` - Prompt History Records (PHR) and ADRs

## Architecture
- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT-based)

## API Endpoints (Phase II)
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Development Workflow
1. Create specification in `/specs/`
2. Generate plan based on specification
3. Break plan into tasks
4. Implement via Claude Code
5. No manual editing of generated source code in `src/`

## Environment Configuration
- Database configuration via `DATABASE_URL`
- Authentication via `BETTER_AUTH_SECRET`
- Backend URL via `NEXT_PUBLIC_BACKEND_URL`
- Auth URL via `NEXT_PUBLIC_BETTER_AUTH_URL`

## Deployment
- Unified Vercel deployment for both frontend and backend
- API routes are handled by `api/index.py` which bridges to FastAPI backend
- Frontend routes handled by Next.js App Router

## Compliance with Constitution
- All development starts with specification
- No manual code editing in `src/` directory
- Uses Claude Code and Spec-Kit Plus as primary tools
- Follows the Agentic Dev Stack workflow