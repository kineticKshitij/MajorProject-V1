import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { dorksService } from '../../services/dorksService';
import type { GoogleDork } from '../../types';

const DorksList = () => {
    const [page, setPage] = useState(1);
    const [search, setSearch] = useState('');
    const [selectedCategory, setSelectedCategory] = useState<number | undefined>();
    const [riskLevel, setRiskLevel] = useState<string>('');
    const [difficultyLevel, setDifficultyLevel] = useState<string>('');
    const [showBookmarked, setShowBookmarked] = useState(false);
    const [showMyDorks, setShowMyDorks] = useState(false);

    // Fetch categories
    const { data: categoriesData } = useQuery({
        queryKey: ['dorkCategories'],
        queryFn: dorksService.getCategories,
    });

    const categories = categoriesData?.results || [];

    // Fetch dorks with filters
    const { data: dorksData, isLoading, refetch } = useQuery({
        queryKey: ['dorks', page, search, selectedCategory, riskLevel, difficultyLevel, showBookmarked, showMyDorks],
        queryFn: () =>
            dorksService.getDorks({
                page,
                search: search || undefined,
                category: selectedCategory,
                risk_level: riskLevel || undefined,
                difficulty: difficultyLevel || undefined,
                bookmarked: showBookmarked || undefined,
                my_dorks: showMyDorks || undefined,
            }),
    });

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        setPage(1);
        refetch();
    };

    const handlePageChange = (newPage: number) => {
        setPage(newPage);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const getRiskBadgeColor = (risk: string) => {
        switch (risk.toLowerCase()) {
            case 'critical':
                return 'bg-red-100 text-red-800';
            case 'high':
                return 'bg-orange-100 text-orange-800';
            case 'medium':
                return 'bg-yellow-100 text-yellow-800';
            case 'low':
                return 'bg-green-100 text-green-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getDifficultyBadgeColor = (difficulty: string) => {
        switch (difficulty.toLowerCase()) {
            case 'beginner':
                return 'bg-blue-100 text-blue-800';
            case 'intermediate':
                return 'bg-indigo-100 text-indigo-800';
            case 'advanced':
                return 'bg-purple-100 text-purple-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex justify-between items-center">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">Google Dorks</h1>
                            <p className="mt-2 text-gray-600">
                                Browse and execute powerful Google search queries
                            </p>
                        </div>
                        <Link
                            to="/dorks/create"
                            className="btn-primary"
                        >
                            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                            </svg>
                            Create Dork
                        </Link>
                    </div>
                </div>

                {/* Search and Filters */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <form onSubmit={handleSearch} className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {/* Search */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Search
                                </label>
                                <input
                                    type="text"
                                    value={search}
                                    onChange={(e) => setSearch(e.target.value)}
                                    placeholder="Search dorks..."
                                    className="input-field"
                                />
                            </div>

                            {/* Category Filter */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Category
                                </label>
                                <select
                                    value={selectedCategory || ''}
                                    onChange={(e) => setSelectedCategory(e.target.value ? parseInt(e.target.value) : undefined)}
                                    className="input-field"
                                >
                                    <option value="">All Categories</option>
                                    {categories.map((cat) => (
                                        <option key={cat.id} value={cat.id}>
                                            {cat.name}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {/* Risk Level Filter */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Risk Level
                                </label>
                                <select
                                    value={riskLevel}
                                    onChange={(e) => setRiskLevel(e.target.value)}
                                    className="input-field"
                                >
                                    <option value="">All Risk Levels</option>
                                    <option value="low">Low</option>
                                    <option value="medium">Medium</option>
                                    <option value="high">High</option>
                                    <option value="critical">Critical</option>
                                </select>
                            </div>

                            {/* Difficulty Filter */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Difficulty
                                </label>
                                <select
                                    value={difficultyLevel}
                                    onChange={(e) => setDifficultyLevel(e.target.value)}
                                    className="input-field"
                                >
                                    <option value="">All Difficulties</option>
                                    <option value="beginner">Beginner</option>
                                    <option value="intermediate">Intermediate</option>
                                    <option value="advanced">Advanced</option>
                                </select>
                            </div>

                            {/* Toggle Filters */}
                            <div className="flex items-end space-x-4">
                                <label className="flex items-center">
                                    <input
                                        type="checkbox"
                                        checked={showBookmarked}
                                        onChange={(e) => setShowBookmarked(e.target.checked)}
                                        className="rounded text-primary-600 focus:ring-primary-500"
                                    />
                                    <span className="ml-2 text-sm text-gray-700">Bookmarked</span>
                                </label>
                                <label className="flex items-center">
                                    <input
                                        type="checkbox"
                                        checked={showMyDorks}
                                        onChange={(e) => setShowMyDorks(e.target.checked)}
                                        className="rounded text-primary-600 focus:ring-primary-500"
                                    />
                                    <span className="ml-2 text-sm text-gray-700">My Dorks</span>
                                </label>
                            </div>
                        </div>

                        <div className="flex gap-2">
                            <button type="submit" className="btn-primary">
                                Search
                            </button>
                            <button
                                type="button"
                                onClick={() => {
                                    setSearch('');
                                    setSelectedCategory(undefined);
                                    setRiskLevel('');
                                    setDifficultyLevel('');
                                    setShowBookmarked(false);
                                    setShowMyDorks(false);
                                    setPage(1);
                                }}
                                className="btn-secondary"
                            >
                                Clear Filters
                            </button>
                        </div>
                    </form>
                </div>

                {/* Results */}
                {isLoading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                        <p className="mt-4 text-gray-600">Loading dorks...</p>
                    </div>
                ) : (
                    <>
                        {/* Results Count */}
                        <div className="mb-4 text-sm text-gray-600">
                            Found {dorksData?.count || 0} dorks
                        </div>

                        {/* Dorks Grid */}
                        <div className="space-y-4 mb-6">
                            {dorksData?.results.map((dork: GoogleDork) => (
                                <div
                                    key={dork.id}
                                    className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
                                >
                                    <div className="flex justify-between items-start">
                                        <div className="flex-1">
                                            <div className="flex items-start justify-between mb-3">
                                                <Link
                                                    to={`/dorks/${dork.id}`}
                                                    className="text-xl font-semibold text-gray-900 hover:text-primary-600"
                                                >
                                                    {dork.title}
                                                </Link>
                                                {dork.is_bookmarked && (
                                                    <span className="ml-2 text-yellow-500">
                                                        ⭐
                                                    </span>
                                                )}
                                            </div>

                                            <p className="text-gray-600 mb-3">{dork.description}</p>

                                            <div className="bg-gray-900 text-gray-100 p-3 rounded-md mb-3 font-mono text-sm overflow-x-auto">
                                                {dork.query}
                                            </div>

                                            <div className="flex flex-wrap gap-2 mb-3">
                                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                                                    {dork.category_name}
                                                </span>
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRiskBadgeColor(dork.risk_level)}`}>
                                                    {dork.risk_level}
                                                </span>
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getDifficultyBadgeColor(dork.difficulty)}`}>
                                                    {dork.difficulty}
                                                </span>
                                            </div>

                                            <div className="flex items-center gap-4 text-sm text-gray-500">
                                                <span>📊 {dork.usage_count} executions</span>
                                                <span>By {dork.created_by_username || 'Unknown'}</span>
                                                <span>{new Date(dork.created_at).toLocaleDateString()}</span>
                                            </div>
                                        </div>

                                        <div className="flex flex-col gap-2 ml-4">
                                            <Link
                                                to={`/dorks/${dork.id}/execute`}
                                                className="btn-primary text-sm whitespace-nowrap"
                                            >
                                                Execute
                                            </Link>
                                            <Link
                                                to={`/dorks/${dork.id}`}
                                                className="btn-secondary text-sm whitespace-nowrap"
                                            >
                                                View Details
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Pagination */}
                        {dorksData && dorksData.count > 0 && (
                            <div className="flex justify-center items-center gap-2">
                                <button
                                    onClick={() => handlePageChange(page - 1)}
                                    disabled={!dorksData.previous}
                                    className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Previous
                                </button>
                                <span className="px-4 py-2 text-gray-700">
                                    Page {page}
                                </span>
                                <button
                                    onClick={() => handlePageChange(page + 1)}
                                    disabled={!dorksData.next}
                                    className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Next
                                </button>
                            </div>
                        )}

                        {/* Empty State */}
                        {dorksData?.results.length === 0 && (
                            <div className="text-center py-12">
                                <svg
                                    className="mx-auto h-12 w-12 text-gray-400"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                    />
                                </svg>
                                <h3 className="mt-2 text-sm font-medium text-gray-900">No dorks found</h3>
                                <p className="mt-1 text-sm text-gray-500">
                                    Try adjusting your search or filter criteria.
                                </p>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default DorksList;
