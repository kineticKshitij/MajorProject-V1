import React, { useState, useEffect } from 'react'; import React, { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom'; import { useNavigate } from 'react-router-dom';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'; import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

import { entitiesService } from '../services/entitiesService'; import { entitiesService } from '../services/entitiesService';

import type { Entity } from '../types'; import type { Entity } from '../types';t React, { useState, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';

interface EntityFormProps {import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

entity ?: Entity; import { entitiesService } from '../services/entitiesService';

isEdit ?: boolean; import type { Entity, EntityType } from '../types';

}

interface EntityFormProps {

interface FormData {
    entity?: Entity;

    name: string; isEdit?: boolean;

    entity_type: number | '';
}

aliases: string;

description: string; interface FormData {

    industry: string; name: string;

    location: string; entity_type: number | '';

    founded_date: string; aliases: string;

    website: string; description: string;

    domains: string; industry: string;

    social_media: {
        location: string;

        linkedin?: string; founded_date: string;

        twitter?: string; website: string;

        facebook?: string; domains: string;

        github?: string; social_media: {

            instagram?: string; linkedin?: string;

        }; twitter?: string;

        tags: string; facebook?: string;

        status: 'active' | 'completed' | 'on_hold' | 'archived'; github?: string;

        priority: 'low' | 'medium' | 'high' | 'critical'; instagram?: string;

    }
};

tags: string;

const EntityForm: React.FC<EntityFormProps> = ({ entity, isEdit = false }) => {
    status: 'active' | 'completed' | 'on_hold' | 'archived';

    const navigate = useNavigate(); priority: 'low' | 'medium' | 'high' | 'critical';

    const queryClient = useQueryClient();
}



// Fetch entity types for dropdownconst EntityForm: React.FC<EntityFormProps> = ({ entity, isEdit = false }) => {

const { data: entityTypes = [], isLoading: loadingTypes } = useQuery({
    const navigate = useNavigate();

    queryKey: ['entity-types'], const queryClient = useQueryClient();

    queryFn: entitiesService.getEntityTypes,

});    // Fetch entity types for dropdown

const { data: entityTypes = [], isLoading: loadingTypes } = useQuery({

    // Initialize form data        queryKey: ['entity-types'],

    const [formData, setFormData] = useState<FormData>({
        queryFn: entitiesService.getEntityTypes,

        name: '',
    });

    entity_type: '',

    aliases: '',    // Initialize form data

    description: '', const [formData, setFormData] = useState<FormData>({

        industry: '', name: '',

        location: '', entity_type: '',

        founded_date: '', aliases: '',

        website: '', description: '',

        domains: '', industry: '',

        social_media: {}, location: '',

        tags: '', founded_date: '',

        status: 'active', website: '',

        priority: 'medium', domains: '',

    }); social_media: {},

    tags: '',

    const [errors, setErrors] = useState<Record<string, string>>({}); status: 'active',

    priority: 'medium',

    // Populate form when editing    });

    useEffect(() => {

    if (entity && isEdit) {
        const [errors, setErrors] = useState<Record<string, string>>({});

        setFormData({

            name: entity.name || '',    // Populate form when editing

            entity_type: entity.entity_type || '', useEffect(() => {

                aliases: Array.isArray(entity.aliases) ? entity.aliases.join(', ') : '', if(entity && isEdit) {

            description: entity.description || '', setFormData({

                industry: entity.industry || '', name: entity.name || '',

                location: entity.location || '', entity_type: entity.entity_type || '',

                founded_date: entity.founded_date || '', aliases: Array.isArray(entity.aliases) ? entity.aliases.join(', ') : '',

                website: entity.website || '', description: entity.description || '',

                domains: Array.isArray(entity.domains) ? entity.domains.join(', ') : '', industry: entity.industry || '',

                social_media: entity.social_media || {}, location: entity.location || '',

                tags: Array.isArray(entity.tags)                 founded_date: entity.founded_date || '',

                    ?entity.tags.join(', ')                 website: entity.website || '',

                    : typeof entity.tags === 'string'                 domains: Array.isArray(entity.domains) ? entity.domains.join(', ') : '',

                    ?entity.tags                 social_media: entity.social_media || {},

                    : '', tags: Array.isArray(entity.tags) 

                status: entity.status || 'active',                    ?entity.tags.join(', ') 

                priority: entity.priority || 'medium',                    : typeof entity.tags === 'string'

            });                    ?entity.tags

        }                    : '',

    }, [entity, isEdit]); status: entity.status || 'active',

        priority: entity.priority || 'medium',

    // Create/Update mutation            });

    const mutation = useMutation({}

        mutationFn: (data: Partial<Entity>) => { }, [entity, isEdit]);

    if (isEdit && entity) {

        return entitiesService.updateEntity(entity.id, data);    // Create/Update mutation

    } const mutation = useMutation({

        return entitiesService.createEntity(data); mutationFn: (data: Partial<Entity>) => {

        }, if(isEdit && entity) {

            onSuccess: (data) => {
                return entitiesService.updateEntity(entity.id, data);

                queryClient.invalidateQueries({ queryKey: ['entities'] });
            }

    queryClient.invalidateQueries({ queryKey: ['entity', data.id] }); return entitiesService.createEntity(data);

    navigate(`/entities/${data.id}`);
},

        }, onSuccess: (data) => {

    onError: (error: any) => {
        queryClient.invalidateQueries({ queryKey: ['entities'] });

        console.error('Failed to save entity:', error); queryClient.invalidateQueries({ queryKey: ['entity', data.id] });

        if (error.response?.data) {
            navigate(`/entities/${data.id}`);

            setErrors(error.response.data);
        },

    }        onError: (error: any) => {

    }, console.error('Failed to save entity:', error);

}); if (error.response?.data) {

    setErrors(error.response.data);

    const handleInputChange = (            }

e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>        },

    ) => { });

const { name, value } = e.target;

setFormData((prev) => ({ ...prev, [name]: value })); const handleInputChange = (

        // Clear error when user starts typing        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>

        if (errors[name]) {    ) => {

    setErrors((prev) => ({ ...prev, [name]: '' })); const { name, value } = e.target;

} setFormData((prev) => ({ ...prev, [name]: value }));

};        // Clear error when user starts typing

if (errors[name]) {

    const handleSocialMediaChange = (platform: string, value: string) => {
        setErrors((prev) => ({ ...prev, [name]: '' }));

        setFormData((prev) => ({}

            ...prev,    };

    social_media: {

                ...prev.social_media,    const handleSocialMediaChange = (platform: string, value: string) => {

            [platform]: value, setFormData((prev) => ({

            },            ...prev,

        })); social_media: {

        };                ...prev.social_media,

            [platform]: value,

    const validateForm = (): boolean => { },

        const newErrors: Record<string, string> = {};
    }));

};

if (!formData.name.trim()) {

    newErrors.name = 'Name is required'; const validateForm = (): boolean => {

    }        const newErrors: Record<string, string> = {};



    if (!formData.entity_type) {
        if (!formData.name.trim()) {

            newErrors.entity_type = 'Entity type is required'; newErrors.name = 'Name is required';

        }
    }



    if (formData.website && !isValidUrl(formData.website)) {
        if (!formData.entity_type) {

            newErrors.website = 'Invalid URL format'; newErrors.entity_type = 'Entity type is required';

        }
    }



    setErrors(newErrors); if (formData.website && !isValidUrl(formData.website)) {

        return Object.keys(newErrors).length === 0; newErrors.website = 'Invalid URL format';

    };
}



const isValidUrl = (url: string): boolean => {
    setErrors(newErrors);

    try {
        return Object.keys(newErrors).length === 0;

        new URL(url);
    };

    return true;

} catch {
    const isValidUrl = (url: string): boolean => {

        return false; try {

        }            new URL(url);

    }; return true;

} catch {

    const handleSubmit = (e: React.FormEvent) => {
        return false;

        e.preventDefault();
    }

};

if (!validateForm()) {

    return; const handleSubmit = (e: React.FormEvent) => {

    }        e.preventDefault();



    // Prepare data for API        if (!validateForm()) {

    const submitData: Partial<Entity> = {
        return;

        name: formData.name.trim(),
    }

    entity_type: Number(formData.entity_type),

        description: formData.description.trim() || undefined,        // Prepare data for API

            industry: formData.industry.trim() || undefined,        const submitData: Partial<Entity> = {

                location: formData.location.trim() || undefined, name: formData.name.trim(),

                founded_date: formData.founded_date || undefined, entity_type: Number(formData.entity_type),

                website: formData.website.trim() || undefined, description: formData.description.trim() || undefined,

                status: formData.status, industry: formData.industry.trim() || undefined,

                priority: formData.priority, location: formData.location.trim() || undefined,

            }; founded_date: formData.founded_date || undefined,

                website: formData.website.trim() || undefined,

        // Parse arrays            status: formData.status,

        if (formData.aliases.trim()) {
        priority: formData.priority,

            submitData.aliases = formData.aliases
    };

                .split(',')

        .map((a) => a.trim())        // Parse arrays

        .filter(Boolean); if (formData.aliases.trim()) {

        } submitData.aliases = formData.aliases

            .split(',')

    if (formData.domains.trim()) {                .map((a) => a.trim())

        submitData.domains = formData.domains.filter(Boolean);

                .split(',')
    }

                .map((d) => d.trim())

        .filter(Boolean); if (formData.domains.trim()) {

        } submitData.domains = formData.domains

            .split(',')

    if (formData.tags.trim()) {                .map((d) => d.trim())

        submitData.tags = formData.tags.filter(Boolean);

                .split(',')
    }

                .map((t) => t.trim())

        .filter(Boolean); if (formData.tags.trim()) {

        } submitData.tags = formData.tags

            .split(',')

    // Clean social media (remove empty values)                .map((t) => t.trim())

    const cleanedSocialMedia = Object.entries(formData.social_media).filter(Boolean);

            .filter(([_, value]) => value && value.trim())
}

            .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});

// Clean social media (remove empty values)

if (Object.keys(cleanedSocialMedia).length > 0) {
    const cleanedSocialMedia = Object.entries(formData.social_media)

    submitData.social_media = cleanedSocialMedia;            .filter(([_, value]) => value && value.trim())

}            .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});



mutation.mutate(submitData); if (Object.keys(cleanedSocialMedia).length > 0) {

}; submitData.social_media = cleanedSocialMedia;

        }

if (loadingTypes) {

    return (mutation.mutate(submitData);

    <div className="flex items-center justify-center min-h-screen">    };

        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>

    </div>    if (loadingTypes) {

        ); return (

    }            <div className="flex items-center justify-center min-h-screen">

                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>

    return (            </div>

        <div className="max-w-4xl mx-auto px-4 py-8">        );

            {/* Header */}    }

            <div className="mb-8">

                <button    return (

                    onClick={() => navigate(-1)}        <div className="max-w-4xl mx-auto px-4 py-8">

                    className="text-gray-600 hover:text-gray-900 mb-4 flex items-center"            {/* Header */}

                >            <div className="mb-8">

                    <span className="mr-2">←</span> Back                <button

                </button>                    onClick={() => navigate(-1)}

                <h1 className="text-3xl font-bold text-gray-900">                    className="text-gray-600 hover:text-gray-900 mb-4 flex items-center"

                    {isEdit ? 'Edit Entity' : 'Create New Entity'}                >

                </h1>                    <span className="mr-2">←</span> Back

                <p className="text-gray-600 mt-2">                </button>

                    {isEdit                <h1 className="text-3xl font-bold text-gray-900">

                        ? 'Update entity information'                    {isEdit ? 'Edit Entity' : 'Create New Entity'}

                        : 'Add a new entity to research'}                </h1>

                </p>                <p className="text-gray-600 mt-2">

            </div>                    {
        isEdit

            ? 'Update entity information'

            {/* Form */ }                        : 'Add a new entity to research'
    }

    <form onSubmit={handleSubmit} className="space-y-8 bg-white rounded-lg shadow-lg p-6">                </p>

    {/* Basic Information */ }            </div >

        <div className="border-b pb-6">

            <h2 className="text-xl font-semibold text-gray-900 mb-4">            {/* Form */}

                Basic Information            <form onSubmit={handleSubmit} className="space-y-8 bg-white rounded-lg shadow-lg p-6">

            </h2>                {/* Basic Information */}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">                <div className="border-b pb-6">

                {/* Name */}                    <h2 className="text-xl font-semibold text-gray-900 mb-4">

                    <div className="md:col-span-2">                        Basic Information

                        <label className="block text-sm font-medium text-gray-700 mb-2">                    </h2>

                        Name <span className="text-red-500">*</span>                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                        </label>                        {/* Name */}

                        <input                        <div className="md:col-span-2">

                            type="text"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                name="name"                                Name <span className="text-red-500">*</span>

                                value={formData.name}                            </label>

                            onChange={handleInputChange}                            <input

                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${type = "text"

                                    errors.name ? 'border-red-500' : 'border-gray-300'                                name="name"

                                }`}                                value={formData.name}

                            placeholder="e.g., Acme Corporation"                                onChange={handleInputChange}

                            />                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${{
                                    errors.name && (errors.name ? 'border-red-500' : 'border-gray-300'

                                        < p className="text-red-500 text-sm mt-1" > { errors.name }</p>                                }`}

                            )}                                placeholder="e.g., Acme Corporation"

                    </div>                            />

                    {errors.name && (

                        {/* Entity Type */ } < p className="text-red-500 text-sm mt-1">{errors.name}</p>

                <div>                            )}

                    <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

                Entity Type <span className="text-red-500">*</span>

            </label>                        {/* Entity Type */}

                <select                        <div>

                    name="entity_type"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                    value={formData.entity_type}                                Entity Type <span className="text-red-500">*</span>

                    onChange={handleInputChange}                            </label>

                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${<select

                    errors.entity_type ? 'border-red-500' : 'border-gray-300'                                name="entity_type"

                                }`}                                value={formData.entity_type}

                            >                                onChange={handleInputChange}

                <option value="">Select type...</option>                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${{
                        entityTypes.map((type) => (errors.entity_type ? 'border-red-500' : 'border-gray-300'

                            < option key = { type.id } value = { type.id } >                                }`}

                                        {type.icon} {type.name}                            >

                                    </option>                                <option value="">Select type...</option>

                                ))}                                {entityTypes.map((type) => (

                            </select>                                    <option key={type.id} value={type.id}>

                            {errors.entity_type && (                                        {type.icon} {type.name}

                                <p className="text-red-500 text-sm mt-1">{errors.entity_type}</p>                                    </option>

                            )}                                ))}

                        </div>                            </select>

                            {errors.entity_type && (

                        {/* Status */}                                <p className="text-red-500 text-sm mt-1">{errors.entity_type}</p>

                        <div>                            )}

                            <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

                                Status

                            </label>                        {/* Status */}

                            <select                        <div>

                                name="status"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                value={formData.status}                                Status

                                onChange={handleInputChange}                            </label>

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                            <select

                            >                                name="status"

                                <option value="active">Active</option>                                value={formData.status}

                                <option value="completed">Completed</option>                                onChange={handleInputChange}

                                <option value="on_hold">On Hold</option>                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                                <option value="archived">Archived</option>                            >

                            </select>                                <option value="active">Active</option>

                        </div>                                <option value="completed">Completed</option>

                                <option value="on_hold">On Hold</option>

                        {/* Priority */}                                <option value="archived">Archived</option>

                        <div>                            </select>

                            <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

                                Priority

                            </label>                        {/* Priority */}

                            <select                        <div>

                                name="priority"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                value={formData.priority}                                Priority

                                onChange={handleInputChange}                            </label>

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                            <select

                            >                                name="priority"

                                <option value="low">↓ Low</option>                                value={formData.priority}

                                <option value="medium">→ Medium</option>                                onChange={handleInputChange}

                                <option value="high">↑ High</option>                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                                <option value="critical">🔴 Critical</option>                            >

                            </select>                                <option value="low">↓ Low</option>

                        </div>                                <option value="medium">→ Medium</option>

                                <option value="high">↑ High</option>

                        {/* Industry */}                                <option value="critical">🔴 Critical</option>

                        <div>                            </select>

                            <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

                                Industry

                            </label>                        {/* Industry */}

                            <input                        <div>

                                type="text"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                name="industry"                                Industry

                                value={formData.industry}                            </label>

                                onChange={handleInputChange}                            <input

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                type="text"

                                placeholder="e.g., Technology, Healthcare"                                name="industry"

                            />                                value={formData.industry}

                        </div>                                onChange={handleInputChange}

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                        {/* Aliases */}                                placeholder="e.g., Technology, Healthcare"

                        <div className="md:col-span-2">                            />

                            <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

                                Aliases

                            </label>                        {/* Aliases */}

                            <input                        <div className="md:col-span-2">

                                type="text"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                name="aliases"                                Aliases

                                value={formData.aliases}                            </label>

                                onChange={handleInputChange}                            <input

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                type="text"

                                placeholder="Comma-separated, e.g., Acme Corp, Acme Inc"                                name="aliases"

                            />                                value={formData.aliases}

                            <p className="text-gray-500 text-sm mt-1">                                onChange={handleInputChange}

                                Alternative names, separated by commas                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                            </p>                                placeholder="Comma-separated, e.g., Acme Corp, Acme Inc"

                        </div>                            />

                            <p className="text-gray-500 text-sm mt-1">

                        {/* Description */}                                Alternative names, separated by commas

                        <div className="md:col-span-2">                            </p>

                            <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

                                Description

                            </label>                        {/* Description */}

                            <textarea                        <div className="md:col-span-2">

                                name="description"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                value={formData.description}                                Description

                                onChange={handleInputChange}                            </label>

                                rows={4}                            <textarea

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                name="description"

                                placeholder="Brief description of the entity..."                                value={formData.description}

                            />                                onChange={handleInputChange}

                        </div>                                rows={4}

                    </div>                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                </div>                                placeholder="Brief description of the entity..."

                            />

                {/* Location & Dates */}                        </div>

                <div className="border-b pb-6">                    </div>

                    <h2 className="text-xl font-semibold text-gray-900 mb-4">                </div>

                        Location & Timeline

                    </h2>                {/* Location & Dates */}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">                <div className="border-b pb-6">

                        {/* Location */}                    <h2 className="text-xl font-semibold text-gray-900 mb-4">

                        <div>                        Location & Timeline

                            <label className="block text-sm font-medium text-gray-700 mb-2">                    </h2>

                                Location                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                            </label>                        {/* Location */}

                            <input                        <div>

                                type="text"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                name="location"                                Location

                                value={formData.location}                            </label>

                                onChange={handleInputChange}                            <input

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                type="text"

                                placeholder="e.g., San Francisco, CA"                                name="location"

                            />                                value={formData.location}

                        </div>                                onChange={handleInputChange}

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                        {/* Founded Date */}                                placeholder="e.g., San Francisco, CA"

                        <div>                            />

                            <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

                                Founded Date

                            </label>                        {/* Founded Date */}

                            <input                        <div>

                                type="date"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                name="founded_date"                                Founded Date

                                value={formData.founded_date}                            </label>

                                onChange={handleInputChange}                            <input

                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                type="date"

                            />                                name="founded_date"

                        </div>                                value={formData.founded_date}

                    </div>                                onChange={handleInputChange}

                </div>                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                            />

                {/* Online Presence */}                        </div>

                <div className="border-b pb-6">                    </div>

                    <h2 className="text-xl font-semibold text-gray-900 mb-4">                </div>

                        Online Presence

                    </h2>                {/* Online Presence */}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">                <div className="border-b pb-6">

                        {/* Website */}                    <h2 className="text-xl font-semibold text-gray-900 mb-4">

                        <div className="md:col-span-2">                        Online Presence

                            <label className="block text-sm font-medium text-gray-700 mb-2">                    </h2>

                                Website                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                            </label>                        {/* Website */}

                            <input                        <div className="md:col-span-2">

                                type="url"                            <label className="block text-sm font-medium text-gray-700 mb-2">

                                name="website"                                Website

                                value={formData.website}                            </label>

                                onChange={handleInputChange}                            <input

                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${type = "url"

                                    errors.website ? 'border-red-500' : 'border-gray-300'                                name="website"

                                }`}                                value={formData.website}

                placeholder="https://example.com"                                onChange={handleInputChange}

                            />                                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${{
                        errors.website && (errors.website ? 'border-red-500' : 'border-gray-300'

                            < p className="text-red-500 text-sm mt-1" > { errors.website }</p>                                }`}

                            )}                                placeholder="https://example.com"

        </div> />

    {
        errors.website && (

            {/* Domains */ } < p className="text-red-500 text-sm mt-1" > { errors.website }</p>

        <div className="md:col-span-2">                            )}

            <label className="block text-sm font-medium text-gray-700 mb-2">                        </div>

    Domains

                            </label > {/* Domains */ }

        < input < div className = "md:col-span-2" >

            type="text" < label className = "block text-sm font-medium text-gray-700 mb-2" >

                name="domains"                                Domains

    value = { formData.domains }                            </label >

        onChange={ handleInputChange } <input

            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" type="text"

            placeholder="Comma-separated, e.g., example.com, example.org" name="domains"

        />                                value = { formData.domains }

            < p className = "text-gray-500 text-sm mt-1" > onChange={ handleInputChange }

                                All domains associated with this entity                                className = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                            </p > placeholder="Comma-separated, e.g., example.com, example.org"

                        </div >                            />

        < p className = "text-gray-500 text-sm mt-1" >

            {/* Social Media */ }                                All domains associated with this entity

                < div className = "md:col-span-2" >                            </p >

                    <label className="block text-sm font-medium text-gray-700 mb-3">                        </div>

                                Social Media

                            </label > {/* Social Media */ }

        < div className = "space-y-3" > <div className="md:col-span-2">

            {/* LinkedIn */}                            <label className="block text-sm font-medium text-gray-700 mb-3">

                <div className="flex items-center gap-3">                                Social Media

                    <span className="w-24 text-sm text-gray-600">LinkedIn:</span>                            </label>

            <input                            <div className="space-y-3">

                type="url"                                {/* LinkedIn */}

                value={formData.social_media.linkedin || ''}                                <div className="flex items-center gap-3">

                    onChange={(e) => <span className="w-24 text-sm text-gray-600">LinkedIn:</span>

                                            handleSocialMediaChange('linkedin', e.target.value)                                    <input

                                        }                                        type="url"

                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                        value={formData.social_media.linkedin || ''}

                    placeholder="https://linkedin.com/company/..."                                        onChange={(e) =>

                                    />                                            handleSocialMediaChange('linkedin', e.target.value)

                                </div>                                        }

                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                {/* Twitter */}                                        placeholder="https://linkedin.com/company/..."

                <div className="flex items-center gap-3">                                    />

                    <span className="w-24 text-sm text-gray-600">Twitter:</span>                                </div>

                <input

                    type="url"                                {/* Twitter */}

                    value={formData.social_media.twitter || ''}                                <div className="flex items-center gap-3">

                    onChange={(e) => <span className="w-24 text-sm text-gray-600">Twitter:</span>

                                            handleSocialMediaChange('twitter', e.target.value)                                    <input

                                        }                                        type="url"

                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                        value={formData.social_media.twitter || ''}

                    placeholder="https://twitter.com/..."                                        onChange={(e) =>

                                    />                                            handleSocialMediaChange('twitter', e.target.value)

                                </div>                                        }

                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                {/* Facebook */}                                        placeholder="https://twitter.com/..."

                <div className="flex items-center gap-3">                                    />

                    <span className="w-24 text-sm text-gray-600">Facebook:</span>                                </div>

                <input

                    type="url"                                {/* Facebook */}

                    value={formData.social_media.facebook || ''}                                <div className="flex items-center gap-3">

                    onChange={(e) => <span className="w-24 text-sm text-gray-600">Facebook:</span>

                                            handleSocialMediaChange('facebook', e.target.value)                                    <input

                                        }                                        type="url"

                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                        value={formData.social_media.facebook || ''}

                    placeholder="https://facebook.com/..."                                        onChange={(e) =>

                                    />                                            handleSocialMediaChange('facebook', e.target.value)

                                </div>                                        }

                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                {/* GitHub */}                                        placeholder="https://facebook.com/..."

                <div className="flex items-center gap-3">                                    />

                    <span className="w-24 text-sm text-gray-600">GitHub:</span>                                </div>

                <input

                    type="url"                                {/* GitHub */}

                    value={formData.social_media.github || ''}                                <div className="flex items-center gap-3">

                    onChange={(e) => <span className="w-24 text-sm text-gray-600">GitHub:</span>

                                            handleSocialMediaChange('github', e.target.value)                                    <input

                                        }                                        type="url"

                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                        value={formData.social_media.github || ''}

                    placeholder="https://github.com/..."                                        onChange={(e) =>

                                    />                                            handleSocialMediaChange('github', e.target.value)

                                </div>                                        }

                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                {/* Instagram */}                                        placeholder="https://github.com/..."

                <div className="flex items-center gap-3">                                    />

                    <span className="w-24 text-sm text-gray-600">Instagram:</span>                                </div>

                <input

                    type="url"                                {/* Instagram */}

                    value={formData.social_media.instagram || ''}                                <div className="flex items-center gap-3">

                    onChange={(e) => <span className="w-24 text-sm text-gray-600">Instagram:</span>

                                            handleSocialMediaChange('instagram', e.target.value)                                    <input

                                        }                                        type="url"

                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"                                        value={formData.social_media.instagram || ''}

                    placeholder="https://instagram.com/..."                                        onChange={(e) =>

                                    />                                            handleSocialMediaChange('instagram', e.target.value)

                                </div>                                        }

        </div>                                        className = "flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

                        </div > placeholder="https://instagram.com/..."

                    </div >                                    />

                </div >                                </div >

                            </div >

        {/* Tags */ }                        </div >

                <div>                    </div>

                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Tags</h2>                </div >

        <div>

            <label className="block text-sm font-medium text-gray-700 mb-2">                {/* Tags */}

                Tags                <div>

            </label>                    <h2 className="text-xl font-semibold text-gray-900 mb-4">Tags</h2>

            <input                    <div>

                type="text"                        <label className="block text-sm font-medium text-gray-700 mb-2">

                name="tags"                            Tags

                value={formData.tags}                        </label>

            onChange={handleInputChange}                        <input

                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" type="text"

                placeholder="Comma-separated, e.g., tech, startup, ai" name="tags"

            />                            value={formData.tags}

            <p className="text-gray-500 text-sm mt-1">                            onChange={handleInputChange}

                Keywords for categorization and search                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

            </p>                            placeholder="Comma-separated, e.g., tech, startup, ai"

        </div> />

                </div >                        <p className="text-gray-500 text-sm mt-1">

                            Keywords for categorization and search

                {/* Form Actions */}                        </p>

                <div className="flex items-center justify-between pt-6 border-t">                    </div>

                    <button                </div>

                        type="button"

                        onClick={() => navigate(-1)}                {/* Form Actions */}

                        className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"                <div className="flex items-center justify-between pt-6 border-t">

                        disabled={mutation.isPending}                    <button

                    >                        type="button"

                        Cancel                        onClick={() => navigate(-1)}

                    </button>                        className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"

                        disabled={mutation.isPending}

                    <button                    >

                        type="submit"                        Cancel

                        disabled={mutation.isPending}                    </button>

                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"

                    >                    <button

                        {mutation.isPending ? (                        type="submit"

                            <>                        disabled={mutation.isPending}

                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"

                                <span>{isEdit ? 'Updating...' : 'Creating...'}</span>                    >

                            </>                        {
        mutation.isPending ? (

        ): (<>

                            <span>{ isEdit? 'Update Entity': 'Create Entity' }</span > <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>

                        )
    } <span>{isEdit ? 'Updating...' : 'Creating...'}</span>

                    </button >                            </>

                </div >                        ) : (

        <span>{isEdit ? 'Update Entity' : 'Create Entity'}</span>

                {/* Error Message */ }                        )
}

{
    mutation.isError && (                    </button >

                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">                </div>

                        <p className="text-red-800 text-sm">

                            Failed to {isEdit ? 'update' : 'create'} entity. Please check the form and try again.                {/* Error Message */}

                        </p>                {
        mutation.isError && (

                    </div > <div className="bg-red-50 border border-red-200 rounded-lg p-4">

                )}                        <p className="text-red-800 text-sm">

            </form>                            Failed to {isEdit ? 'update' : 'create'} entity. Please check the form and try again.

        </div>                        </p >

    );                    </div >

};                )
}

            </form >

export default EntityForm;        </div >

    );
};

export default EntityForm;
