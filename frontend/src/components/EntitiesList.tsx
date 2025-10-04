import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';
import type { Entity } from '../types';

const EntitiesList = () => {
    const navigate = useNavigate();
    const [filters, setFilters] = useState({
        search: '',
        entity_type: undefined as number | undefined,
        status: '',
        priority: '',
        page: 1,
    });

    // Fetch entity types for filter
    const { data: entityTypesResponse } = useQuery({
        queryKey: ['entity-types'],
        queryFn: () => entitiesService.getEntityTypes(),
    });

    // Handle both array and paginated response
    const entityTypes = Array.isArray(entityTypesResponse)
        ? entityTypesResponse
        : (entityTypesResponse as any)?.results || [];

    // Fetch entities
    const { data: entitiesData, isLoading, refetch } = useQuery({
        queryKey: ['entities', filters],
        queryFn: () => entitiesService.getEntities(filters),
    });

    // Fetch statistics
    const { data: stats } = useQuery({
        queryKey: ['entity-statistics'],
        queryFn: () => entitiesService.getEntityStatistics(),
    });

    const handleFilterChange = (key: string, value: string | number) => {
        setFilters(prev => ({
            ...prev,
            [key]: value === '' ? undefined : (key === 'entity_type' ? Number(value) : value),
            page: 1
        }));
    };

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        refetch();
    };

    const getStatusColor = (status: string) => {
        const colors: Record<string, string> = {
            active: 'bg-green-100 text-green-800',
            completed: 'bg-blue-100 text-blue-800',
            on_hold: 'bg-yellow-100 text-yellow-800',
            archived: 'bg-gray-100 text-gray-800',
        };
        return colors[status] || 'bg-gray-100 text-gray-800';
    };

    const getPriorityColor = (priority: string) => {
        const colors: Record<string, string> = {
            low: 'text-gray-600',
            medium: 'text-blue-600',
            high: 'text-orange-600',
            critical: 'text-red-600',
        };
        return colors[priority] || 'text-gray-600';
    };

    const getPriorityIcon = (priority: string) => {
        const icons: Record<string, string> = {
            low: '↓',
            medium: '→',
            high: '↑',
            critical: '🔴',
        };
        return icons[priority] || '→';
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Entities</h1>
                        <p className="mt-1 text-sm text-gray-500">
                            Manage research targets: companies, persons, organizations, and more
                        </p>
                    </div>
                    <Link
                        to="/entities/new"
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        <svg className="mr-2 -ml-1 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        New Entity
                    </Link>
                </div>
            </div>

            {/* Statistics Cards */}
            {stats && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                </svg>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">Total Entities</p>
                                <p className="text-2xl font-semibold text-gray-900">{stats.total_entities || 0}</p>
                            </div>
                        </div>
                    </div>

                    {stats.status_distribution && Array.isArray(stats.status_distribution) && stats.status_distribution.map((item: any) => (
                        <div key={item.status} className="bg-white rounded-lg shadow p-6">
                            <div className="flex items-center">
                                <div className={`flex-shrink-0 rounded-md p-3 ${item.status === 'active' ? 'bg-green-500' :
                                    item.status === 'completed' ? 'bg-blue-500' :
                                        item.status === 'on_hold' ? 'bg-yellow-500' :
                                            'bg-gray-500'
                                    }`}>
                                    <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                </div>
                                <div className="ml-4">
                                    <p className="text-sm font-medium text-gray-500 capitalize">{item.status.replace('_', ' ')}</p>
                                    <p className="text-2xl font-semibold text-gray-900">{item.count}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Filters */}
            <div className="bg-white rounded-lg shadow mb-6 p-6">
                <form onSubmit={handleSearch} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        {/* Search */}
                        <div className="md:col-span-2">
                            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                                Search
                            </label>
                            <input
                                type="text"
                                id="search"
                                value={filters.search}
                                onChange={(e) => handleFilterChange('search', e.target.value)}
                                placeholder="Search by name, description, industry..."
                                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            />
                        </div>

                        {/* Entity Type */}
                        <div>
                            <label htmlFor="entity_type" className="block text-sm font-medium text-gray-700 mb-1">
                                Entity Type
                            </label>
                            <select
                                id="entity_type"
                                value={filters.entity_type}
                                onChange={(e) => handleFilterChange('entity_type', e.target.value)}
                                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            >
                                <option value="">All Types</option>
                                {entityTypes.map((type: any) => (
                                    <option key={type.id} value={type.id}>{type.display_name || type.name}</option>
                                ))}
                            </select>
                        </div>

                        {/* Status */}
                        <div>
                            <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                                Status
                            </label>
                            <select
                                id="status"
                                value={filters.status}
                                onChange={(e) => handleFilterChange('status', e.target.value)}
                                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            >
                                <option value="">All Status</option>
                                <option value="active">Active</option>
                                <option value="completed">Completed</option>
                                <option value="on_hold">On Hold</option>
                                <option value="archived">Archived</option>
                            </select>
                        </div>
                    </div>

                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                            {/* Priority Filter */}
                            <select
                                value={filters.priority}
                                onChange={(e) => handleFilterChange('priority', e.target.value)}
                                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            >
                                <option value="">All Priorities</option>
                                <option value="low">Low Priority</option>
                                <option value="medium">Medium Priority</option>
                                <option value="high">High Priority</option>
                                <option value="critical">Critical Priority</option>
                            </select>
                        </div>

                        <button
                            type="submit"
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            <svg className="mr-2 -ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                            Search
                        </button>
                    </div>
                </form>
            </div>

            {/* Entities List */}
            {isLoading ? (
                <div className="flex justify-center items-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                </div>
            ) : entitiesData && entitiesData.results.length > 0 ? (
                <>
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <ul className="divide-y divide-gray-200">
                            {entitiesData.results.map((entity: Entity) => (
                                <li key={entity.id}>
                                    <Link
                                        to={`/entities/${entity.id}`}
                                        className="block hover:bg-gray-50 transition duration-150"
                                    >
                                        <div className="px-6 py-4">
                                            <div className="flex items-center justify-between">
                                                <div className="flex-1 min-w-0">
                                                    <div className="flex items-center space-x-3">
                                                        {/* Entity Icon */}
                                                        <div
                                                            className="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold text-lg"
                                                            style={{ backgroundColor: entity.entity_type_data?.color || '#6366f1' }}
                                                        >
                                                            {entity.entity_type_data?.icon || entity.name.charAt(0).toUpperCase()}
                                                        </div>

                                                        <div className="flex-1 min-w-0">
                                                            <div className="flex items-center space-x-2">
                                                                <h3 className="text-lg font-medium text-gray-900 truncate">
                                                                    {entity.name}
                                                                </h3>
                                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(entity.status)}`}>
                                                                    {entity.status.replace('_', ' ')}
                                                                </span>
                                                                <span className={`inline-flex items-center text-sm font-medium ${getPriorityColor(entity.priority)}`}>
                                                                    {getPriorityIcon(entity.priority)} {entity.priority}
                                                                </span>
                                                            </div>

                                                            <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                                                                <span className="flex items-center">
                                                                    <span className="mr-1">📁</span>
                                                                    {entity.entity_type_data?.display_name || entity.entity_type_name}
                                                                </span>
                                                                {entity.industry && (
                                                                    <span className="flex items-center">
                                                                        <span className="mr-1">🏢</span>
                                                                        {entity.industry}
                                                                    </span>
                                                                )}
                                                                {entity.location && (
                                                                    <span className="flex items-center">
                                                                        <span className="mr-1">📍</span>
                                                                        {entity.location}
                                                                    </span>
                                                                )}
                                                            </div>

                                                            {entity.description && (
                                                                <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                                                                    {entity.description}
                                                                </p>
                                                            )}

                                                            {entity.tags && Array.isArray(entity.tags) && entity.tags.length > 0 && (
                                                                <div className="mt-2 flex flex-wrap gap-1">
                                                                    {entity.tags.slice(0, 5).map((tag: string, idx: number) => (
                                                                        <span
                                                                            key={idx}
                                                                            className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                                                                        >
                                                                            #{tag}
                                                                        </span>
                                                                    ))}
                                                                    {entity.tags.length > 5 && (
                                                                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                                                                            +{entity.tags.length - 5} more
                                                                        </span>
                                                                    )}
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* Stats */}
                                                <div className="flex items-center space-x-6 ml-4">
                                                    <div className="text-center">
                                                        <div className="text-2xl font-semibold text-gray-900">{entity.search_count || 0}</div>
                                                        <div className="text-xs text-gray-500">Searches</div>
                                                    </div>
                                                    <div className="text-center">
                                                        <div className="text-2xl font-semibold text-gray-900">{entity.results_found || 0}</div>
                                                        <div className="text-xs text-gray-500">Results</div>
                                                    </div>
                                                    <div className="text-right">
                                                        <div className="text-sm text-gray-500">
                                                            Updated {new Date(entity.updated_at).toLocaleDateString()}
                                                        </div>
                                                        {entity.last_researched && (
                                                            <div className="text-xs text-gray-400">
                                                                Last researched {new Date(entity.last_researched).toLocaleDateString()}
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Pagination */}
                    {(entitiesData.previous || entitiesData.next) && (
                        <div className="mt-6 flex items-center justify-between">
                            <button
                                onClick={() => setFilters(prev => ({ ...prev, page: prev.page - 1 }))}
                                disabled={!entitiesData.previous}
                                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Previous
                            </button>
                            <span className="text-sm text-gray-700">
                                Page {filters.page}
                            </span>
                            <button
                                onClick={() => setFilters(prev => ({ ...prev, page: prev.page + 1 }))}
                                disabled={!entitiesData.next}
                                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Next
                            </button>
                        </div>
                    )}
                </>
            ) : (
                <div className="text-center py-12 bg-white rounded-lg shadow">
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No entities found</h3>
                    <p className="mt-1 text-sm text-gray-500">Get started by creating a new entity.</p>
                    <div className="mt-6">
                        <Link
                            to="/entities/new"
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
                        >
                            <svg className="mr-2 -ml-1 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                            </svg>
                            New Entity
                        </Link>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EntitiesList;
