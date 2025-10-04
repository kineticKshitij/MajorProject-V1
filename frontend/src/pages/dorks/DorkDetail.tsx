import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { dorksService } from '../../services/dorksService';

const DorkDetail = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

    // Fetch dork details
    const { data: dork, isLoading, error } = useQuery({
        queryKey: ['dork', id],
        queryFn: () => dorksService.getDork(Number(id)),
        enabled: !!id,
    });

    // Execute mutation
    const executeMutation = useMutation({
        mutationFn: () => dorksService.executeDork(Number(id)),
        onSuccess: (data) => {
            window.open(data.search_url, '_blank');
            queryClient.invalidateQueries({ queryKey: ['dork', id] });
        },
    });

    // Bookmark mutation
    const bookmarkMutation = useMutation({
        mutationFn: () => dorksService.toggleBookmark(Number(id)),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['dork', id] });
        },
    });

    // Delete mutation
    const deleteMutation = useMutation({
        mutationFn: () => dorksService.deleteDork(Number(id)),
        onSuccess: () => {
            navigate('/dorks');
        },
    });

    const handleExecute = () => {
        executeMutation.mutate();
    };

    const handleBookmark = () => {
        bookmarkMutation.mutate();
    };

    const handleDelete = () => {
        deleteMutation.mutate();
    };

    const getRiskBadgeColor = (risk: string) => {
        switch (risk.toLowerCase()) {
            case 'critical':
                return 'bg-red-100 text-red-800 border-red-200';
            case 'high':
                return 'bg-orange-100 text-orange-800 border-orange-200';
            case 'medium':
                return 'bg-yellow-100 text-yellow-800 border-yellow-200';
            case 'low':
                return 'bg-green-100 text-green-800 border-green-200';
            default:
                return 'bg-gray-100 text-gray-800 border-gray-200';
        }
    };

    const getDifficultyBadgeColor = (difficulty: string | undefined) => {
        if (!difficulty) return 'bg-gray-100 text-gray-800 border-gray-200';
        switch (difficulty.toLowerCase()) {
            case 'beginner':
                return 'bg-blue-100 text-blue-800 border-blue-200';
            case 'intermediate':
                return 'bg-indigo-100 text-indigo-800 border-indigo-200';
            case 'advanced':
                return 'bg-purple-100 text-purple-800 border-purple-200';
            default:
                return 'bg-gray-100 text-gray-800 border-gray-200';
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                    <p className="mt-4 text-gray-600">Loading dork details...</p>
                </div>
            </div>
        );
    }

    if (error || !dork) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900">Dork not found</h2>
                    <p className="mt-2 text-gray-600">The dork you're looking for doesn't exist.</p>
                    <Link to="/dorks" className="mt-4 inline-block btn-primary">
                        Back to Dorks
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Back Button */}
                <Link
                    to="/dorks"
                    className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-6"
                >
                    ← Back to Dorks
                </Link>

                {/* Header */}
                <div className="card mb-6">
                    <div className="flex justify-between items-start mb-4">
                        <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                                <h1 className="text-3xl font-bold text-gray-900">{dork.title}</h1>
                                {dork.is_active && (
                                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                                        Active
                                    </span>
                                )}
                            </div>
                            <p className="text-gray-600">{dork.description}</p>
                        </div>
                    </div>

                    {/* Badges */}
                    <div className="flex flex-wrap gap-2 mb-4">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 border border-primary-200">
                            📁 {dork.category_name}
                        </span>
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getRiskBadgeColor(dork.risk_level)}`}>
                            ⚠️ {dork.risk_level}
                        </span>
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getDifficultyBadgeColor(dork.difficulty_level)}`}>
                            🎯 {dork.difficulty_level}
                        </span>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-3">
                        <button
                            onClick={handleExecute}
                            disabled={executeMutation.isPending}
                            className="btn-primary"
                        >
                            {executeMutation.isPending ? 'Executing...' : '🚀 Execute Dork'}
                        </button>
                        <button
                            onClick={handleBookmark}
                            disabled={bookmarkMutation.isPending}
                            className="btn-secondary"
                        >
                            {dork.is_bookmarked ? '⭐ Bookmarked' : '☆ Bookmark'}
                        </button>
                        <Link
                            to={`/dorks/${id}/edit`}
                            className="btn-secondary"
                        >
                            ✏️ Edit
                        </Link>
                        <button
                            onClick={() => setShowDeleteConfirm(true)}
                            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                        >
                            🗑️ Delete
                        </button>
                    </div>
                </div>

                {/* Query Section */}
                <div className="card mb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-3">Search Query</h2>
                    <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm overflow-x-auto mb-3">
                        {dork.query}
                    </div>
                    <button
                        onClick={() => navigator.clipboard.writeText(dork.query)}
                        className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                    >
                        📋 Copy Query
                    </button>
                </div>

                {/* Example Usage */}
                {dork.example_usage && (
                    <div className="card mb-6">
                        <h2 className="text-xl font-semibold text-gray-900 mb-3">Example Usage</h2>
                        <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                            {dork.example_usage}
                        </div>
                    </div>
                )}

                {/* Notes */}
                {dork.notes && (
                    <div className="card mb-6">
                        <h2 className="text-xl font-semibold text-gray-900 mb-3">Notes</h2>
                        <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                            {dork.notes}
                        </div>
                    </div>
                )}

                {/* Tags */}
                {dork.tags && (
                    <div className="card mb-6">
                        <h2 className="text-xl font-semibold text-gray-900 mb-3">Tags</h2>
                        <div className="flex flex-wrap gap-2">
                            {dork.tags.split(',').map((tag, index) => (
                                <span
                                    key={index}
                                    className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-800"
                                >
                                    #{tag.trim()}
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                {/* Metadata */}
                <div className="card">
                    <h2 className="text-xl font-semibold text-gray-900 mb-3">Metadata</h2>
                    <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <dt className="text-sm font-medium text-gray-500">Executions</dt>
                            <dd className="mt-1 text-sm text-gray-900">{dork.execution_count}</dd>
                        </div>
                        <div>
                            <dt className="text-sm font-medium text-gray-500">Created By</dt>
                            <dd className="mt-1 text-sm text-gray-900">{dork.created_by_username || 'Unknown'}</dd>
                        </div>
                        <div>
                            <dt className="text-sm font-medium text-gray-500">Created</dt>
                            <dd className="mt-1 text-sm text-gray-900">
                                {new Date(dork.created_at).toLocaleString()}
                            </dd>
                        </div>
                        <div>
                            <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                            <dd className="mt-1 text-sm text-gray-900">
                                {new Date(dork.updated_at).toLocaleString()}
                            </dd>
                        </div>
                    </dl>
                </div>

                {/* Delete Confirmation Modal */}
                {showDeleteConfirm && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                Delete Dork?
                            </h3>
                            <p className="text-gray-600 mb-6">
                                Are you sure you want to delete "{dork.title}"? This action cannot be undone.
                            </p>
                            <div className="flex gap-3 justify-end">
                                <button
                                    onClick={() => setShowDeleteConfirm(false)}
                                    className="btn-secondary"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={handleDelete}
                                    disabled={deleteMutation.isPending}
                                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                                >
                                    {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DorkDetail;
