import { useQuery } from '@tanstack/react-query';
import { chatbotService } from '../../services/chatbotService';
import { formatDistanceToNow } from 'date-fns';

interface ChatSidebarProps {
    isOpen: boolean;
    currentSessionId: number | null;
    onSelectSession: (sessionId: number) => void;
    onNewChat: () => void;
    onDeleteSession: (sessionId: number) => void;
    onClose: () => void;
}

const ChatSidebar = ({
    isOpen,
    currentSessionId,
    onSelectSession,
    onNewChat,
    onDeleteSession,
    onClose,
}: ChatSidebarProps) => {
    const { data: sessionsResponse, isLoading } = useQuery({
        queryKey: ['chatSessions'],
        queryFn: () => chatbotService.getSessions(),
    });

    const sessions = sessionsResponse?.results || [];

    return (
        <>
            {/* Mobile overlay */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
                    onClick={onClose}
                />
            )}

            {/* Sidebar */}
            <div
                className={`
                    fixed lg:static inset-y-0 left-0 z-50
                    w-80 bg-white border-r border-gray-200
                    transform transition-transform duration-300 ease-in-out
                    ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
                    flex flex-col
                `}
            >
                {/* Sidebar Header */}
                <div className="p-4 border-b border-gray-200">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold text-gray-900">Chat Sessions</h2>
                        <button
                            onClick={onClose}
                            className="text-gray-500 hover:text-gray-700 lg:hidden"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <button
                        onClick={onNewChat}
                        className="w-full btn-primary flex items-center justify-center gap-2"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        New Chat
                    </button>
                </div>

                {/* Sessions List */}
                <div className="flex-1 overflow-y-auto">
                    {isLoading ? (
                        <div className="p-4 text-center text-gray-500">
                            Loading sessions...
                        </div>
                    ) : sessions.length === 0 ? (
                        <div className="p-4 text-center text-gray-500">
                            <p className="mb-2">No chat sessions yet</p>
                            <p className="text-sm">Start a new conversation!</p>
                        </div>
                    ) : (
                        <div className="divide-y divide-gray-200">
                            {sessions.map((session) => (
                                <div
                                    key={session.id}
                                    className={`
                                        p-4 cursor-pointer hover:bg-gray-50 transition-colors
                                        ${currentSessionId === session.id ? 'bg-primary-50 border-l-4 border-primary-600' : ''}
                                    `}
                                    onClick={() => onSelectSession(session.id)}
                                >
                                    <div className="flex items-start justify-between gap-2">
                                        <div className="flex-1 min-w-0">
                                            <h3 className="font-medium text-gray-900 truncate mb-1">
                                                {session.title}
                                            </h3>
                                            <div className="flex items-center gap-2 text-xs text-gray-500">
                                                <span>{session.message_count} messages</span>
                                                <span>•</span>
                                                <span>
                                                    {formatDistanceToNow(new Date(session.updated_at), { addSuffix: true })}
                                                </span>
                                            </div>
                                            {session.entity_name && (
                                                <div className="mt-1">
                                                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                                                        {session.entity_name}
                                                    </span>
                                                </div>
                                            )}
                                        </div>
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                onDeleteSession(session.id);
                                            }}
                                            className="text-gray-400 hover:text-red-600 transition-colors"
                                            title="Delete session"
                                        >
                                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Sidebar Footer */}
                <div className="p-4 border-t border-gray-200 bg-gray-50">
                    <div className="text-xs text-gray-600">
                        <p className="mb-1">💡 <strong>Tips:</strong></p>
                        <ul className="list-disc list-inside space-y-1 text-gray-500">
                            <li>Ask about Google dorking techniques</li>
                            <li>Get help with entity research</li>
                            <li>Learn security best practices</li>
                        </ul>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ChatSidebar;
