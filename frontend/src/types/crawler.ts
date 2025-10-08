// Social Media Crawler Types

export type Platform =
    | 'twitter'
    | 'github'
    | 'linkedin'
    | 'reddit'
    | 'instagram'
    | 'facebook'
    | 'tiktok'
    | 'youtube';

export type CrawlStatus =
    | 'pending'
    | 'in_progress'
    | 'completed'
    | 'failed'
    | 'cancelled';

export type CrawlFrequency =
    | 'hourly'
    | 'daily'
    | 'weekly'
    | 'monthly';

export type MediaType =
    | 'image'
    | 'video'
    | 'audio'
    | 'document'
    | 'link';

export type Sentiment =
    | 'positive'
    | 'negative'
    | 'neutral';

// Crawl Job Interfaces
export interface CrawlJob {
    id: string;
    user: number;
    entity?: number;
    platform: Platform;
    target_username: string;
    target_url?: string;
    status: CrawlStatus;
    progress: number;
    crawl_posts: boolean;
    crawl_followers: boolean;
    crawl_following: boolean;
    max_posts?: number;
    max_followers?: number;
    profiles_found: number;
    posts_found: number;
    error_message?: string;
    metadata?: Record<string, unknown>;
    created_at: string;
    started_at?: string;
    completed_at?: string;
}

export interface CrawlJobList {
    id: string;
    platform: Platform;
    target_username: string;
    status: CrawlStatus;
    progress: number;
    profiles_found: number;
    posts_found: number;
    created_at: string;
    completed_at?: string;
}

export interface CreateCrawlJob {
    entity?: number;
    platform: Platform;
    target_username?: string;
    target_url?: string;
    crawl_posts?: boolean;
    crawl_followers?: boolean;
    crawl_following?: boolean;
    max_posts?: number;
    max_followers?: number;
}

// Social Profile Interfaces
export interface SocialProfile {
    id: string;
    crawl_job: string;
    entity?: number;
    platform: Platform;
    username: string;
    user_id?: string;
    profile_url?: string;
    display_name?: string;
    bio?: string;
    avatar_url?: string;
    banner_url?: string;
    followers_count: number;
    following_count: number;
    posts_count: number;
    verified: boolean;
    location?: string;
    website?: string;
    joined_date?: string;
    raw_data?: Record<string, unknown>;
    crawled_at: string;
    last_updated: string;
    posts?: SocialPost[];
}

export interface SocialProfileList {
    id: string;
    platform: Platform;
    username: string;
    display_name?: string;
    avatar_url?: string;
    followers_count: number;
    posts_count: number;
    verified: boolean;
    crawled_at: string;
}

// Social Post Interfaces
export interface SocialPost {
    id: string;
    profile: string;
    crawl_job: string;
    post_id: string;
    post_url?: string;
    content?: string;
    media_urls?: string[];
    media_type?: MediaType;
    likes_count: number;
    comments_count: number;
    shares_count: number;
    views_count?: number;
    posted_at?: string;
    language?: string;
    hashtags?: string[];
    mentions?: string[];
    sentiment?: Sentiment;
    topics?: string[];
    raw_data?: Record<string, unknown>;
    crawled_at: string;
}

// Social Metrics Interfaces
export interface SocialMetrics {
    id: string;
    profile: string;
    date: string;
    followers_count: number;
    following_count: number;
    posts_count: number;
    followers_gained?: number;
    followers_lost?: number;
    total_likes: number;
    total_comments: number;
    total_shares: number;
    engagement_rate: number;
    posts_today: number;
    avg_likes_per_post?: number;
    recorded_at: string;
}

// Crawl Schedule Interfaces
export interface CrawlSchedule {
    id: string;
    user: number;
    entity?: number;
    name: string;
    platform: Platform;
    target_username: string;
    frequency: CrawlFrequency;
    is_active: boolean;
    last_run?: string;
    next_run?: string;
    crawl_config?: {
        crawl_posts?: boolean;
        crawl_followers?: boolean;
        crawl_following?: boolean;
        max_posts?: number;
        max_followers?: number;
    };
    created_at: string;
    updated_at: string;
}

export interface CreateCrawlSchedule {
    entity?: number;
    name: string;
    platform: Platform;
    target_username: string;
    frequency: CrawlFrequency;
    is_active?: boolean;
    crawl_config?: {
        crawl_posts?: boolean;
        crawl_followers?: boolean;
        crawl_following?: boolean;
        max_posts?: number;
        max_followers?: number;
    };
}

// Analytics Interfaces
export interface ProfileAnalytics {
    profile: {
        username: string;
        platform: Platform;
    };
    total_posts: number;
    total_engagement: number;
    avg_engagement_per_post: number;
    most_liked_post?: {
        content?: string;
        likes_count: number;
    };
    most_commented_post?: {
        content?: string;
        comments_count: number;
    };
    engagement_by_type: {
        likes: number;
        comments: number;
        shares: number;
    };
}

export interface CrawlStatistics {
    total_jobs: number;
    completed_jobs: number;
    failed_jobs: number;
    pending_jobs: number;
    in_progress_jobs: number;
    total_profiles_crawled: number;
    total_posts_crawled: number;
    jobs_by_platform: Record<Platform, number>;
}

export interface SupportedPlatforms {
    platforms: Platform[];
    message: string;
}

// API Response Interfaces
export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

// Filter Interfaces
export interface CrawlJobFilters {
    status?: CrawlStatus;
    platform?: Platform;
    entity?: number;
    search?: string;
    ordering?: string;
}

export interface SocialPostFilters {
    profile?: string;
    platform?: Platform;
    posted_after?: string;
    posted_before?: string;
    sentiment?: Sentiment;
    search?: string;
    ordering?: string;
}

export interface SocialMetricsFilters {
    profile?: string;
    date_after?: string;
    date_before?: string;
    ordering?: string;
}
