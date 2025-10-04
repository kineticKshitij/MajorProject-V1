import api from './api';
import type {
    CrawlJob,
    CrawlJobList,
    CreateCrawlJob,
    SocialProfile,
    SocialProfileList,
    SocialPost,
    SocialMetrics,
    CrawlSchedule,
    CreateCrawlSchedule,
    ProfileAnalytics,
    CrawlStatistics,
    SupportedPlatforms,
    PaginatedResponse,
    CrawlJobFilters,
    SocialPostFilters,
    SocialMetricsFilters,
} from '../types/crawler';

const CRAWLER_BASE = '/crawler';

// Crawl Jobs
export const crawlerService = {
    // Jobs CRUD
    getJobs: async (filters?: CrawlJobFilters, page: number = 1) => {
        const params = new URLSearchParams();
        if (filters?.status) params.append('status', filters.status);
        if (filters?.platform) params.append('platform', filters.platform);
        if (filters?.entity) params.append('entity', filters.entity.toString());
        if (filters?.search) params.append('search', filters.search);
        if (filters?.ordering) params.append('ordering', filters.ordering);
        if (page > 1) params.append('page', page.toString());

        const response = await api.get<PaginatedResponse<CrawlJobList>>(
            `${CRAWLER_BASE}/jobs/?${params.toString()}`
        );
        return response.data;
    },

    getJob: async (id: string) => {
        const response = await api.get<CrawlJob>(`${CRAWLER_BASE}/jobs/${id}/`);
        return response.data;
    },

    createJob: async (data: CreateCrawlJob) => {
        const response = await api.post<CrawlJob>(`${CRAWLER_BASE}/jobs/`, data);
        return response.data;
    },

    updateJob: async (id: string, data: Partial<CreateCrawlJob>) => {
        const response = await api.patch<CrawlJob>(`${CRAWLER_BASE}/jobs/${id}/`, data);
        return response.data;
    },

    deleteJob: async (id: string) => {
        await api.delete(`${CRAWLER_BASE}/jobs/${id}/`);
    },

    // Job Actions
    restartJob: async (id: string) => {
        const response = await api.post<CrawlJob>(`${CRAWLER_BASE}/jobs/${id}/restart/`);
        return response.data;
    },

    cancelJob: async (id: string) => {
        const response = await api.post<CrawlJob>(`${CRAWLER_BASE}/jobs/${id}/cancel/`);
        return response.data;
    },

    getSupportedPlatforms: async () => {
        const response = await api.get<SupportedPlatforms>(
            `${CRAWLER_BASE}/jobs/supported_platforms/`
        );
        return response.data;
    },

    getStatistics: async () => {
        const response = await api.get<CrawlStatistics>(
            `${CRAWLER_BASE}/jobs/statistics/`
        );
        return response.data;
    },

    // Profiles
    getProfiles: async (page: number = 1, filters?: { platform?: string; search?: string }) => {
        const params = new URLSearchParams();
        if (filters?.platform) params.append('platform', filters.platform);
        if (filters?.search) params.append('search', filters.search);
        if (page > 1) params.append('page', page.toString());

        const response = await api.get<PaginatedResponse<SocialProfileList>>(
            `${CRAWLER_BASE}/profiles/?${params.toString()}`
        );
        return response.data;
    },

    getProfile: async (id: string) => {
        const response = await api.get<SocialProfile>(`${CRAWLER_BASE}/profiles/${id}/`);
        return response.data;
    },

    getProfileAnalytics: async (id: string) => {
        const response = await api.get<ProfileAnalytics>(
            `${CRAWLER_BASE}/profiles/${id}/analytics/`
        );
        return response.data;
    },

    // Posts
    getPosts: async (filters?: SocialPostFilters, page: number = 1) => {
        const params = new URLSearchParams();
        if (filters?.profile) params.append('profile', filters.profile);
        if (filters?.platform) params.append('platform', filters.platform);
        if (filters?.posted_after) params.append('posted_after', filters.posted_after);
        if (filters?.posted_before) params.append('posted_before', filters.posted_before);
        if (filters?.sentiment) params.append('sentiment', filters.sentiment);
        if (filters?.search) params.append('search', filters.search);
        if (filters?.ordering) params.append('ordering', filters.ordering);
        if (page > 1) params.append('page', page.toString());

        const response = await api.get<PaginatedResponse<SocialPost>>(
            `${CRAWLER_BASE}/posts/?${params.toString()}`
        );
        return response.data;
    },

    getPost: async (id: string) => {
        const response = await api.get<SocialPost>(`${CRAWLER_BASE}/posts/${id}/`);
        return response.data;
    },

    // Metrics
    getMetrics: async (filters?: SocialMetricsFilters, page: number = 1) => {
        const params = new URLSearchParams();
        if (filters?.profile) params.append('profile', filters.profile);
        if (filters?.date_after) params.append('date_after', filters.date_after);
        if (filters?.date_before) params.append('date_before', filters.date_before);
        if (filters?.ordering) params.append('ordering', filters.ordering);
        if (page > 1) params.append('page', page.toString());

        const response = await api.get<PaginatedResponse<SocialMetrics>>(
            `${CRAWLER_BASE}/metrics/?${params.toString()}`
        );
        return response.data;
    },

    getMetric: async (id: string) => {
        const response = await api.get<SocialMetrics>(`${CRAWLER_BASE}/metrics/${id}/`);
        return response.data;
    },

    // Schedules CRUD
    getSchedules: async (page: number = 1, filters?: { platform?: string; is_active?: boolean }) => {
        const params = new URLSearchParams();
        if (filters?.platform) params.append('platform', filters.platform);
        if (filters?.is_active !== undefined) params.append('is_active', filters.is_active.toString());
        if (page > 1) params.append('page', page.toString());

        const response = await api.get<PaginatedResponse<CrawlSchedule>>(
            `${CRAWLER_BASE}/schedules/?${params.toString()}`
        );
        return response.data;
    },

    getSchedule: async (id: string) => {
        const response = await api.get<CrawlSchedule>(`${CRAWLER_BASE}/schedules/${id}/`);
        return response.data;
    },

    createSchedule: async (data: CreateCrawlSchedule) => {
        const response = await api.post<CrawlSchedule>(`${CRAWLER_BASE}/schedules/`, data);
        return response.data;
    },

    updateSchedule: async (id: string, data: Partial<CreateCrawlSchedule>) => {
        const response = await api.patch<CrawlSchedule>(
            `${CRAWLER_BASE}/schedules/${id}/`,
            data
        );
        return response.data;
    },

    deleteSchedule: async (id: string) => {
        await api.delete(`${CRAWLER_BASE}/schedules/${id}/`);
    },

    toggleScheduleActive: async (id: string) => {
        const response = await api.post<CrawlSchedule>(
            `${CRAWLER_BASE}/schedules/${id}/toggle_active/`
        );
        return response.data;
    },
};

export default crawlerService;
