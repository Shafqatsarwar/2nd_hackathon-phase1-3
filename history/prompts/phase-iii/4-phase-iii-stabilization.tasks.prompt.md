# Prompt: Phase III Stabilization & Documentation

## Context
Phase III is currently tracking its AI-native objectives, but the MCP tooling stack in the monorepo was temporarily causing runtime failures because the pinned `modelcontextprotocol` version (0.3.0) no longer exists. A lightweight MCP stub was introduced to keep the chat experience live while we resolve the dependency surge.

## Objective
1. Align the repository with the constitutional requirements: keep all specs and documentation in sync, make every public-facing doc mention the current in-progress state, and document how to run the API now that the MCP tooling is stubbed.
2. Fix the dependency metadata so `uv install`/`uv lock` can resolve the `modelcontextprotocol` release that is actually published.
3. Record the stabilizing work in the Phase III prompt history so future agents know that this step is completed.

## Tasks
- Update `requirements.txt`, `pyproject.toml`, and `src/backend/pyproject.toml` to require `modelcontextprotocol>=1.0.1`, then regenerate `uv.lock`.
- Describe the current Phase III state in `README.md` and `guide.md`, emphasize the placeholder MCP implementation, and link the documentation back to `history/prompts/phase-iii`.
- Add this prompt history record so each stabilization step is tracked under `.specify/memory`.

## Tests
- `npm run lint`
- `uv run python -c "import main"` inside `src/backend`
- `uv run uvicorn main:app --host 0.0.0.0 --port 800 --reload` (manual, confirms startup log without MCP import errors)
