import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import crawlerService from '../services/crawlerService';
import type { CreateCrawlJob, Platform } from '../types/crawler';

const NewCrawlJob = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState<CreateCrawlJob>({
        platform: 'github',
        target_username: '',
        crawl_posts: true,
        crawl_followers: false,
        crawl_following: false,
        max_posts: 50,
        max_followers: 100,
    });

    // Fetch supported platforms
    const { data: platformsData } = useQuery({
        queryKey: ['supported-platforms'],
        queryFn: () => crawlerService.getSupportedPlatforms(),
    });

    // Create job mutation
    const createJobMutation = useMutation({
        mutationFn: (data: CreateCrawlJob) => crawlerService.createJob(data),
        onSuccess: (data) => {
            navigate(`/crawler/jobs/${data.id}`);
        },
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

    const getPlatformDescription = (platform: Platform) => {
        const descriptions: Record<Platform, string> = {
            twitter: 'Crawl tweets, followers, and profile information from Twitter/X',
            github: 'Crawl repositories, stars, and profile information from GitHub',
            linkedin: 'Crawl posts, connections, and profile information from LinkedIn',
            reddit: 'Crawl posts, comments, and user information from Reddit',
            instagram: 'Crawl posts, stories, and profile information from Instagram',
            facebook: 'Crawl posts, friends, and profile information from Facebook',
            tiktok: 'Crawl videos, followers, and profile information from TikTok',
            youtube: 'Crawl videos, subscribers, and channel information from YouTube',
        };
        return descriptions[platform] || 'Crawl social media data';
    };

    const isPlatformSupported = (platform: Platform) => {
        return platformsData?.platforms.includes(platform) ?? false;
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // Validate
        if (!formData.target_username?.trim() && !formData.target_url?.trim()) {
            alert('Please enter a username or URL');
            return;
        }

        // Clean up data before sending - remove empty fields
        const cleanData: CreateCrawlJob = {
            platform: formData.platform,
            crawl_posts: formData.crawl_posts ?? true,
            crawl_followers: formData.crawl_followers ?? false,
            crawl_following: formData.crawl_following ?? false,
            max_posts: formData.max_posts ?? 50,
            max_followers: formData.max_followers ?? 100,
        };

        // Only include non-empty username or URL
        if (formData.target_username?.trim()) {
            cleanData.target_username = formData.target_username.trim();
        }
        if (formData.target_url?.trim()) {
            cleanData.target_url = formData.target_url.trim();
        }
        if (formData.entity) {
            cleanData.entity = formData.entity;
        }

        createJobMutation.mutate(cleanData);
    };

    const handleInputChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
    ) => {
        const { name, value, type } = e.target;

        if (type === 'checkbox') {
            const checked = (e.target as HTMLInputElement).checked;
            setFormData(prev => ({ ...prev, [name]: checked }));
        } else if (type === 'number') {
            setFormData(prev => ({ ...prev, [name]: parseInt(value) || 0 }));
        } else {
            setFormData(prev => ({ ...prev, [name]: value }));
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
                <h1 className="text-3xl font-bold text-gray-900">Create New Crawl Job</h1>
                <p className="mt-2 text-gray-600">
                    Select a platform and configure your social media crawl
                </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Platform Selection */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Select Platform</h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        {(['github', 'reddit', 'twitter', 'linkedin', 'instagram', 'facebook', 'tiktok', 'youtube'] as Platform[]).map((platform) => {
                            const supported = isPlatformSupported(platform);
                            return (
                                <button
                                    key={platform}
                                    type="button"
                                    onClick={() => setFormData(prev => ({ ...prev, platform }))}
                                    disabled={!supported}
                                    className={`relative p-4 rounded-lg border-2 transition-all ${formData.platform === platform
                                        ? 'border-indigo-600 bg-indigo-50'
                                        : supported
                                            ? 'border-gray-300 hover:border-indigo-300'
                                            : 'border-gray-200 bg-gray-50 cursor-not-allowed opacity-60'
                                        }`}
                                >
                                    <div className="flex flex-col items-center text-center">
                                        <span className="text-4xl mb-2">{getPlatformIcon(platform)}</span>
                                        <span className={`text-sm font-medium capitalize ${formData.platform === platform ? 'text-indigo-900' : 'text-gray-900'
                                            }`}>
                                            {platform}
                                        </span>
                                        {!supported && (
                                            <span className="text-xs text-red-600 mt-1">Coming Soon</span>
                                        )}
                                    </div>
                                    {formData.platform === platform && (
                                        <div className="absolute top-2 right-2">
                                            <svg className="w-5 h-5 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                            </svg>
                                        </div>
                                    )}
                                </button>
                            );
                        })}
                    </div>

                    {formData.platform && (
                        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                            <p className="text-sm text-blue-800">
                                <strong className="capitalize">{formData.platform}:</strong> {getPlatformDescription(formData.platform)}
                            </p>
                        </div>
                    )}
                </div>

                {/* Target Configuration */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Target Configuration</h2>

                    <div className="space-y-4">
                        <div>
                            <label htmlFor="target_username" className="block text-sm font-medium text-gray-700 mb-1">
                                Username <span className="text-red-500">*</span>
                            </label>
                            <div className="relative rounded-md shadow-sm">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <span className="text-gray-500 sm:text-sm">@</span>
                                </div>
                                <input
                                    type="text"
                                    name="target_username"
                                    id="target_username"
                                    value={formData.target_username}
                                    onChange={handleInputChange}
                                    className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-8 pr-12 sm:text-sm border-gray-300 rounded-md"
                                    placeholder="username"
                                    required={!formData.target_url}
                                />
                            </div>
                            <p className="mt-1 text-sm text-gray-500">
                                Enter the username of the profile you want to crawl
                            </p>
                        </div>

                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-300"></div>
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-white text-gray-500">OR</span>
                            </div>
                        </div>

                        <div>
                            <label htmlFor="target_url" className="block text-sm font-medium text-gray-700 mb-1">
                                Profile URL
                            </label>
                            <input
                                type="url"
                                name="target_url"
                                id="target_url"
                                value={formData.target_url || ''}
                                onChange={handleInputChange}
                                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                placeholder={`https://${formData.platform}.com/username`}
                            />
                            <p className="mt-1 text-sm text-gray-500">
                                Or provide the full URL to the profile
                            </p>
                        </div>
                    </div>
                </div>

                {/* Crawl Options */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Crawl Options</h2>

                    <div className="space-y-4">
                        {/* Crawl Posts */}
                        <div className="flex items-start">
                            <div className="flex items-center h-5">
                                <input
                                    id="crawl_posts"
                                    name="crawl_posts"
                                    type="checkbox"
                                    checked={formData.crawl_posts}
                                    onChange={handleInputChange}
                                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                />
                            </div>
                            <div className="ml-3 text-sm">
                                <label htmlFor="crawl_posts" className="font-medium text-gray-700">
                                    Crawl Posts/Content
                                </label>
                                <p className="text-gray-500">
                                    Collect posts, tweets, repositories, or other content from the profile
                                </p>
                                {formData.crawl_posts && (
                                    <div className="mt-2">
                                        <label htmlFor="max_posts" className="block text-xs font-medium text-gray-600 mb-1">
                                            Maximum Posts
                                        </label>
                                        <input
                                            type="number"
                                            name="max_posts"
                                            id="max_posts"
                                            value={formData.max_posts}
                                            onChange={handleInputChange}
                                            min="1"
                                            max="500"
                                            className="focus:ring-indigo-500 focus:border-indigo-500 block w-32 sm:text-sm border-gray-300 rounded-md"
                                        />
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Crawl Followers */}
                        <div className="flex items-start">
                            <div className="flex items-center h-5">
                                <input
                                    id="crawl_followers"
                                    name="crawl_followers"
                                    type="checkbox"
                                    checked={formData.crawl_followers}
                                    onChange={handleInputChange}
                                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                />
                            </div>
                            <div className="ml-3 text-sm">
                                <label htmlFor="crawl_followers" className="font-medium text-gray-700">
                                    Crawl Followers
                                </label>
                                <p className="text-gray-500">
                                    Collect information about the profile's followers
                                </p>
                                {formData.crawl_followers && (
                                    <div className="mt-2">
                                        <label htmlFor="max_followers" className="block text-xs font-medium text-gray-600 mb-1">
                                            Maximum Followers
                                        </label>
                                        <input
                                            type="number"
                                            name="max_followers"
                                            id="max_followers"
                                            value={formData.max_followers}
                                            onChange={handleInputChange}
                                            min="1"
                                            max="1000"
                                            className="focus:ring-indigo-500 focus:border-indigo-500 block w-32 sm:text-sm border-gray-300 rounded-md"
                                        />
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Crawl Following */}
                        <div className="flex items-start">
                            <div className="flex items-center h-5">
                                <input
                                    id="crawl_following"
                                    name="crawl_following"
                                    type="checkbox"
                                    checked={formData.crawl_following}
                                    onChange={handleInputChange}
                                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                />
                            </div>
                            <div className="ml-3 text-sm">
                                <label htmlFor="crawl_following" className="font-medium text-gray-700">
                                    Crawl Following
                                </label>
                                <p className="text-gray-500">
                                    Collect information about accounts the profile is following
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Information Box */}
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <div className="ml-3">
                            <h3 className="text-sm font-medium text-yellow-800">Important Notes</h3>
                            <div className="mt-2 text-sm text-yellow-700">
                                <ul className="list-disc list-inside space-y-1">
                                    <li>Crawling will start immediately after submission</li>
                                    <li>Large jobs may take several minutes to complete</li>
                                    <li>Respect platform rate limits and terms of service</li>
                                    <li>Currently supported: GitHub & Reddit (no API key needed)</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Error Message */}
                {createJobMutation.isError && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <div className="flex">
                            <div className="flex-shrink-0">
                                <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <div className="ml-3">
                                <h3 className="text-sm font-medium text-red-800">Error creating crawl job</h3>
                                <p className="mt-1 text-sm text-red-700">
                                    {createJobMutation.error instanceof Error
                                        ? createJobMutation.error.message
                                        : 'An error occurred. Please try again.'}
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Actions */}
                <div className="flex items-center justify-end space-x-4">
                    <button
                        type="button"
                        onClick={() => navigate('/crawler')}
                        className="px-6 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={createJobMutation.isPending || !isPlatformSupported(formData.platform)}
                        className="px-6 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {createJobMutation.isPending ? (
                            <span className="flex items-center">
                                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Creating...
                            </span>
                        ) : (
                            'Start Crawl'
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default NewCrawlJob;
