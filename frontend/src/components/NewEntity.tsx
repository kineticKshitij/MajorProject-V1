import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';
import type { Entity } from '../types';

interface FormData {
    name: string;
    entity_type: number | '';
    aliases: string;
    description: string;
    industry: string;
    location: string;
    founded_date: string;
    website: string;
    domains: string;
    social_media: {
        linkedin?: string;
        twitter?: string;
        facebook?: string;
        github?: string;
        instagram?: string;
    };
    tags: string;
    status: 'active' | 'completed' | 'on_hold' | 'archived';
    priority: 'low' | 'medium' | 'high' | 'critical';
}

const NewEntity: React.FC = () => {
    const navigate = useNavigate();
    const queryClient = useQueryClient();

    // Fetch entity types for dropdown
    const { data: entityTypesData, isLoading: loadingTypes } = useQuery({
        queryKey: ['entity-types'],
        queryFn: entitiesService.getEntityTypes,
    });

    // Ensure entityTypes is always an array
    const entityTypes = Array.isArray(entityTypesData) ? entityTypesData : [];

    // Initialize form data
    const [formData, setFormData] = useState<FormData>({
        name: '',
        entity_type: '',
        aliases: '',
        description: '',
        industry: '',
        location: '',
        founded_date: '',
        website: '',
        domains: '',
        social_media: {},
        tags: '',
        status: 'active',
        priority: 'medium',
    });

    const [errors, setErrors] = useState<Record<string, string>>({});

    // Create mutation
    const mutation = useMutation({
        mutationFn: (data: Partial<Entity>) => entitiesService.createEntity(data),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['entities'] });
            navigate(`/entities/${data.id}`);
        },
        onError: (error: Error & { response?: { data?: Record<string, string | string[]> } }) => {
            console.error('Failed to create entity:', error);
            if (error.response?.data) {
                // Convert array errors to string
                const normalizedErrors = Object.entries(error.response.data).reduce((acc, [key, value]) => {
                    acc[key] = Array.isArray(value) ? value.join(', ') : value;
                    return acc;
                }, {} as Record<string, string>);
                setErrors(normalizedErrors);
            }
        },
    });

    const handleInputChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
    ) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
        if (errors[name]) {
            setErrors((prev) => ({ ...prev, [name]: '' }));
        }
    };

    const handleSocialMediaChange = (platform: string, value: string) => {
        setFormData((prev) => ({
            ...prev,
            social_media: {
                ...prev.social_media,
                [platform]: value,
            },
        }));
    };

    const validateForm = (): boolean => {
        const newErrors: Record<string, string> = {};

        if (!formData.name.trim()) {
            newErrors.name = 'Name is required';
        }

        if (!formData.entity_type) {
            newErrors.entity_type = 'Entity type is required';
        }

        if (formData.website && !isValidUrl(formData.website)) {
            newErrors.website = 'Invalid URL format';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const isValidUrl = (url: string): boolean => {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        // Prepare data for API
        const submitData: Partial<Entity> = {
            name: formData.name.trim(),
            entity_type: Number(formData.entity_type),
            description: formData.description.trim() || undefined,
            industry: formData.industry.trim() || undefined,
            location: formData.location.trim() || undefined,
            founded_date: formData.founded_date || undefined,
            website: formData.website.trim() || undefined,
            status: formData.status,
            priority: formData.priority,
        };

        // Parse arrays
        if (formData.aliases.trim()) {
            submitData.aliases = formData.aliases
                .split(',')
                .map((a) => a.trim())
                .filter(Boolean);
        }

        if (formData.domains.trim()) {
            submitData.domains = formData.domains
                .split(',')
                .map((d) => d.trim())
                .filter(Boolean);
        }

        if (formData.tags.trim()) {
            submitData.tags = formData.tags
                .split(',')
                .map((t) => t.trim())
                .filter(Boolean);
        }

        // Clean social media
        const cleanedSocialMedia = Object.entries(formData.social_media)
            .filter(([, value]) => value && value.trim())
            .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});

        if (Object.keys(cleanedSocialMedia).length > 0) {
            submitData.social_media = cleanedSocialMedia;
        }

        mutation.mutate(submitData);
    };

    if (loadingTypes) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto px-4 py-8">
            {/* Header */}
            <div className="mb-8">
                <button
                    onClick={() => navigate(-1)}
                    className="text-gray-600 hover:text-gray-900 mb-4 flex items-center"
                >
                    <span className="mr-2">←</span> Back
                </button>
                <h1 className="text-3xl font-bold text-gray-900">Create New Entity</h1>
                <p className="text-gray-600 mt-2">Add a new entity to research</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-8 bg-white rounded-lg shadow-lg p-6">
                {/* Basic Information */}
                <div className="border-b pb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                        Basic Information
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Name */}
                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Name <span className="text-red-500">*</span>
                            </label>
                            <input
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleInputChange}
                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.name ? 'border-red-500' : 'border-gray-300'
                                    }`}
                                placeholder="e.g., Acme Corporation"
                            />
                            {errors.name && (
                                <p className="text-red-500 text-sm mt-1">{errors.name}</p>
                            )}
                        </div>

                        {/* Entity Type */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Entity Type <span className="text-red-500">*</span>
                            </label>
                            <select
                                name="entity_type"
                                value={formData.entity_type}
                                onChange={handleInputChange}
                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.entity_type ? 'border-red-500' : 'border-gray-300'
                                    }`}
                            >
                                <option value="">Select type...</option>
                                {entityTypes.map((type) => (
                                    <option key={type.id} value={type.id}>
                                        {type.icon} {type.name}
                                    </option>
                                ))}
                            </select>
                            {errors.entity_type && (
                                <p className="text-red-500 text-sm mt-1">{errors.entity_type}</p>
                            )}
                        </div>

                        {/* Status */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Status
                            </label>
                            <select
                                name="status"
                                value={formData.status}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="active">Active</option>
                                <option value="completed">Completed</option>
                                <option value="on_hold">On Hold</option>
                                <option value="archived">Archived</option>
                            </select>
                        </div>

                        {/* Priority */}
                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Priority
                            </label>
                            <select
                                name="priority"
                                value={formData.priority}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                <option value="low">↓ Low</option>
                                <option value="medium">→ Medium</option>
                                <option value="high">↑ High</option>
                                <option value="critical">🔴 Critical</option>
                            </select>
                        </div>

                        {/* Description */}
                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Description
                            </label>
                            <textarea
                                name="description"
                                value={formData.description}
                                onChange={handleInputChange}
                                rows={4}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Brief description of the entity..."
                            />
                        </div>

                        {/* Industry */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Industry
                            </label>
                            <input
                                type="text"
                                name="industry"
                                value={formData.industry}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="e.g., Technology, Healthcare"
                            />
                        </div>

                        {/* Location */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Location
                            </label>
                            <input
                                type="text"
                                name="location"
                                value={formData.location}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="e.g., San Francisco, CA"
                            />
                        </div>

                        {/* Founded Date */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Founded Date
                            </label>
                            <input
                                type="date"
                                name="founded_date"
                                value={formData.founded_date}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        {/* Website */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Website
                            </label>
                            <input
                                type="url"
                                name="website"
                                value={formData.website}
                                onChange={handleInputChange}
                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.website ? 'border-red-500' : 'border-gray-300'
                                    }`}
                                placeholder="https://example.com"
                            />
                            {errors.website && (
                                <p className="text-red-500 text-sm mt-1">{errors.website}</p>
                            )}
                        </div>

                        {/* Aliases */}
                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Aliases
                            </label>
                            <input
                                type="text"
                                name="aliases"
                                value={formData.aliases}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Comma-separated, e.g., Acme Corp, Acme Inc"
                            />
                        </div>

                        {/* Domains */}
                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Domains
                            </label>
                            <input
                                type="text"
                                name="domains"
                                value={formData.domains}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Comma-separated, e.g., example.com, example.org"
                            />
                        </div>

                        {/* Tags */}
                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Tags
                            </label>
                            <input
                                type="text"
                                name="tags"
                                value={formData.tags}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Comma-separated, e.g., tech, startup, ai"
                            />
                        </div>
                    </div>
                </div>

                {/* Social Media */}
                <div className="border-b pb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                        Social Media (Optional)
                    </h2>
                    <div className="space-y-3">
                        <div className="flex items-center gap-3">
                            <span className="w-24 text-sm text-gray-600">LinkedIn:</span>
                            <input
                                type="url"
                                value={formData.social_media.linkedin || ''}
                                onChange={(e) => handleSocialMediaChange('linkedin', e.target.value)}
                                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="https://linkedin.com/company/..."
                            />
                        </div>

                        <div className="flex items-center gap-3">
                            <span className="w-24 text-sm text-gray-600">Twitter:</span>
                            <input
                                type="url"
                                value={formData.social_media.twitter || ''}
                                onChange={(e) => handleSocialMediaChange('twitter', e.target.value)}
                                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="https://twitter.com/..."
                            />
                        </div>

                        <div className="flex items-center gap-3">
                            <span className="w-24 text-sm text-gray-600">Facebook:</span>
                            <input
                                type="url"
                                value={formData.social_media.facebook || ''}
                                onChange={(e) => handleSocialMediaChange('facebook', e.target.value)}
                                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="https://facebook.com/..."
                            />
                        </div>

                        <div className="flex items-center gap-3">
                            <span className="w-24 text-sm text-gray-600">GitHub:</span>
                            <input
                                type="url"
                                value={formData.social_media.github || ''}
                                onChange={(e) => handleSocialMediaChange('github', e.target.value)}
                                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="https://github.com/..."
                            />
                        </div>

                        <div className="flex items-center gap-3">
                            <span className="w-24 text-sm text-gray-600">Instagram:</span>
                            <input
                                type="url"
                                value={formData.social_media.instagram || ''}
                                onChange={(e) => handleSocialMediaChange('instagram', e.target.value)}
                                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="https://instagram.com/..."
                            />
                        </div>
                    </div>
                </div>

                {/* Form Actions */}
                <div className="flex items-center justify-between pt-6 border-t">
                    <button
                        type="button"
                        onClick={() => navigate(-1)}
                        className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                        disabled={mutation.isPending}
                    >
                        Cancel
                    </button>

                    <button
                        type="submit"
                        disabled={mutation.isPending}
                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        {mutation.isPending ? (
                            <>
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                <span>Creating...</span>
                            </>
                        ) : (
                            <span>Create Entity</span>
                        )}
                    </button>
                </div>

                {/* Error Message */}
                {mutation.isError && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <p className="text-red-800 text-sm">
                            Failed to create entity. Please check the form and try again.
                        </p>
                    </div>
                )}
            </form>
        </div>
    );
};

export default NewEntity;
