import api from './api';
import type {
    GoogleDork,
    DorkCategory,
    SearchSession,
    SearchResult,
    DorkBookmark,
    PaginatedResponse,
} from '../types';

export const dorksService = {
    // Categories
    async getCategories(): Promise<PaginatedResponse<DorkCategory>> {
        const response = await api.get<PaginatedResponse<DorkCategory>>('/dorks/categories/');
        return response.data;
    },

    async getCategory(id: number): Promise<DorkCategory> {
        const response = await api.get<DorkCategory>(`/dorks/categories/${id}/`);
        return response.data;
    },

    // Dorks
    async getDorks(params?: {
        page?: number;
        search?: string;
        category?: number;
        risk_level?: string;
        difficulty?: string;
        bookmarked?: boolean;
        my_dorks?: boolean;
    }): Promise<PaginatedResponse<GoogleDork>> {
        const response = await api.get<PaginatedResponse<GoogleDork>>('/dorks/dorks/', {
            params,
        });
        return response.data;
    },

    async getDork(id: number): Promise<GoogleDork> {
        const response = await api.get<GoogleDork>(`/dorks/dorks/${id}/`);
        return response.data;
    },

    async createDork(data: Partial<GoogleDork>): Promise<GoogleDork> {
        const response = await api.post<GoogleDork>('/dorks/dorks/', data);
        return response.data;
    },

    async updateDork(id: number, data: Partial<GoogleDork>): Promise<GoogleDork> {
        const response = await api.put<GoogleDork>(`/dorks/dorks/${id}/`, data);
        return response.data;
    },

    async deleteDork(id: number): Promise<void> {
        await api.delete(`/dorks/dorks/${id}/`);
    },

    async executeDork(id: number): Promise<{
        success: boolean;
        dork: GoogleDork;
        search_url: string;
        message: string;
    }> {
        const response = await api.post(`/dorks/dorks/${id}/execute/`);
        return response.data;
    },

    async toggleBookmark(id: number): Promise<{
        success: boolean;
        bookmarked: boolean;
        message: string;
        bookmark?: DorkBookmark;
    }> {
        const response = await api.post(`/dorks/dorks/${id}/bookmark/`);
        return response.data;
    },

    async getDorkStatistics(): Promise<{
        total_dorks: number;
        active_dorks: number;
        inactive_dorks: number;
        total_categories: number;
        risk_distribution: Array<{ risk_level: string; count: number }>;
        difficulty_distribution: Array<{ difficulty_level: string; count: number }>;
    }> {
        const response = await api.get('/dorks/dorks/statistics/');
        return response.data;
    },

    // Search Sessions
    async getSessions(params?: {
        page?: number;
        search?: string;
    }): Promise<PaginatedResponse<SearchSession>> {
        const response = await api.get<PaginatedResponse<SearchSession>>(
            '/dorks/sessions/',
            { params }
        );
        return response.data;
    },

    async getSession(id: number): Promise<SearchSession> {
        const response = await api.get<SearchSession>(`/dorks/sessions/${id}/`);
        return response.data;
    },

    async createSession(data: Partial<SearchSession>): Promise<SearchSession> {
        const response = await api.post<SearchSession>('/dorks/sessions/', data);
        return response.data;
    },

    async deleteSession(id: number): Promise<void> {
        await api.delete(`/dorks/sessions/${id}/`);
    },

    async getSessionResults(id: number): Promise<SearchResult[]> {
        const response = await api.get<SearchResult[]>(`/dorks/sessions/${id}/results/`);
        return response.data;
    },

    // Search Results
    async getResults(params?: {
        page?: number;
        session?: number;
        dork?: number;
    }): Promise<PaginatedResponse<SearchResult>> {
        const response = await api.get<PaginatedResponse<SearchResult>>('/dorks/results/', {
            params,
        });
        return response.data;
    },

    async createResult(data: Partial<SearchResult>): Promise<SearchResult> {
        const response = await api.post<SearchResult>('/dorks/results/', data);
        return response.data;
    },

    async updateResult(
        id: number,
        data: Partial<SearchResult>
    ): Promise<SearchResult> {
        const response = await api.put<SearchResult>(`/dorks/results/${id}/`, data);
        return response.data;
    },

    async deleteResult(id: number): Promise<void> {
        await api.delete(`/dorks/results/${id}/`);
    },

    // Bookmarks
    async getBookmarks(params?: {
        page?: number;
        search?: string;
    }): Promise<PaginatedResponse<DorkBookmark>> {
        const response = await api.get<PaginatedResponse<DorkBookmark>>(
            '/dorks/bookmarks/',
            { params }
        );
        return response.data;
    },

    async createBookmark(data: {
        dork: number;
        notes?: string;
    }): Promise<DorkBookmark> {
        const response = await api.post<DorkBookmark>('/dorks/bookmarks/', data);
        return response.data;
    },

    async updateBookmark(
        id: number,
        data: { notes?: string }
    ): Promise<DorkBookmark> {
        const response = await api.put<DorkBookmark>(`/dorks/bookmarks/${id}/`, data);
        return response.data;
    },

    async deleteBookmark(id: number): Promise<void> {
        await api.delete(`/dorks/bookmarks/${id}/`);
    },
};
