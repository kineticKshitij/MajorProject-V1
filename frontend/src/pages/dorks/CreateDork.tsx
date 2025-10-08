import { useState, type FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { dorksService } from '../../services/dorksService';
import type { GoogleDork } from '../../types';

const CreateDork = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        query: '',
        description: '',
        category: '',
        tags: '',
        risk_level: 'low' as 'low' | 'medium' | 'high' | 'critical',
        difficulty_level: 'beginner' as 'beginner' | 'intermediate' | 'advanced',
        example_usage: '',
        notes: '',
        is_active: true,
    });
    const [error, setError] = useState('');

    // Fetch categories
    const { data: categories } = useQuery({
        queryKey: ['dorkCategories'],
        queryFn: dorksService.getCategories,
    });

    // Create mutation
    const createMutation = useMutation({
        mutationFn: (data: Partial<GoogleDork>) => dorksService.createDork(data),
        onSuccess: (data) => {
            navigate(`/dorks/${data.id}`);
        },
        onError: (err: any) => {
            setError(
                err.response?.data?.detail ||
                err.response?.data?.message ||
                'Failed to create dork'
            );
        },
    });

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        setError('');

        if (!formData.title.trim()) {
            setError('Title is required');
            return;
        }
        if (!formData.query.trim()) {
            setError('Query is required');
            return;
        }
        if (!formData.category) {
            setError('Category is required');
            return;
        }

        createMutation.mutate({
            ...formData,
            category: Number(formData.category),
        });
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="mb-6">
                    <Link
                        to="/dorks"
                        className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4"
                    >
                        ← Back to Dorks
                    </Link>
                    <h1 className="text-3xl font-bold text-gray-900">Create New Dork</h1>
                    <p className="mt-2 text-gray-600">
                        Add a new Google dork query to your collection
                    </p>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="mb-6 rounded-md bg-red-50 p-4">
                        <p className="text-sm text-red-800">{error}</p>
                    </div>
                )}

                {/* Form */}
                <form onSubmit={handleSubmit} className="card space-y-6">
                    {/* Title */}
                    <div>
                        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                            Title <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            id="title"
                            required
                            className="input-field"
                            placeholder="e.g., Find Exposed SQL Databases"
                            value={formData.title}
                            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                        />
                    </div>

                    {/* Query */}
                    <div>
                        <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-1">
                            Search Query <span className="text-red-500">*</span>
                        </label>
                        <textarea
                            id="query"
                            required
                            rows={3}
                            className="input-field font-mono text-sm"
                            placeholder='e.g., inurl:"sql" intitle:"phpMyAdmin" intext:"MySQL"'
                            value={formData.query}
                            onChange={(e) => setFormData({ ...formData, query: e.target.value })}
                        />
                        <p className="mt-1 text-xs text-gray-500">
                            Enter the Google dork query exactly as it should be searched
                        </p>
                    </div>

                    {/* Description */}
                    <div>
                        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                            Description <span className="text-red-500">*</span>
                        </label>
                        <textarea
                            id="description"
                            required
                            rows={3}
                            className="input-field"
                            placeholder="Describe what this dork finds and how it can be used..."
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        />
                    </div>

                    {/* Category */}
                    <div>
                        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
                            Category <span className="text-red-500">*</span>
                        </label>
                        <select
                            id="category"
                            required
                            className="input-field"
                            value={formData.category}
                            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                        >
                            <option value="">Select a category</option>
                            {categories?.results?.map((cat: { id: number; name: string }) => (
                                <option key={cat.id} value={cat.id}>
                                    {cat.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Risk and Difficulty */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label htmlFor="risk_level" className="block text-sm font-medium text-gray-700 mb-1">
                                Risk Level <span className="text-red-500">*</span>
                            </label>
                            <select
                                id="risk_level"
                                required
                                className="input-field"
                                value={formData.risk_level}
                                onChange={(e) => setFormData({ ...formData, risk_level: e.target.value as any })}
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                                <option value="critical">Critical</option>
                            </select>
                        </div>

                        <div>
                            <label htmlFor="difficulty_level" className="block text-sm font-medium text-gray-700 mb-1">
                                Difficulty Level <span className="text-red-500">*</span>
                            </label>
                            <select
                                id="difficulty_level"
                                required
                                className="input-field"
                                value={formData.difficulty_level}
                                onChange={(e) => setFormData({ ...formData, difficulty_level: e.target.value as any })}
                            >
                                <option value="beginner">Beginner</option>
                                <option value="intermediate">Intermediate</option>
                                <option value="advanced">Advanced</option>
                            </select>
                        </div>
                    </div>

                    {/* Tags */}
                    <div>
                        <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-1">
                            Tags
                        </label>
                        <input
                            type="text"
                            id="tags"
                            className="input-field"
                            placeholder="sql, database, phpmyadmin (comma-separated)"
                            value={formData.tags}
                            onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                        />
                        <p className="mt-1 text-xs text-gray-500">
                            Separate tags with commas
                        </p>
                    </div>

                    {/* Example Usage */}
                    <div>
                        <label htmlFor="example_usage" className="block text-sm font-medium text-gray-700 mb-1">
                            Example Usage
                        </label>
                        <textarea
                            id="example_usage"
                            rows={4}
                            className="input-field"
                            placeholder="Provide examples of how to use this dork effectively..."
                            value={formData.example_usage}
                            onChange={(e) => setFormData({ ...formData, example_usage: e.target.value })}
                        />
                    </div>

                    {/* Notes */}
                    <div>
                        <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-1">
                            Additional Notes
                        </label>
                        <textarea
                            id="notes"
                            rows={4}
                            className="input-field"
                            placeholder="Any additional information, warnings, or tips..."
                            value={formData.notes}
                            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                        />
                    </div>

                    {/* Active Status */}
                    <div className="flex items-center">
                        <input
                            type="checkbox"
                            id="is_active"
                            checked={formData.is_active}
                            onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                        />
                        <label htmlFor="is_active" className="ml-2 text-sm text-gray-700">
                            Active (make this dork publicly visible)
                        </label>
                    </div>

                    {/* Submit Buttons */}
                    <div className="flex gap-3 pt-4 border-t">
                        <button
                            type="submit"
                            disabled={createMutation.isPending}
                            className="btn-primary"
                        >
                            {createMutation.isPending ? 'Creating...' : 'Create Dork'}
                        </button>
                        <Link to="/dorks" className="btn-secondary">
                            Cancel
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateDork;
