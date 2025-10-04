import { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { chatbotService } from '../../services/chatbotService';
import ChatSidebar from '../../components/chatbot/ChatSidebar';
import ChatMessages from '../../components/chatbot/ChatMessages';
import ChatInput from '../../components/chatbot/ChatInput';
import ApiKeyPrompt from '../../components/chatbot/ApiKeyPrompt';

const ChatInterface = () => {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [searchParams] = useSearchParams();
    const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
    const [showSidebar, setShowSidebar] = useState(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Check API configuration
    const { data: configStatus } = useQuery({
        queryKey: ['chatbotConfig'],
        queryFn: chatbotService.checkConfiguration,
    });

    // Get current session
    const { data: currentSession, isLoading: isLoadingSession } = useQuery({
        queryKey: ['chatSession', currentSessionId],
        queryFn: () => chatbotService.getSession(currentSessionId!),
        enabled: !!currentSessionId,
    });

    // Get messages for current session
    const { data: messages = [], isLoading: isLoadingMessages, refetch: refetchMessages } = useQuery({
        queryKey: ['chatMessages', currentSessionId],
        queryFn: () => chatbotService.getMessages(currentSessionId!),
        enabled: !!currentSessionId,
    });

    // Start new session mutation
    const startSessionMutation = useMutation({
        mutationFn: () => chatbotService.startSession(),
        onSuccess: (session) => {
            setCurrentSessionId(session.id);
            queryClient.invalidateQueries({ queryKey: ['chatSessions'] });
        },
    });

    // Send message mutation
    const sendMessageMutation = useMutation({
        mutationFn: ({ message }: { message: string }) =>
            chatbotService.sendMessage(currentSessionId!, { message }),
        onSuccess: () => {
            refetchMessages();
            queryClient.invalidateQueries({ queryKey: ['chatSessions'] });
            queryClient.invalidateQueries({ queryKey: ['chatSession', currentSessionId] });
        },
    });

    // Delete session mutation
    const deleteSessionMutation = useMutation({
        mutationFn: (sessionId: number) => chatbotService.deleteSession(sessionId),
        onSuccess: () => {
            if (currentSessionId === deleteSessionMutation.variables) {
                setCurrentSessionId(null);
            }
            queryClient.invalidateQueries({ queryKey: ['chatSessions'] });
        },
    });

    // Handle session selection from URL or start new session
    useEffect(() => {
        const sessionParam = searchParams.get('session');
        if (sessionParam) {
            setCurrentSessionId(Number(sessionParam));
        } else if (!currentSessionId) {
            startSessionMutation.mutate();
        }
    }, [searchParams]);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSelectSession = (sessionId: number) => {
        setCurrentSessionId(sessionId);
        navigate(`/chatbot?session=${sessionId}`);
    };

    const handleNewChat = () => {
        startSessionMutation.mutate();
    };

    const handleSendMessage = (message: string) => {
        if (!currentSessionId || !message.trim()) return;
        sendMessageMutation.mutate({ message });
    };

    const handleDeleteSession = (sessionId: number) => {
        if (window.confirm('Are you sure you want to delete this chat session?')) {
            deleteSessionMutation.mutate(sessionId);
        }
    };

    // Show API key prompt if not configured
    if (configStatus && !configStatus.configured) {
        return <ApiKeyPrompt message={configStatus.message} />;
    }

    return (
        <div className="h-screen flex overflow-hidden bg-gray-50">
            {/* Sidebar */}
            <ChatSidebar
                isOpen={showSidebar}
                currentSessionId={currentSessionId}
                onSelectSession={handleSelectSession}
                onNewChat={handleNewChat}
                onDeleteSession={handleDeleteSession}
                onClose={() => setShowSidebar(false)}
            />

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Header */}
                <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => setShowSidebar(!showSidebar)}
                            className="text-gray-500 hover:text-gray-700 lg:hidden"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                        <div>
                            <h1 className="text-xl font-semibold text-gray-900">
                                {isLoadingSession ? 'Loading...' : currentSession?.title || 'New Chat'}
                            </h1>
                            {currentSession?.entity_name && (
                                <p className="text-sm text-gray-500">
                                    Entity: {currentSession.entity_name}
                                </p>
                            )}
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={handleNewChat}
                            className="btn-primary text-sm"
                            disabled={startSessionMutation.isPending}
                        >
                            + New Chat
                        </button>
                    </div>
                </div>

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto">
                    {isLoadingMessages ? (
                        <div className="flex items-center justify-center h-full">
                            <div className="text-center">
                                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                                <p className="mt-4 text-gray-600">Loading messages...</p>
                            </div>
                        </div>
                    ) : messages.length === 0 ? (
                        <div className="flex items-center justify-center h-full">
                            <div className="text-center max-w-md">
                                <div className="text-6xl mb-4">💬</div>
                                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                                    Start a Conversation
                                </h2>
                                <p className="text-gray-600 mb-6">
                                    Ask me anything about Google dorking, security research, or entity investigation!
                                </p>
                                <div className="space-y-2 text-left">
                                    <div className="p-3 bg-gray-100 rounded-lg text-sm">
                                        <strong>Example:</strong> "How do I find exposed databases?"
                                    </div>
                                    <div className="p-3 bg-gray-100 rounded-lg text-sm">
                                        <strong>Example:</strong> "What are the best dorks for finding API keys?"
                                    </div>
                                    <div className="p-3 bg-gray-100 rounded-lg text-sm">
                                        <strong>Example:</strong> "Help me research a company"
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <ChatMessages
                            messages={messages}
                            isLoading={sendMessageMutation.isPending}
                        />
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <ChatInput
                    onSendMessage={handleSendMessage}
                    disabled={!currentSessionId || sendMessageMutation.isPending}
                    isLoading={sendMessageMutation.isPending}
                />
            </div>
        </div>
    );
};

export default ChatInterface;
