# Prompt: Frontend Chat Interface Integration for Phase III

## Context
We are implementing the frontend chat interface for the AI-powered todo chatbot in Phase III of The Evolution of Todo project.

## Objective
Create a beautiful, functional chat interface that connects to the backend chat API and provides natural language task management.

## Tasks
1. Create new chat page at `/chat` route
2. Implement real-time messaging interface with message bubbles
3. Integrate with existing Better Auth for authentication
4. Connect to the `/api/{user_id}/chat` endpoint
5. Implement proper loading states and error handling
6. Add navigation between dashboard and chat interfaces
7. Ensure responsive design matching existing UI
8. Implement conversation history display

## Implementation Notes
- Use the same design language as existing dashboard
- Ensure proper authentication token handling
- Implement smooth scrolling to latest messages
- Add typing indicators for AI responses
- Handle conversation state properly
- Include helpful placeholder text and examples

## Acceptance Criteria
- Chat interface is accessible at `/chat` route
- Messages display properly with user/assistant differentiation
- Authentication works seamlessly with Better Auth
- Messages are sent to and received from the backend
- Loading states and error handling are implemented
- Navigation between dashboard and chat works properly
- UI is responsive and matches existing design
- Helpful examples are shown for new users