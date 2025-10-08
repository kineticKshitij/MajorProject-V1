import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';
import type { Entity, EntityType } from '../types';

interface EntityFormProps {
    entity?: Entity;
    isEdit?: boolean;
}

interface FormData {
    name: string;
    entity_type_id: number | '';
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

const EntityForm: React.FC<EntityFormProps> = ({ entity, isEdit = false }) => {
    const navigate = useNavigate();
    const queryClient = useQueryClient();

    // Fetch entity types for dropdown
    const { data: entityTypes = [], isLoading: loadingTypes } = useQuery({
        queryKey: ['entity-types'],
        queryFn: entitiesService.getEntityTypes,
    });

    // Initialize form data
    const [formData, setFormData] = useState<FormData>({
        name: '',
        entity_type_id: '',
        aliases: '',
        description: '',
        industry: '',
        location: '',
        founded_date: '',
        website: '',
        domains: '',
        social_media: {
            linkedin: '',
            twitter: '',
            facebook: '',
            github: '',
            instagram: '',
        },
        tags: '',
        status: 'active',
        priority: 'medium',
    });

    // Populate form with entity data when editing
    useEffect(() => {
        if (entity && isEdit) {
            setFormData({
                name: entity.name || '',
                entity_type_id: entity.entity_type_data?.id ?? entity.entity_type,
                aliases: Array.isArray(entity.aliases) ? entity.aliases.join(', ') : '',
                description: entity.description || '',
                industry: entity.industry || '',
                location: entity.location || '',
                founded_date: entity.founded_date || '',
                website: entity.website || '',
                domains: Array.isArray(entity.domains) ? entity.domains.join(', ') : '',
                social_media: {
                    linkedin: entity.social_media?.linkedin || '',
                    twitter: entity.social_media?.twitter || '',
                    facebook: entity.social_media?.facebook || '',
                    github: entity.social_media?.github || '',
                    instagram: entity.social_media?.instagram || '',
                },
                tags: Array.isArray(entity.tags) ? entity.tags.join(', ') : '',
                status: entity.status || 'active',
                priority: entity.priority || 'medium',
            });
        }
    }, [entity, isEdit]);

    // Create entity mutation
    const createMutation = useMutation({
        mutationFn: entitiesService.createEntity,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entities'] });
            navigate('/entities');
        },
        onError: (error: Error) => {
            console.error('Create error:', error);
            alert(`Error creating entity: ${error.message || 'Unknown error'}`);
        },
    });

    // Update entity mutation
    const updateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: Partial<Entity> }) =>
            entitiesService.updateEntity(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entities'] });
            navigate('/entities');
        },
        onError: (error: any) => {
            console.error('Update error:', error);
            alert(`Error updating entity: ${error.message || 'Unknown error'}`);
        },
    });

    // Handle form field changes
    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
    ) => {
        const { name, value } = e.target;

        if (name.startsWith('social_media.')) {
            const field = name.split('.')[1];
            setFormData(prev => ({
                ...prev,
                social_media: {
                    ...prev.social_media,
                    [field]: value,
                },
            }));
        } else {
            setFormData(prev => ({
                ...prev,
                [name]: value,
            }));
        }
    };

    // Handle form submission
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Prepare data for submission
        const submitData = {
            ...formData,
            aliases: formData.aliases.split(',').map(a => a.trim()).filter(Boolean),
            domains: formData.domains.split(',').map(d => d.trim()).filter(Boolean),
            tags: formData.tags.split(',').map(t => t.trim()).filter(Boolean),
            social_media: Object.fromEntries(
                Object.entries(formData.social_media).filter(([_, v]) => v)
            ),
        };

        try {
            if (isEdit && entity) {
                await updateMutation.mutateAsync({ id: entity.id, data: submitData });
            } else {
                await createMutation.mutateAsync(submitData);
            }
        } catch (error) {
            console.error('Submit error:', error);
        }
    };

    if (loadingTypes) {
        return <div className="loading">Loading form...</div>;
    }

    return (
        <div className="entity-form-container">
            <h2>{isEdit ? 'Edit Entity' : 'Create New Entity'}</h2>

            <form onSubmit={handleSubmit} className="entity-form">
                {/* Basic Information */}
                <div className="form-section">
                    <h3>Basic Information</h3>

                    <div className="form-group">
                        <label htmlFor="name">Name *</label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="entity_type_id">Entity Type *</label>
                        <select
                            id="entity_type_id"
                            name="entity_type_id"
                            value={formData.entity_type_id}
                            onChange={handleChange}
                            required
                        >
                            <option value="">Select Type</option>
                            {entityTypes.map((type: EntityType) => (
                                <option key={type.id} value={type.id}>
                                    {type.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="aliases">Aliases (comma-separated)</label>
                        <input
                            type="text"
                            id="aliases"
                            name="aliases"
                            value={formData.aliases}
                            onChange={handleChange}
                            placeholder="alias1, alias2, alias3"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="description">Description</label>
                        <textarea
                            id="description"
                            name="description"
                            value={formData.description}
                            onChange={handleChange}
                            rows={4}
                        />
                    </div>
                </div>

                {/* Company Details */}
                <div className="form-section">
                    <h3>Company Details</h3>

                    <div className="form-group">
                        <label htmlFor="industry">Industry</label>
                        <input
                            type="text"
                            id="industry"
                            name="industry"
                            value={formData.industry}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="location">Location</label>
                        <input
                            type="text"
                            id="location"
                            name="location"
                            value={formData.location}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="founded_date">Founded Date</label>
                        <input
                            type="date"
                            id="founded_date"
                            name="founded_date"
                            value={formData.founded_date}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="website">Website</label>
                        <input
                            type="url"
                            id="website"
                            name="website"
                            value={formData.website}
                            onChange={handleChange}
                            placeholder="https://example.com"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="domains">Domains (comma-separated)</label>
                        <input
                            type="text"
                            id="domains"
                            name="domains"
                            value={formData.domains}
                            onChange={handleChange}
                            placeholder="example.com, sub.example.com"
                        />
                    </div>
                </div>

                {/* Social Media */}
                <div className="form-section">
                    <h3>Social Media</h3>

                    <div className="form-group">
                        <label htmlFor="social_media.linkedin">LinkedIn</label>
                        <input
                            type="url"
                            id="social_media.linkedin"
                            name="social_media.linkedin"
                            value={formData.social_media.linkedin}
                            onChange={handleChange}
                            placeholder="https://linkedin.com/company/..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="social_media.twitter">Twitter</label>
                        <input
                            type="url"
                            id="social_media.twitter"
                            name="social_media.twitter"
                            value={formData.social_media.twitter}
                            onChange={handleChange}
                            placeholder="https://twitter.com/..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="social_media.facebook">Facebook</label>
                        <input
                            type="url"
                            id="social_media.facebook"
                            name="social_media.facebook"
                            value={formData.social_media.facebook}
                            onChange={handleChange}
                            placeholder="https://facebook.com/..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="social_media.github">GitHub</label>
                        <input
                            type="url"
                            id="social_media.github"
                            name="social_media.github"
                            value={formData.social_media.github}
                            onChange={handleChange}
                            placeholder="https://github.com/..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="social_media.instagram">Instagram</label>
                        <input
                            type="url"
                            id="social_media.instagram"
                            name="social_media.instagram"
                            value={formData.social_media.instagram}
                            onChange={handleChange}
                            placeholder="https://instagram.com/..."
                        />
                    </div>
                </div>

                {/* Additional Information */}
                <div className="form-section">
                    <h3>Additional Information</h3>

                    <div className="form-group">
                        <label htmlFor="tags">Tags (comma-separated)</label>
                        <input
                            type="text"
                            id="tags"
                            name="tags"
                            value={formData.tags}
                            onChange={handleChange}
                            placeholder="tag1, tag2, tag3"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="status">Status</label>
                        <select
                            id="status"
                            name="status"
                            value={formData.status}
                            onChange={handleChange}
                        >
                            <option value="active">Active</option>
                            <option value="completed">Completed</option>
                            <option value="on_hold">On Hold</option>
                            <option value="archived">Archived</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="priority">Priority</label>
                        <select
                            id="priority"
                            name="priority"
                            value={formData.priority}
                            onChange={handleChange}
                        >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="critical">Critical</option>
                        </select>
                    </div>
                </div>

                {/* Form Actions */}
                <div className="form-actions">
                    <button
                        type="button"
                        onClick={() => navigate('/entities')}
                        className="btn btn-secondary"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={createMutation.isPending || updateMutation.isPending}
                    >
                        {isEdit ? 'Update' : 'Create'} Entity
                    </button>
                </div>
            </form>
        </div>
    );
};

export default EntityForm;
