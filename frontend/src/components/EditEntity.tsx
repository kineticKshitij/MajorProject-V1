import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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

const EditEntity: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();

    // Fetch entity to edit
    const { data: entity, isLoading: loadingEntity, error: entityError } = useQuery({
        queryKey: ['entity', id],
        queryFn: () => entitiesService.getEntity(id!),
        enabled: !!id,
    });

    // Fetch entity types for dropdown
    const { data: entityTypesData } = useQuery({
        queryKey: ['entity-types'],
        queryFn: entitiesService.getEntityTypes,
    });

    // Ensure entityTypes is always an array
    const entityTypes = Array.isArray(entityTypesData) ? entityTypesData : [];

    // Form state
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

    // Populate form when entity loads
    useEffect(() => {
        if (entity) {
            setFormData({
                name: entity.name || '',
                entity_type: entity.entity_type || '',
                aliases: Array.isArray(entity.aliases) ? entity.aliases.join(', ') : '',
                description: entity.description || '',
                industry: entity.industry || '',
                location: entity.location || '',
                founded_date: entity.founded_date || '',
                website: entity.website || '',
                domains: Array.isArray(entity.domains) ? entity.domains.join(', ') : '',
                social_media: entity.social_media || {},
                tags: Array.isArray(entity.tags)
                    ? entity.tags.join(', ')
                    : typeof entity.tags === 'string'
                        ? entity.tags
                        : '',
                status: entity.status || 'active',
                priority: entity.priority || 'medium',
            });
        }
    }, [entity]);

    // Update mutation
    const mutation = useMutation({
        mutationFn: (data: Partial<Entity>) =>
            entitiesService.updateEntity(Number(id), data),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['entities'] });
            queryClient.invalidateQueries({ queryKey: ['entity', id] });
            navigate(`/entities/${data.id}`);
        },
        onError: (error: any) => {
            console.error('Failed to update entity:', error);
            if (error.response?.data) {
                setErrors(error.response.data);
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
            .filter(([_, value]) => value && value.trim())
            .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});

        if (Object.keys(cleanedSocialMedia).length > 0) {
            submitData.social_media = cleanedSocialMedia;
        }

        mutation.mutate(submitData);
    };

    if (loadingEntity) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (entityError || !entity) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Entity Not Found</h2>
                    <p className="text-gray-600">The entity you're looking for doesn't exist.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto px-4 py-8">
            {/* Header */}
            <div className="mb-8">
                <button
                    onClick={() => navigate(`/entities/${id}`)}
                    className="text-gray-600 hover:text-gray-900 mb-4 flex items-center"
                >
                    <span className="mr-2">←</span> Back to Entity
                </button>
                <h1 className="text-3xl font-bold text-gray-900">Edit Entity</h1>
                <p className="text-gray-600 mt-2">Update entity information</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-8 bg-white rounded-lg shadow-lg p-6">
                {/* Basic Information - Same as NewEntity */}
                <div className="border-b pb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Basic Information</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                            {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
                        </div>

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
                            {errors.entity_type && <p className="text-red-500 text-sm mt-1">{errors.entity_type}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
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

                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
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

                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                            <textarea
                                name="description"
                                value={formData.description}
                                onChange={handleInputChange}
                                rows={4}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Brief description..."
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                            <input
                                type="text"
                                name="industry"
                                value={formData.industry}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="e.g., Technology"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                            <input
                                type="text"
                                name="location"
                                value={formData.location}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="e.g., San Francisco, CA"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Founded Date</label>
                            <input
                                type="date"
                                name="founded_date"
                                value={formData.founded_date}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Website</label>
                            <input
                                type="url"
                                name="website"
                                value={formData.website}
                                onChange={handleInputChange}
                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.website ? 'border-red-500' : 'border-gray-300'
                                    }`}
                                placeholder="https://example.com"
                            />
                            {errors.website && <p className="text-red-500 text-sm mt-1">{errors.website}</p>}
                        </div>

                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Aliases</label>
                            <input
                                type="text"
                                name="aliases"
                                value={formData.aliases}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Comma-separated"
                            />
                        </div>

                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Domains</label>
                            <input
                                type="text"
                                name="domains"
                                value={formData.domains}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Comma-separated"
                            />
                        </div>

                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
                            <input
                                type="text"
                                name="tags"
                                value={formData.tags}
                                onChange={handleInputChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Comma-separated"
                            />
                        </div>
                    </div>
                </div>

                {/* Social Media */}
                <div className="border-b pb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Social Media</h2>
                    <div className="space-y-3">
                        {['linkedin', 'twitter', 'facebook', 'github', 'instagram'].map((platform) => (
                            <div key={platform} className="flex items-center gap-3">
                                <span className="w-24 text-sm text-gray-600 capitalize">{platform}:</span>
                                <input
                                    type="url"
                                    value={formData.social_media[platform as keyof typeof formData.social_media] || ''}
                                    onChange={(e) => handleSocialMediaChange(platform, e.target.value)}
                                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={`https://${platform}.com/...`}
                                />
                            </div>
                        ))}
                    </div>
                </div>

                {/* Form Actions */}
                <div className="flex items-center justify-between pt-6 border-t">
                    <button
                        type="button"
                        onClick={() => navigate(`/entities/${id}`)}
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
                                <span>Updating...</span>
                            </>
                        ) : (
                            <span>Update Entity</span>
                        )}
                    </button>
                </div>

                {mutation.isError && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <p className="text-red-800 text-sm">
                            Failed to update entity. Please check the form and try again.
                        </p>
                    </div>
                )}
            </form>
        </div>
    );
};

export default EditEntity;
