"use client";

import { useState, useRef, useEffect } from "react";
import { createAuthClient } from "better-auth/react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import SignOutButton from "../../components/SignOutButton";

const authClient = createAuthClient();

export default function ChatPage() {
    const [session, setSession] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [messages, setMessages] = useState<{id: number, role: string, content: string, timestamp: Date}[]>([]);
    const [inputMessage, setInputMessage] = useState("");
    const [isSending, setIsSending] = useState(false);
    const router = useRouter();
    const messagesEndRef = useRef<null | HTMLDivElement>(null);

    useEffect(() => {
        async function init() {
            // Check for special Admin login first
            const isAdmin = localStorage.getItem("admin_access") === "true";
            if (isAdmin) {
                setSession({
                    user: { id: "admin", name: "Khan Sarwar", email: "khansarwar1@hotmail.com" },
                    token: "admin_token"
                });
                setLoading(false);
                return;
            }

            const { data } = await authClient.getSession();
            if (!data) {
                router.push("/auth");
                return;
            }
            setSession(data);
            setLoading(false);
        }
        init();
    }, [router]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSendMessage = async () => {
        if (!inputMessage.trim() || !session || isSending) return;

        const userMessage = {
            id: Date.now(),
            role: "user",
            content: inputMessage,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage("");
        setIsSending(true);

        try {
            const userId = session.user.id;
            const token = session.token;

            // Find the most recent conversation ID or use the first one if any exist
            const conversationId = messages.length > 0 ? findConversationId() : undefined;

            const response = await fetch(`/api/${userId}/chat`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    message: inputMessage,
                    conversation_id: conversationId
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            const assistantMessage = {
                id: Date.now() + 1,
                role: "assistant",
                content: data.response,
                timestamp: new Date()
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error("Error sending message:", error);
            const errorMessage = {
                id: Date.now() + 1,
                role: "assistant",
                content: "Sorry, I encountered an error processing your request. Please try again.",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsSending(false);
        }
    };

    // Helper function to find conversation ID (in a real implementation, you'd track this properly)
    const findConversationId = () => {
        // This is a simplified approach - in a real app you'd track conversation IDs properly
        return undefined; // Let the backend create a new conversation or use the most recent one
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    if (loading) return (
        <div className="min-h-screen bg-neutral-950 flex items-center justify-center">
            <div className="w-16 h-16 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin" />
        </div>
    );

    const userId = session?.user.id;
    const token = session?.token;

    return (
        <div className="min-h-screen bg-neutral-950 text-slate-200 font-sans p-4 md:p-12 relative overflow-hidden">
            {/* Background accents */}
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-purple-600/10 blur-[150px] -z-10" />
            <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-600/10 blur-[150px] -z-10" />

            <div className="max-w-5xl mx-auto z-10 relative">
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-16 gap-6">
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-xs font-bold uppercase tracking-[0.2em] text-purple-400">Phase III</span>
                            <div className="h-[1px] w-8 bg-purple-500/30" />
                        </div>
                        <h1 className="text-5xl font-black text-white tracking-tight">
                            AI Todo Assistant
                        </h1>
                        <p className="text-slate-500 mt-2 text-lg">
                            Chat with your AI assistant to manage tasks naturally.
                        </p>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="text-right hidden md:block">
                            <p className="text-sm font-bold text-white">{session?.user.name}</p>
                            <p className="text-xs text-slate-500">{session?.user.email}</p>
                        </div>
                        <SignOutButton />
                    </div>
                </header>

                <div className="mb-8">
                    <div className="flex space-x-4 overflow-x-auto pb-2">
                        <Link
                            href="/dashboard"
                            className="px-4 py-2 rounded-lg border border-white/10 text-slate-300 hover:bg-white/5 whitespace-nowrap"
                        >
                            Tasks
                        </Link>
                        <Link
                            href="/chat"
                            className="px-4 py-2 rounded-lg bg-purple-600/20 border border-purple-500/30 text-purple-300 whitespace-nowrap"
                        >
                            AI Chat
                        </Link>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-12">
                    <section className="relative">
                        <div className="bg-neutral-900/50 backdrop-blur-xl border border-white/10 rounded-2xl p-6 min-h-[60vh] max-h-[60vh] flex flex-col">
                            <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-2 scrollbar-thin scrollbar-thumb-purple-500/30 scrollbar-track-transparent">
                                {messages.length === 0 ? (
                                    <div className="h-full flex flex-col items-center justify-center text-center text-slate-500">
                                        <div className="mb-4">
                                            <div className="w-16 h-16 mx-auto bg-purple-500/10 rounded-full flex items-center justify-center">
                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                                                </svg>
                                            </div>
                                        </div>
                                        <h3 className="text-xl font-bold text-white mb-2">Welcome to your AI Todo Assistant!</h3>
                                        <p className="max-w-md">Start a conversation to manage your tasks naturally. Try commands like:</p>
                                        <ul className="mt-3 text-left space-y-1">
                                            <li className="text-sm">&bull; &ldquo;Add a task to buy groceries&rdquo;</li>
                                            <li className="text-sm">&bull; &ldquo;Show me my tasks&rdquo;</li>
                                            <li className="text-sm">&bull; &ldquo;Mark task 1 as complete&rdquo;</li>
                                            <li className="text-sm">&bull; &ldquo;Delete the meeting task&rdquo;</li>
                                        </ul>
                                    </div>
                                ) : (
                                    messages.map((msg) => (
                                        <div
                                            key={msg.id}
                                            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                                        >
                                            <div
                                                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                                                    msg.role === "user"
                                                        ? "bg-purple-600/20 border border-purple-500/30 rounded-br-none"
                                                        : "bg-neutral-800/50 border border-white/10 rounded-bl-none"
                                                }`}
                                            >
                                                <div className="whitespace-pre-wrap">{msg.content}</div>
                                                <div className={`text-xs mt-1 ${msg.role === "user" ? "text-purple-400/70" : "text-slate-500"}`}>
                                                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                </div>
                                            </div>
                                        </div>
                                    ))
                                )}
                                <div ref={messagesEndRef} />
                            </div>

                            <div className="flex gap-3">
                                <textarea
                                    value={inputMessage}
                                    onChange={(e) => setInputMessage(e.target.value)}
                                    onKeyPress={handleKeyPress}
                                    placeholder="Message your AI assistant..."
                                    className="flex-1 bg-neutral-800/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-transparent resize-none"
                                    rows={2}
                                    disabled={isSending}
                                />
                                <button
                                    onClick={handleSendMessage}
                                    disabled={isSending || !inputMessage.trim()}
                                    className="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/30 disabled:cursor-not-allowed text-white px-6 rounded-xl font-medium transition-colors whitespace-nowrap flex items-center justify-center"
                                >
                                    {isSending ? (
                                        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                    ) : (
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                                        </svg>
                                    )}
                                </button>
                            </div>
                        </div>
                    </section>
                </div>

                <footer className="mt-24 pt-12 border-t border-white/5 text-center">
                    <p className="text-slate-600 text-sm">
                        Evolution of Todo &bull; AI-Powered Task Management
                    </p>
                </footer>
            </div>
        </div>
    );
}
