import { useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import crawlerService from '../services/crawlerService';
import type { CrawlStatus, Platform } from '../types/crawler';

const CrawlJobDetail = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();

    // Fetch job details
    const { data: job, isLoading, refetch } = useQuery({
        queryKey: ['crawl-job', id],
        queryFn: () => crawlerService.getJob(id!),
        enabled: !!id,
    });

    // Note: We could fetch profiles and posts here, but they're accessible via links

    // Cancel job mutation
    const cancelMutation = useMutation({
        mutationFn: () => crawlerService.cancelJob(id!),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['crawl-job', id] });
            refetch();
        },
    });

    // Restart job mutation
    const restartMutation = useMutation({
        mutationFn: () => crawlerService.restartJob(id!),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['crawl-job', id] });
            refetch();
        },
    });

    // Delete job mutation
    const deleteMutation = useMutation({
        mutationFn: () => crawlerService.deleteJob(id!),
        onSuccess: () => {
            navigate('/crawler');
        },
    });

    // Auto-refresh for in-progress jobs
    useEffect(() => {
        if (job && (job.status === 'in_progress' || job.status === 'pending')) {
            const interval = setInterval(() => {
                refetch();
            }, 3000); // Refresh every 3 seconds

            return () => clearInterval(interval);
        }
    }, [job, refetch]);

    const getStatusBadgeColor = (status: CrawlStatus) => {
        const colors = {
            pending: 'bg-yellow-100 text-yellow-800',
            in_progress: 'bg-blue-100 text-blue-800',
            completed: 'bg-green-100 text-green-800',
            failed: 'bg-red-100 text-red-800',
            cancelled: 'bg-gray-100 text-gray-800',
        };
        return colors[status] || 'bg-gray-100 text-gray-800';
    };

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

    const formatDate = (dateString?: string) => {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleString();
    };

    const formatDuration = (start?: string, end?: string) => {
        if (!start) return 'N/A';
        const startDate = new Date(start);
        const endDate = end ? new Date(end) : new Date();
        const durationMs = endDate.getTime() - startDate.getTime();
        const seconds = Math.floor(durationMs / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);

        if (hours > 0) return `${hours}h ${minutes % 60}m`;
        if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
        return `${seconds}s`;
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            </div>
        );
    }

    if (!job) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="text-center">
                    <h3 className="text-lg font-medium text-gray-900">Job not found</h3>
                    <p className="mt-2 text-sm text-gray-500">The crawl job you're looking for doesn't exist.</p>
                    <div className="mt-6">
                        <Link
                            to="/crawler"
                            className="text-indigo-600 hover:text-indigo-800"
                        >
                            Back to Dashboard
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header */}
            <div className="mb-8">
                <button
                    onClick={() => navigate('/crawler')}
                    className="text-indigo-600 hover:text-indigo-800 flex items-center mb-4"
                >
                    <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    Back to Dashboard
                </button>
                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <span className="text-4xl mr-4">{getPlatformIcon(job.platform)}</span>
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">
                                @{job.target_username}
                            </h1>
                            <p className="text-gray-600 capitalize">{job.platform} Crawl Job</p>
                        </div>
                    </div>
                    <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${getStatusBadgeColor(job.status)}`}>
                        {job.status.replace('_', ' ')}
                    </span>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main Content */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Progress Card */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">Progress</h2>

                        <div className="space-y-4">
                            <div>
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm font-medium text-gray-700">Completion</span>
                                    <span className="text-sm font-medium text-gray-900">{job.progress}%</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-4">
                                    <div
                                        className={`h-4 rounded-full transition-all duration-500 ${job.status === 'completed' ? 'bg-green-600' :
                                                job.status === 'failed' ? 'bg-red-600' :
                                                    job.status === 'cancelled' ? 'bg-gray-600' :
                                                        'bg-blue-600'
                                            }`}
                                        style={{ width: `${job.progress}%` }}
                                    ></div>
                                </div>
                            </div>

                            {(job.status === 'in_progress' || job.status === 'pending') && (
                                <div className="flex items-center text-sm text-blue-600">
                                    <svg className="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span>Crawling in progress...</span>
                                </div>
                            )}

                            {job.status === 'completed' && (
                                <div className="flex items-center text-sm text-green-600">
                                    <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span>Crawl completed successfully!</span>
                                </div>
                            )}

                            {job.status === 'failed' && job.error_message && (
                                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                                    <div className="flex">
                                        <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                        </svg>
                                        <div className="ml-3">
                                            <h3 className="text-sm font-medium text-red-800">Error</h3>
                                            <p className="mt-1 text-sm text-red-700">{job.error_message}</p>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Results Card */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">Results</h2>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-purple-50 rounded-lg p-4">
                                <div className="flex items-center">
                                    <svg className="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                    </svg>
                                    <div className="ml-3">
                                        <p className="text-sm font-medium text-purple-600">Profiles</p>
                                        <p className="text-2xl font-bold text-purple-900">{job.profiles_found}</p>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-indigo-50 rounded-lg p-4">
                                <div className="flex items-center">
                                    <svg className="h-8 w-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                                    </svg>
                                    <div className="ml-3">
                                        <p className="text-sm font-medium text-indigo-600">Posts</p>
                                        <p className="text-2xl font-bold text-indigo-900">{job.posts_found}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {job.profiles_found > 0 && (
                            <div className="mt-6 flex space-x-4">
                                <Link
                                    to="/crawler/profiles"
                                    className="flex-1 text-center px-4 py-2 border border-purple-300 rounded-md text-sm font-medium text-purple-700 bg-purple-50 hover:bg-purple-100"
                                >
                                    View Profiles
                                </Link>
                                {job.posts_found > 0 && (
                                    <Link
                                        to="/crawler/posts"
                                        className="flex-1 text-center px-4 py-2 border border-indigo-300 rounded-md text-sm font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100"
                                    >
                                        View Posts
                                    </Link>
                                )}
                            </div>
                        )}
                    </div>

                    {/* Configuration Card */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">Configuration</h2>

                        <div className="space-y-3">
                            <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Crawl Posts:</span>
                                <span className="text-sm font-medium text-gray-900">
                                    {job.crawl_posts ? `Yes (max ${job.max_posts})` : 'No'}
                                </span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Crawl Followers:</span>
                                <span className="text-sm font-medium text-gray-900">
                                    {job.crawl_followers ? `Yes (max ${job.max_followers})` : 'No'}
                                </span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-sm text-gray-600">Crawl Following:</span>
                                <span className="text-sm font-medium text-gray-900">
                                    {job.crawl_following ? 'Yes' : 'No'}
                                </span>
                            </div>
                            {job.target_url && (
                                <div className="flex justify-between">
                                    <span className="text-sm text-gray-600">Target URL:</span>
                                    <a
                                        href={job.target_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-sm font-medium text-indigo-600 hover:text-indigo-800"
                                    >
                                        View Profile
                                    </a>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Sidebar */}
                <div className="space-y-6">
                    {/* Actions Card */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">Actions</h2>

                        <div className="space-y-3">
                            {(job.status === 'in_progress' || job.status === 'pending') && (
                                <button
                                    onClick={() => cancelMutation.mutate()}
                                    disabled={cancelMutation.isPending}
                                    className="w-full px-4 py-2 border border-red-300 rounded-md text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 disabled:opacity-50"
                                >
                                    {cancelMutation.isPending ? 'Cancelling...' : 'Cancel Job'}
                                </button>
                            )}

                            {job.status === 'failed' && (
                                <button
                                    onClick={() => restartMutation.mutate()}
                                    disabled={restartMutation.isPending}
                                    className="w-full px-4 py-2 border border-indigo-300 rounded-md text-sm font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 disabled:opacity-50"
                                >
                                    {restartMutation.isPending ? 'Restarting...' : 'Restart Job'}
                                </button>
                            )}

                            {(job.status === 'completed' || job.status === 'failed' || job.status === 'cancelled') && (
                                <button
                                    onClick={() => {
                                        if (confirm('Are you sure you want to delete this job? This action cannot be undone.')) {
                                            deleteMutation.mutate();
                                        }
                                    }}
                                    disabled={deleteMutation.isPending}
                                    className="w-full px-4 py-2 border border-red-300 rounded-md text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 disabled:opacity-50"
                                >
                                    {deleteMutation.isPending ? 'Deleting...' : 'Delete Job'}
                                </button>
                            )}

                            <Link
                                to="/crawler/new"
                                className="block w-full px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 text-center"
                            >
                                Create New Job
                            </Link>
                        </div>
                    </div>

                    {/* Timestamps Card */}
                    <div className="bg-white rounded-lg shadow p-6">
                        <h2 className="text-lg font-semibold text-gray-900 mb-4">Timeline</h2>

                        <div className="space-y-4">
                            <div>
                                <p className="text-xs text-gray-500 uppercase tracking-wide">Created</p>
                                <p className="text-sm font-medium text-gray-900">{formatDate(job.created_at)}</p>
                            </div>

                            {job.started_at && (
                                <div>
                                    <p className="text-xs text-gray-500 uppercase tracking-wide">Started</p>
                                    <p className="text-sm font-medium text-gray-900">{formatDate(job.started_at)}</p>
                                </div>
                            )}

                            {job.completed_at && (
                                <div>
                                    <p className="text-xs text-gray-500 uppercase tracking-wide">Completed</p>
                                    <p className="text-sm font-medium text-gray-900">{formatDate(job.completed_at)}</p>
                                </div>
                            )}

                            {job.started_at && (
                                <div>
                                    <p className="text-xs text-gray-500 uppercase tracking-wide">Duration</p>
                                    <p className="text-sm font-medium text-gray-900">
                                        {formatDuration(job.started_at, job.completed_at)}
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Info Card */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <div className="ml-3">
                                <p className="text-sm text-blue-700">
                                    Job ID: <code className="font-mono text-xs">{job.id}</code>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CrawlJobDetail;
