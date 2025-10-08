import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import crawlerService from '../services/crawlerService';
import type { Platform, Sentiment } from '../types/crawler';

const PostsList = () => {
    const [platformFilter, setPlatformFilter] = useState<Platform | 'all'>('all');
    const [sentimentFilter, setSentimentFilter] = useState<Sentiment | 'all'>('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [currentPage, setCurrentPage] = useState(1);

    // Fetch posts
    const { data: postsData, isLoading } = useQuery({
        queryKey: ['posts', platformFilter, sentimentFilter, searchQuery, currentPage],
        queryFn: () => crawlerService.getPosts(
            {
                platform: platformFilter !== 'all' ? platformFilter : undefined,
                sentiment: sentimentFilter !== 'all' ? sentimentFilter : undefined,
                search: searchQuery || undefined,
            },
            currentPage
        ),
    });

    const getPlatformIcon = (platform: Platform) => {
        const icons: Record<Platform, string> = {
            twitter: '𝕏',
            github: '🐙',
            linkedin: '💼',
            reddit: '🤖',
            instagram: '📷',
            facebook: '👍',
            tiktok: '🎵',
            youtube: '▶️',
        };
        return icons[platform] || '🌐';
    };

    const getSentimentColor = (sentiment?: Sentiment) => {
        if (!sentiment) return 'bg-gray-100 text-gray-800';
        const colors = {
            positive: 'bg-green-100 text-green-800',
            negative: 'bg-red-100 text-red-800',
            neutral: 'bg-gray-100 text-gray-800',
        };
        return colors[sentiment];
    };

    const getSentimentIcon = (sentiment?: Sentiment) => {
        if (!sentiment) return '😐';
        const icons = {
            positive: '😊',
            negative: '😔',
            neutral: '😐',
        };
        return icons[sentiment];
    };

    const formatNumber = (num: number) => {
        if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
        if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
        return num.toString();
    };

    const formatDate = (dateString?: string) => {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString();
    };

    const truncateText = (text: string, maxLength: number) => {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Crawled Posts</h1>
                <p className="mt-2 text-gray-600">
                    Browse all social media posts and content that have been crawled
                </p>
            </div>

            {/* Filters */}
            <div className="bg-white rounded-lg shadow mb-6 p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Search */}
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => {
                            setSearchQuery(e.target.value);
                            setCurrentPage(1);
                        }}
                        placeholder="Search in post content..."
                        className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    />

                    {/* Platform Filter */}
                    <select
                        value={platformFilter}
                        onChange={(e) => {
                            setPlatformFilter(e.target.value as Platform | 'all');
                            setCurrentPage(1);
                        }}
                        className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                        <option value="all">All Platforms</option>
                        <option value="github">GitHub</option>
                        <option value="reddit">Reddit</option>
                        <option value="twitter">Twitter</option>
                        <option value="linkedin">LinkedIn</option>
                    </select>

                    {/* Sentiment Filter */}
                    <select
                        value={sentimentFilter}
                        onChange={(e) => {
                            setSentimentFilter(e.target.value as Sentiment | 'all');
                            setCurrentPage(1);
                        }}
                        className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                        <option value="all">All Sentiments</option>
                        <option value="positive">Positive 😊</option>
                        <option value="neutral">Neutral 😐</option>
                        <option value="negative">Negative 😔</option>
                    </select>
                </div>
            </div>

            {/* Posts List */}
            {isLoading ? (
                <div className="flex justify-center items-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                </div>
            ) : postsData?.results.length === 0 ? (
                <div className="bg-white rounded-lg shadow p-12 text-center">
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                    </svg>
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No posts found</h3>
                    <p className="mt-1 text-sm text-gray-500">Try adjusting your filters.</p>
                </div>
            ) : (
                <>
                    <div className="space-y-4 mb-6">
                        {postsData?.results.map((post) => (
                            <div key={post.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6">
                                {/* Post Header */}
                                <div className="flex items-start justify-between mb-4">
                                    <div className="flex items-center space-x-2">
                                        <span className="text-2xl">{getPlatformIcon(post.profile as Platform)}</span>
                                        <div>
                                            <p className="text-sm font-medium text-gray-900">
                                                Post ID: <code className="text-xs font-mono">{post.post_id}</code>
                                            </p>
                                            <p className="text-xs text-gray-500">{formatDate(post.posted_at)}</p>
                                        </div>
                                    </div>
                                    {post.sentiment && (
                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getSentimentColor(post.sentiment)}`}>
                                            {getSentimentIcon(post.sentiment)} {post.sentiment}
                                        </span>
                                    )}
                                </div>

                                {/* Post Content */}
                                {post.content && (
                                    <div className="mb-4">
                                        <p className="text-gray-800">
                                            {truncateText(post.content, 300)}
                                        </p>
                                    </div>
                                )}

                                {/* Media indicator */}
                                {post.media_urls && post.media_urls.length > 0 && (
                                    <div className="mb-4 flex items-center text-sm text-gray-500">
                                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
                                        <span>{post.media_urls.length} media file(s)</span>
                                    </div>
                                )}

                                {/* Hashtags */}
                                {post.hashtags && post.hashtags.length > 0 && (
                                    <div className="mb-4 flex flex-wrap gap-2">
                                        {post.hashtags.slice(0, 5).map((tag, index) => (
                                            <span key={index} className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-50 text-blue-700">
                                                #{tag}
                                            </span>
                                        ))}
                                        {post.hashtags.length > 5 && (
                                            <span className="text-xs text-gray-500">+{post.hashtags.length - 5} more</span>
                                        )}
                                    </div>
                                )}

                                {/* Engagement Stats */}
                                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                                    <div className="flex items-center space-x-6 text-sm text-gray-500">
                                        <div className="flex items-center">
                                            <svg className="w-5 h-5 mr-1 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                                            </svg>
                                            <span className="font-medium">{formatNumber(post.likes_count)}</span>
                                        </div>
                                        <div className="flex items-center">
                                            <svg className="w-5 h-5 mr-1 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                                            </svg>
                                            <span className="font-medium">{formatNumber(post.comments_count)}</span>
                                        </div>
                                        <div className="flex items-center">
                                            <svg className="w-5 h-5 mr-1 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                                                <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                                            </svg>
                                            <span className="font-medium">{formatNumber(post.shares_count)}</span>
                                        </div>
                                        {post.views_count && post.views_count > 0 && (
                                            <div className="flex items-center">
                                                <svg className="w-5 h-5 mr-1 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                                                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                                                    <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                                                </svg>
                                                <span className="font-medium">{formatNumber(post.views_count)}</span>
                                            </div>
                                        )}
                                    </div>

                                    {post.post_url && (
                                        <a
                                            href={post.post_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                                        >
                                            View Original
                                            <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                            </svg>
                                        </a>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Pagination */}
                    {postsData && postsData.results.length > 0 && (
                        <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 rounded-lg shadow">
                            <div className="flex-1 flex justify-between sm:hidden">
                                <button
                                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                    disabled={!postsData.previous}
                                    className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Previous
                                </button>
                                <button
                                    onClick={() => setCurrentPage(prev => prev + 1)}
                                    disabled={!postsData.next}
                                    className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Next
                                </button>
                            </div>
                            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                                <div>
                                    <p className="text-sm text-gray-700">
                                        Showing <span className="font-medium">{((currentPage - 1) * 10) + 1}</span> to{' '}
                                        <span className="font-medium">
                                            {Math.min(currentPage * 10, postsData.count)}
                                        </span> of{' '}
                                        <span className="font-medium">{postsData.count}</span> results
                                    </p>
                                </div>
                                <div>
                                    <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                                        <button
                                            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                            disabled={!postsData.previous}
                                            className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                        >
                                            <span className="sr-only">Previous</span>
                                            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                                            </svg>
                                        </button>
                                        <button
                                            onClick={() => setCurrentPage(prev => prev + 1)}
                                            disabled={!postsData.next}
                                            className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                        >
                                            <span className="sr-only">Next</span>
                                            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                                            </svg>
                                        </button>
                                    </nav>
                                </div>
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default PostsList;
