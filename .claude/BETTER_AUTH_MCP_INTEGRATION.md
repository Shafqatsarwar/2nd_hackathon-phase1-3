# Better Auth MCP Integration Guide

## Overview
This project integrates Better Auth with Claude Code using Model Context Protocol (MCP) to enable enhanced development capabilities around authentication features.

## Configuration Files

### `.claude/mcp-config.json`
- Defines MCP tools for Better Auth operations
- Provides Claude Code with authentication-related functions
- Enables Claude to interact with Better Auth endpoints

### `.claude/project-config.json`
- Project-level configuration for Claude Code
- Defines Better Auth integration settings
- Specifies environment variables and file locations

## Better Auth Setup

### Frontend Integration
- Located at: `src/frontend/auth_v3.ts`
- Uses Better Auth with JWT plugin
- Supports both SQLite and PostgreSQL databases
- Handles build/static generation phases appropriately

### API Routes
- Located at: `src/frontend/app/api/auth/[...better-auth]/route.ts`
- Uses Next.js handler for Better Auth
- Provides standard authentication endpoints

### Backend Integration
- Located at: `src/backend/auth_utils.py`
- JWT verification utilities
- Integration with FastAPI security dependencies
- Shared secret handling between frontend and backend

## Environment Variables

### Frontend (.env.local)
- `NEXT_PUBLIC_BACKEND_URL`: Backend API URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth URL
- `BETTER_AUTH_SECRET`: Shared authentication secret
- `DATABASE_URL`: Database connection string

### Backend (.env.backend)
- `DATABASE_URL`: Database connection string
- `BETTER_AUTH_SECRET`: Shared authentication secret

## API Endpoints

### Better Auth Endpoints
- `/api/auth/...` - Standard Better Auth routes
- Handles sign-in, sign-up, session management

### Backend Task API (with Auth)
- `GET /api/{user_id}/tasks` - List user tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

## MCP Tools Available

### better_auth_client
- Perform authentication operations (sign_in, sign_up, etc.)
- Manage user sessions and credentials

### better_auth_api
- Call Better Auth API endpoints directly
- Perform HTTP operations against auth endpoints

### better_auth_manager
- Create user sessions
- Validate tokens
- Refresh sessions
- Logout users

### auth_debugger
- Check authentication state
- Inspect cookies
- Validate JWT tokens
- Test auth flows

## Development Workflow

When working with authentication features:

1. Claude Code will use MCP tools to understand the auth system
2. Environment variables are validated through MCP
3. Authentication flows can be tested using built-in tools
4. API endpoints are documented and accessible through Claude

## Testing

The integration includes:
- Backend tests in `src/backend/test_api.py`
- Frontend auth functionality in `src/frontend/auth_v3.ts`
- Proper error handling and validation