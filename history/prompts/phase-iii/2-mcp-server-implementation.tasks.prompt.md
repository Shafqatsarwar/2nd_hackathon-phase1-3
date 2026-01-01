# Prompt: MCP Server Implementation for Phase III

## Context
We are implementing the MCP (Model Context Protocol) server for the AI-powered todo chatbot in Phase III of The Evolution of Todo project.

## Objective
Create a complete MCP server with all required tools for task operations that can be used by AI agents to interact with the todo system.

## Tasks
1. Implement MCP server with Official MCP SDK
2. Create tools for all task operations:
   - `add_task`: Create new tasks via natural language
   - `list_tasks`: Retrieve and display tasks
   - `complete_task`: Mark tasks as complete
   - `delete_task`: Remove tasks from the list
   - `update_task`: Modify existing tasks
3. Ensure tools are stateless and database-backed
4. Add proper error handling to all tools
5. Implement proper authentication and user isolation in tools
6. Test all tools individually

## Implementation Notes
- Tools should use the existing database models and session management
- All operations must verify user permissions
- Error messages should be user-friendly
- Tools should return consistent response formats

## Acceptance Criteria
- MCP server starts without errors
- All 5 tools are registered with the server
- Tools properly interact with the database
- User isolation is maintained (user A cannot access user B's tasks)
- Proper error handling is implemented