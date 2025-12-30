# Vercel Deployment Checklist

## Pre-Deployment Verification

### 1. Code Structure
- [x] `api/index.py` exists and properly bridges to backend
- [x] `vercel.json` exists with correct rewrites
- [x] `src/frontend` contains Next.js application
- [x] `src/backend` contains FastAPI application
- [x] `pyproject.toml` contains all Python dependencies
- [x] `src/frontend/package.json` contains all frontend dependencies

### 2. Environment Variables
- [x] `BETTER_AUTH_SECRET` - Shared secret for JWT
- [x] `DATABASE_URL` - PostgreSQL connection string (Neon DB)
- [x] `NEXT_PUBLIC_BACKEND_URL` - Backend API host (`/api` appended automatically)
- [x] `NEXT_PUBLIC_BETTER_AUTH_URL` - Auth URL

### 3. API Endpoints
- [x] `/api/{user_id}/tasks` - List tasks
- [x] `/api/{user_id}/tasks` - Create task
- [x] `/api/{user_id}/tasks/{id}` - Get task
- [x] `/api/{user_id}/tasks/{id}` - Update task
- [x] `/api/{user_id}/tasks/{id}` - Delete task
- [x] `/api/{user_id}/tasks/{id}/complete` - Toggle completion
- [x] `/api/health` - Health check
- [x] `/docs` - API documentation
- [x] `/openapi.json` - OpenAPI specification

### 4. Authentication
- [x] Better Auth configured in frontend
- [x] JWT verification in backend
- [x] User isolation implemented
- [x] Admin access token available for testing

### 5. Frontend
- [x] Next.js App Router used
- [x] Proper API URL configuration
- [x] Authentication flow implemented
- [x] Task management UI functional

### 6. Backend
- [x] FastAPI application structure
- [x] SQLModel database integration
- [x] Proper error handling
- [x] Authentication middleware
- [x] User-specific data filtering

### 7. MCP Integration
- [x] MCP configuration files in `.claude/`
- [x] Better Auth MCP tools defined
- [x] Integration documentation created

### 8. Specifications
- [x] Phase I specs in `specs/001-add-task/`
- [x] Phase II architecture specs in `specs/phase-ii-architecture/`
- [x] Phase III AI chatbot specs in `specs/phase-iii-ai-chatbot/`
- [x] Intermediate features specs in `specs/intermediate-features/`
- [x] Advanced features specs in `specs/advanced-features/`
- [x] Constitution compliance verified

### 9. Testing
- [x] Backend tests passing
- [x] Frontend functionality verified
- [x] Authentication flow tested
- [x] API endpoints tested
- [x] Database connectivity verified

## Deployment Steps

### 1. Environment Setup
1. Create Neon PostgreSQL database
2. Get database connection string (pooled)
3. Generate `BETTER_AUTH_SECRET` (32+ character random string)
4. Prepare URLs for environment variables

### 2. Vercel Configuration
1. Push code to GitHub repository
2. Import project to Vercel
3. Set framework preset to Next.js
4. Set root directory to `./`
5. Add environment variables to Vercel dashboard

### 3. Environment Variables for Vercel
```
DATABASE_URL=postgresql://user:pass@ep-host.region.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your_32_plus_character_random_string
NEXT_PUBLIC_BACKEND_URL=https://your-app-name.vercel.app
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app-name.vercel.app
```

### 4. Post-Deployment Verification
1. Visit frontend: `https://your-app-name.vercel.app`
2. Check backend health: `https://your-app-name.vercel.app/api/health`
3. Verify API docs: `https://your-app-name.vercel.app/docs`
4. Test API functionality with auth
5. Verify user isolation works properly

## Rollback Plan
- If deployment fails, revert to previous version in Vercel dashboard
- If environment variables are incorrect, update them in Vercel settings
- If database connectivity fails, verify Neon DB connection string

## Success Criteria
- [ ] Frontend loads without errors
- [ ] Backend API endpoints are accessible
- [ ] Authentication works properly
- [ ] Tasks can be created, read, updated, and deleted
- [ ] User isolation is maintained
- [ ] Admin access token works for testing
- [ ] API documentation is accessible
- [ ] Health check returns healthy status

## Deployment Troubleshooting

### Common Issues and Solutions

#### 1. Pydantic-core Build Issues
**Problem**: `pydantic-core` fails to build during deployment with Rust compilation errors.
**Solution**: Use specific Pydantic version that has pre-compiled wheels available for the deployment platform.

**Files updated**:
- `src/backend/pyproject.toml` - Changed to `pydantic==2.4.2`
- `pyproject.toml` - Changed to `pydantic==2.4.2`
- `requirements.txt` - Changed to `pydantic==2.4.2`

#### 2. Node.js/Next.js Conflicts
**Problem**: Version conflicts between root and frontend dependencies.
**Solution**: Clean up root package.json to avoid dependency conflicts with frontend workspace.

**Files updated**:
- `package.json` - Removed direct frontend dependencies, added engines specification

#### 3. Dependency Resolution
**Problem**: Vercel may have issues resolving complex Python dependencies.
**Solution**: Maintain explicit `requirements.txt` with compatible versions for critical dependencies.

**Files updated**:
- `requirements.txt` - Complete list of dependencies with compatible versions

#### 4. Python Version Compatibility
**Problem**: Inconsistent Python versions between local and deployment environment.
**Solution**: Updated runtime requirements to ensure compatibility.

**Files updated**:
- `src/backend/pyproject.toml` - Updated to `>=3.12`
- `pyproject.toml` - Updated to `>=3.12`
- `runtime.txt` - Specifies `python-3.12.0`

### Verification Steps After Fix
1. Confirm the specific Pydantic version (2.4.2) is used to ensure pre-built wheels
2. Verify `requirements.txt` contains all necessary dependencies
3. Test local deployment with updated dependencies
4. Retry Vercel deployment
