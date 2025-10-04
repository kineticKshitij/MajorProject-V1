import { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { useMutation } from '@tanstack/react-query';
import { chatbotService } from '../../services/chatbotService';
import type { ChatMessage } from '../../types';

interface ChatMessagesProps {
    messages: ChatMessage[];
    isLoading?: boolean;
}

const ChatMessages = ({ messages, isLoading }: ChatMessagesProps) => {
    const [copiedId, setCopiedId] = useState<number | null>(null);
    const [feedbackStates, setFeedbackStates] = useState<Record<number, 'helpful' | 'not_helpful' | null>>({});

    const feedbackMutation = useMutation({
        mutationFn: (data: { messageId: number; feedbackType: 'helpful' | 'not_helpful' }) =>
            chatbotService.submitFeedback({
                message: data.messageId,
                feedback_type: data.feedbackType,
            }),
        onSuccess: (_data, variables) => {
            setFeedbackStates(prev => ({ ...prev, [variables.messageId]: variables.feedbackType }));
        },
    });

    const copyToClipboard = async (text: string, messageId: number) => {
        try {
            await navigator.clipboard.writeText(text);
            setCopiedId(messageId);
            setTimeout(() => setCopiedId(null), 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    };

    const handleFeedback = (messageId: number, feedbackType: 'helpful' | 'not_helpful') => {
        feedbackMutation.mutate({ messageId, feedbackType });
    };

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            {messages.map((message) => (
                <div
                    key={message.id}
                    className={`flex gap-4 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                        }`}
                >
                    {/* Avatar */}
                    <div
                        className={`
                            flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold
                            ${message.role === 'user' ? 'bg-primary-600' : 'bg-green-600'}
                        `}
                    >
                        {message.role === 'user' ? '👤' : '🤖'}
                    </div>

                    {/* Message Content */}
                    <div className={`flex-1 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                        <div
                            className={`
                                inline-block max-w-[85%] p-4 rounded-lg
                                ${message.role === 'user'
                                    ? 'bg-primary-600 text-white'
                                    : 'bg-white border border-gray-200'
                                }
                            `}
                        >
                            <div className="whitespace-pre-wrap break-words">
                                {message.message}
                            </div>

                            {/* Message Metadata */}
                            <div
                                className={`
                                    mt-2 text-xs flex items-center gap-2
                                    ${message.role === 'user' ? 'text-primary-100 justify-end' : 'text-gray-500 justify-start'}
                                `}
                            >
                                <span>
                                    {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
                                </span>
                                {message.tokens_used && message.role === 'assistant' && (
                                    <>
                                        <span>•</span>
                                        <span>{message.tokens_used} tokens</span>
                                    </>
                                )}
                            </div>
                        </div>

                        {/* Action Buttons (for assistant messages) */}
                        {message.role === 'assistant' && (
                            <div className="mt-2 flex items-center gap-2">
                                {/* Copy Button */}
                                <button
                                    onClick={() => copyToClipboard(message.message, message.id)}
                                    className="text-gray-500 hover:text-gray-700 text-sm flex items-center gap-1"
                                    title="Copy message"
                                >
                                    {copiedId === message.id ? (
                                        <>
                                            <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                            </svg>
                                            <span className="text-green-600">Copied!</span>
                                        </>
                                    ) : (
                                        <>
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                            </svg>
                                            <span>Copy</span>
                                        </>
                                    )}
                                </button>

                                {/* Feedback Buttons */}
                                <div className="flex items-center gap-1 ml-2">
                                    <button
                                        onClick={() => handleFeedback(message.id, 'helpful')}
                                        disabled={feedbackStates[message.id] !== undefined}
                                        className={`
                                            p-1 rounded hover:bg-gray-100 transition-colors
                                            ${feedbackStates[message.id] === 'helpful' ? 'text-green-600' : 'text-gray-400'}
                                            disabled:opacity-50 disabled:cursor-not-allowed
                                        `}
                                        title="Helpful"
                                    >
                                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                                        </svg>
                                    </button>
                                    <button
                                        onClick={() => handleFeedback(message.id, 'not_helpful')}
                                        disabled={feedbackStates[message.id] !== undefined}
                                        className={`
                                            p-1 rounded hover:bg-gray-100 transition-colors
                                            ${feedbackStates[message.id] === 'not_helpful' ? 'text-red-600' : 'text-gray-400'}
                                            disabled:opacity-50 disabled:cursor-not-allowed
                                        `}
                                        title="Not helpful"
                                    >
                                        <svg className="w-4 h-4 transform rotate-180" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
                <div className="flex gap-4">
                    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-600 flex items-center justify-center text-white">
                        🤖
                    </div>
                    <div className="flex-1">
                        <div className="inline-block bg-white border border-gray-200 p-4 rounded-lg">
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChatMessages;
