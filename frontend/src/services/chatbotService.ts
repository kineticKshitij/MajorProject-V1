import api from './api';
import type {
    ChatSession,
    ChatMessage,
    SendMessageData,
    ChatFeedback,
    PaginatedResponse,
} from '../types';

export const chatbotService = {
    // Chat Sessions
    async getSessions(params?: {
        page?: number;
        search?: string;
    }): Promise<PaginatedResponse<ChatSession>> {
        const response = await api.get<PaginatedResponse<ChatSession>>(
            '/chatbot/sessions/',
            { params }
        );
        return response.data;
    },

    async getSession(id: number): Promise<ChatSession> {
        const response = await api.get<ChatSession>(`/chatbot/sessions/${id}/`);
        return response.data;
    },

    async createSession(data: {
        title: string;
        entity?: number;
    }): Promise<ChatSession> {
        const response = await api.post<ChatSession>('/chatbot/sessions/', data);
        return response.data;
    },

    async startSession(entityId?: number): Promise<ChatSession> {
        const response = await api.post<ChatSession>('/chatbot/sessions/start_session/', {
            entity_id: entityId,
        });
        return response.data;
    },

    async updateSession(
        id: number,
        data: { title?: string }
    ): Promise<ChatSession> {
        const response = await api.put<ChatSession>(`/chatbot/sessions/${id}/`, data);
        return response.data;
    },

    async deleteSession(id: number): Promise<void> {
        await api.delete(`/chatbot/sessions/${id}/`);
    },

    // Messages
    async getMessages(sessionId: number): Promise<ChatMessage[]> {
        const response = await api.get<ChatMessage[]>(
            `/chatbot/sessions/${sessionId}/messages/`
        );
        return response.data;
    },

    async sendMessage(
        sessionId: number,
        data: SendMessageData
    ): Promise<ChatMessage> {
        const response = await api.post<ChatMessage>(
            `/chatbot/sessions/${sessionId}/send_message/`,
            data
        );
        return response.data;
    },

    // Feedback
    async submitFeedback(data: Partial<ChatFeedback>): Promise<ChatFeedback> {
        const response = await api.post<ChatFeedback>('/chatbot/feedback/', data);
        return response.data;
    },

    // Configuration check
    async checkConfiguration(): Promise<{
        configured: boolean;
        message: string;
    }> {
        const response = await api.get('/chatbot/sessions/check_configuration/');
        return response.data;
    },

    // Statistics
    async getStatistics(): Promise<{
        total_sessions: number;
        total_messages: number;
        avg_messages_per_session: number;
    }> {
        const response = await api.get('/chatbot/sessions/statistics/');
        return response.data;
    },
};
