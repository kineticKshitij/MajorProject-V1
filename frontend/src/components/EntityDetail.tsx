import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';
import TemplateIntegration from './TemplateIntegration';
import EnhancedRelationshipGraph from './EnhancedRelationshipGraph';
import InlineAttributeForm from './InlineAttributeForm';
import InlineRelationshipForm from './InlineRelationshipForm';
import type {
    Entity,
    EntityAttribute,
    EntityRelationship,
    EntityNote,
    EntitySearchResult
} from '../types';

type TabType = 'overview' | 'attributes' | 'relationships' | 'notes' | 'templates' | 'graph' | 'results';

const EntityDetail: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [activeTab, setActiveTab] = useState<TabType>('overview');

    // Validate ID early but don't return yet - all hooks must be called first
    const isValidId = !!(id && id !== 'undefined' && id !== 'NaN');

    // Fetch entity details - Use ID as string (UUID)
    const { data: entity, isLoading, error } = useQuery<Entity>({
        queryKey: ['entity', id],
        queryFn: () => entitiesService.getEntity(id!),
        enabled: isValidId,
    });

    // Fetch attributes
    const { data: attributes = [] } = useQuery<EntityAttribute[]>({
        queryKey: ['entity-attributes', id],
        queryFn: () => entitiesService.getEntityAttributes(id!),
        enabled: isValidId && activeTab === 'attributes',
    });

    // Fetch relationships
    const { data: relationshipsData } = useQuery<{ outgoing: EntityRelationship[]; incoming: EntityRelationship[] }>({
        queryKey: ['entity-relationships', id],
        queryFn: () => entitiesService.getEntityRelationships(id!),
        enabled: isValidId && activeTab === 'relationships',
    });

    const relationships = [
        ...(relationshipsData?.outgoing || []),
        ...(relationshipsData?.incoming || [])
    ];

    // Fetch notes
    const { data: notes = [] } = useQuery<EntityNote[]>({
        queryKey: ['entity-notes', id],
        queryFn: () => entitiesService.getEntityNotes(id!),
        enabled: isValidId && activeTab === 'notes',
    });

    // Fetch search results - using search sessions endpoint (for future implementation)
    useQuery({
        queryKey: ['entity-search-sessions', id],
        queryFn: () => entitiesService.getEntitySearchSessions(id!),
        enabled: false, // Disabled until search execution is implemented
    });

    // TODO: Expand search sessions to get actual results
    const results: EntitySearchResult[] = [];
    // In future: Fetch results for each session and combine them
    // For now, showing empty state until search execution is implemented

    // Delete mutation
    const deleteMutation = useMutation({
        mutationFn: () => entitiesService.deleteEntity(Number(id)),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entities'] });
            navigate('/entities');
        },
    });

    // NOW check for invalid ID after all hooks are called
    if (!isValidId) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="bg-white p-8 rounded-lg shadow-md max-w-md text-center">
                    <div className="text-red-600 text-5xl mb-4">⚠️</div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Invalid Entity ID</h2>
                    <p className="text-gray-600 mb-6">
                        The entity ID is missing or invalid. Please navigate to an entity from the entities list.
                    </p>
                    <Link
                        to="/entities"
                        className="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition"
                    >
                        ← Back to Entities List
                    </Link>
                </div>
            </div>
        );
    }

    const handleDelete = () => {
        if (window.confirm(`Are you sure you want to delete "${entity?.name}"?`)) {
            deleteMutation.mutate();
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading entity details...</p>
                </div>
            </div>
        );
    }

    if (error || !entity) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                    <h2 className="text-2xl font-bold text-red-700 mb-2">Entity Not Found</h2>
                    <p className="text-red-600 mb-4">The entity you're looking for doesn't exist or has been deleted.</p>
                    <Link to="/entities" className="text-blue-600 hover:text-blue-800 font-medium">
                        ← Back to Entities List
                    </Link>
                </div>
            </div>
        );
    }

    const tabs = [
        { id: 'overview' as TabType, label: 'Overview', icon: '📋' },
        { id: 'attributes' as TabType, label: 'Attributes', icon: '🏷️', count: attributes.length },
        { id: 'relationships' as TabType, label: 'Relationships', icon: '🔗', count: relationships.length },
        { id: 'notes' as TabType, label: 'Notes', icon: '📝', count: notes.length },
        { id: 'templates' as TabType, label: 'Templates', icon: '🎯' },
        { id: 'graph' as TabType, label: 'Graph', icon: '🕸️' },
        { id: 'results' as TabType, label: 'Search Results', icon: '🔍', count: results.length },
    ];

    const priorityColors = {
        low: 'bg-gray-100 text-gray-700',
        medium: 'bg-blue-100 text-blue-700',
        high: 'bg-orange-100 text-orange-700',
        critical: 'bg-red-100 text-red-700',
    };

    const statusColors = {
        active: 'bg-green-100 text-green-700',
        completed: 'bg-blue-100 text-blue-700',
        on_hold: 'bg-yellow-100 text-yellow-700',
        archived: 'bg-gray-100 text-gray-700',
    };

    const priorityIcons = {
        low: '↓',
        medium: '→',
        high: '↑',
        critical: '🔴',
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header */}
            <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                    <Link to="/entities" className="text-blue-600 hover:text-blue-800 font-medium flex items-center">
                        <span className="mr-2">←</span> Back to Entities
                    </Link>
                    <div className="flex gap-2">
                        <Link
                            to={`/entities/${id}/edit`}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                        >
                            ✏️ Edit
                        </Link>
                        <button
                            onClick={handleDelete}
                            disabled={deleteMutation.isPending}
                            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
                        >
                            🗑️ Delete
                        </button>
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                                <span
                                    className="text-3xl"
                                    style={{ color: entity.entity_type_data?.color || '#3B82F6' }}
                                >
                                    {entity.entity_type_data?.icon || '📌'}
                                </span>
                                <h1 className="text-3xl font-bold text-gray-900">{entity.name}</h1>
                            </div>
                            <div className="flex items-center gap-2 mb-3">
                                <span className={`px-3 py-1 rounded-full text-sm font-medium ${priorityColors[entity.priority]}`}>
                                    {priorityIcons[entity.priority]} {entity.priority.toUpperCase()}
                                </span>
                                <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColors[entity.status]}`}>
                                    {entity.status.replace('_', ' ').toUpperCase()}
                                </span>
                                <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-medium">
                                    {entity.entity_type_data?.display_name || entity.entity_type_name}
                                </span>
                            </div>
                            {entity.description && (
                                <p className="text-gray-600 mb-3">{entity.description}</p>
                            )}
                            <div className="flex flex-wrap gap-2">
                                {(Array.isArray(entity.tags) ? entity.tags : []).map((tag, index) => (
                                    <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm">
                                        #{tag}
                                    </span>
                                ))}
                            </div>
                        </div>
                        <div className="text-right text-sm text-gray-500 ml-4">
                            <div className="mb-2">
                                <span className="font-medium">Searches:</span> {entity.search_count || 0}
                            </div>
                            <div className="mb-2">
                                <span className="font-medium">Results:</span> {entity.results_found || 0}
                            </div>
                            {entity.last_researched && (
                                <div>
                                    <span className="font-medium">Last Researched:</span>
                                    <br />
                                    {new Date(entity.last_researched).toLocaleDateString()}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <div className="border-b border-gray-200">
                    <nav className="flex -mb-px">
                        {tabs.map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors ${activeTab === tab.id
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                            >
                                <span className="mr-2">{tab.icon}</span>
                                {tab.label}
                                {tab.count !== undefined && tab.count > 0 && (
                                    <span className="ml-2 px-2 py-1 bg-gray-200 text-gray-700 rounded-full text-xs">
                                        {tab.count}
                                    </span>
                                )}
                            </button>
                        ))}
                    </nav>
                </div>

                <div className="p-6">
                    {activeTab === 'overview' && <OverviewTab entity={entity} />}
                    {activeTab === 'attributes' && <AttributesTab entityId={id!} attributes={attributes} />}
                    {activeTab === 'relationships' && <RelationshipsTab entityId={id!} relationships={relationships} />}
                    {activeTab === 'notes' && <NotesTab entityId={id!} notes={notes} />}
                    {activeTab === 'templates' && <TemplateIntegration entity={entity} />}
                    {activeTab === 'graph' && <EnhancedRelationshipGraph entity={entity} />}
                    {activeTab === 'results' && <SearchResultsTab entityId={id!} results={[]} />}
                </div>
            </div>
        </div>
    );
};

// Overview Tab Component
const OverviewTab: React.FC<{ entity: Entity }> = ({ entity }) => {
    const InfoItem: React.FC<{ label: string; value: string | string[] | number | Record<string, string> | undefined; icon?: string }> = ({ label, value, icon }) => {
        if (!value || (Array.isArray(value) && value.length === 0)) return null;

        const displayValue = Array.isArray(value) 
            ? value.join(', ') 
            : typeof value === 'object' 
                ? JSON.stringify(value)
                : String(value);

        return (
            <div className="py-3 border-b border-gray-100 last:border-0">
                <dt className="text-sm font-medium text-gray-500 mb-1">
                    {icon && <span className="mr-2">{icon}</span>}
                    {label}
                </dt>
                <dd className="text-sm text-gray-900">
                    {displayValue}
                </dd>
            </div>
        );
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Basic Information */}
            <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">📋 Basic Information</h3>
                <dl className="space-y-1">
                    <InfoItem label="Name" value={entity.name} />
                    <InfoItem label="Entity Type" value={entity.entity_type_data?.display_name || entity.entity_type_name} />
                    {entity.aliases && entity.aliases.length > 0 && (
                        <InfoItem label="Aliases" value={entity.aliases} />
                    )}
                    <InfoItem label="Industry" value={entity.industry} icon="🏢" />
                    <InfoItem label="Location" value={entity.location} icon="📍" />
                    <InfoItem label="Founded" value={entity.founded_date} icon="📅" />
                </dl>
            </div>

            {/* Online Presence */}
            <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">🌐 Online Presence</h3>
                <dl className="space-y-1">
                    {entity.website && (
                        <div className="py-3 border-b border-gray-100">
                            <dt className="text-sm font-medium text-gray-500 mb-1">🔗 Website</dt>
                            <dd className="text-sm">
                                <a
                                    href={entity.website}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:text-blue-800"
                                >
                                    {entity.website}
                                </a>
                            </dd>
                        </div>
                    )}
                    {entity.domains && entity.domains.length > 0 && (
                        <InfoItem label="Domains" value={entity.domains.join(', ')} icon="🌍" />
                    )}
                    {entity.social_media && Object.keys(entity.social_media).length > 0 && (
                        <div className="py-3">
                            <dt className="text-sm font-medium text-gray-500 mb-2">📱 Social Media</dt>
                            <dd className="space-y-1">
                                {Object.entries(entity.social_media).map(([platform, url]) => (
                                    <div key={platform} className="text-sm">
                                        <span className="font-medium capitalize">{platform}:</span>{' '}
                                        <a
                                            href={url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-blue-600 hover:text-blue-800"
                                        >
                                            {url}
                                        </a>
                                    </div>
                                ))}
                            </dd>
                        </div>
                    )}
                </dl>
            </div>

            {/* Metadata */}
            <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 Metadata</h3>
                <dl className="space-y-1">
                    <InfoItem
                        label="Created"
                        value={new Date(entity.created_at).toLocaleString()}
                        icon="🕐"
                    />
                    <InfoItem
                        label="Updated"
                        value={new Date(entity.updated_at).toLocaleString()}
                        icon="🕐"
                    />
                    {entity.last_researched && (
                        <InfoItem
                            label="Last Researched"
                            value={new Date(entity.last_researched).toLocaleString()}
                            icon="🔍"
                        />
                    )}
                    <InfoItem label="Created By" value={entity.created_by_username} icon="👤" />
                </dl>
            </div>

            {/* Statistics */}
            <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">📈 Statistics</h3>
                <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 bg-white rounded-lg border border-gray-200">
                        <div className="text-3xl font-bold text-blue-600">{entity.search_count || 0}</div>
                        <div className="text-sm text-gray-600 mt-1">Searches</div>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg border border-gray-200">
                        <div className="text-3xl font-bold text-green-600">{entity.results_found || 0}</div>
                        <div className="text-sm text-gray-600 mt-1">Results Found</div>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg border border-gray-200">
                        <div className="text-3xl font-bold text-purple-600">{entity.attribute_count || 0}</div>
                        <div className="text-sm text-gray-600 mt-1">Attributes</div>
                    </div>
                    <div className="text-center p-4 bg-white rounded-lg border border-gray-200">
                        <div className="text-3xl font-bold text-orange-600">{entity.relationship_count || 0}</div>
                        <div className="text-sm text-gray-600 mt-1">Relationships</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Attributes Tab Component
const AttributesTab: React.FC<{ entityId: string; attributes: EntityAttribute[] }> = ({ entityId, attributes }) => {
    const [isAdding, setIsAdding] = useState(false);
    const [editingId, setEditingId] = useState<number | null>(null);
    const queryClient = useQueryClient();

    const deleteMutation = useMutation({
        mutationFn: (attributeId: number) => entitiesService.deleteAttribute(attributeId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-attributes', entityId] });
        },
    });

    const handleEdit = (attr: EntityAttribute) => {
        setEditingId(attr.id);
        setIsAdding(false);
    };

    const handleCancelEdit = () => {
        setEditingId(null);
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Entity Attributes</h3>
                <button
                    onClick={() => {
                        setIsAdding(!isAdding);
                        setEditingId(null);
                    }}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                >
                    {isAdding ? '✖️ Cancel' : '+ Add Attribute'}
                </button>
            </div>

            {isAdding && (
                <div className="mb-6">
                    <InlineAttributeForm
                        entityId={entityId}
                        onCancel={() => setIsAdding(false)}
                        onSuccess={() => setIsAdding(false)}
                    />
                </div>
            )}

            {attributes.length === 0 && !isAdding ? (
                <div className="text-center py-12 text-gray-500">
                    <div className="text-5xl mb-4">🏷️</div>
                    <p className="text-lg">No attributes added yet</p>
                    <p className="text-sm">Add custom attributes to store additional information</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {attributes.map((attr) => (
                        <div key={attr.id}>
                            {editingId === attr.id ? (
                                <InlineAttributeForm
                                    entityId={entityId}
                                    attributeId={attr.id}
                                    initialData={{
                                        key: attr.attribute_name,
                                        value: attr.attribute_value,
                                        value_type: attr.attribute_type,
                                        source: attr.source || '',
                                        confidence: (attr.confidence || 0.5) * 100,
                                        is_public: attr.is_public,
                                    }}
                                    onCancel={handleCancelEdit}
                                    onSuccess={handleCancelEdit}
                                />
                            ) : (
                                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-blue-300 transition-all group">
                                    <div className="flex justify-between items-start">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <h4 className="font-semibold text-gray-900">{attr.attribute_name}</h4>
                                                <span className="text-xs text-gray-500 bg-white px-2 py-0.5 rounded border border-gray-200">
                                                    {attr.attribute_type}
                                                </span>
                                                {attr.is_verified && (
                                                    <span className="text-green-600 text-xs font-medium">✓ Verified</span>
                                                )}
                                            </div>
                                            <p className="text-gray-700 mb-2">{attr.attribute_value}</p>
                                            <div className="flex items-center gap-3 text-xs text-gray-500">
                                                {attr.source && (
                                                    <span className="flex items-center gap-1">
                                                        <span className="font-medium">Source:</span> {attr.source}
                                                    </span>
                                                )}
                                                {attr.confidence && (
                                                    <span className="flex items-center gap-1">
                                                        <span className="font-medium">Confidence:</span> {Math.round(attr.confidence * 100)}%
                                                    </span>
                                                )}
                                                <span>{new Date(attr.created_at).toLocaleDateString()}</span>
                                            </div>
                                        </div>
                                        <div className="ml-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button
                                                onClick={() => handleEdit(attr)}
                                                className="text-blue-600 hover:text-blue-800 p-1 hover:bg-blue-50 rounded transition-colors"
                                                title="Edit attribute"
                                            >
                                                ✏️
                                            </button>
                                            <button
                                                onClick={() => {
                                                    if (window.confirm(`Delete attribute "${attr.attribute_name}"?`)) {
                                                        deleteMutation.mutate(attr.id);
                                                    }
                                                }}
                                                disabled={deleteMutation.isPending}
                                                className="text-red-600 hover:text-red-800 p-1 hover:bg-red-50 rounded disabled:opacity-50 transition-colors"
                                                title="Delete attribute"
                                            >
                                                🗑️
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

// Relationships Tab Component
const RelationshipsTab: React.FC<{ entityId: string; relationships: EntityRelationship[] }> = ({ entityId, relationships }) => {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [isAdding, setIsAdding] = useState(false);
    const [editingId, setEditingId] = useState<number | null>(null);

    const deleteMutation = useMutation({
        mutationFn: (relationshipId: number) => entitiesService.deleteRelationship(relationshipId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-relationships', entityId] });
        },
    });

    const handleEdit = (rel: EntityRelationship) => {
        setEditingId(rel.id);
        setIsAdding(false);
    };

    const handleCancelEdit = () => {
        setEditingId(null);
    };

    const relationshipTypeLabels: Record<string, string> = {
        parent_company: '🏢 Parent Company',
        subsidiary: '🏪 Subsidiary',
        partner: '🤝 Partner',
        competitor: '⚔️ Competitor',
        supplier: '📦 Supplier',
        customer: '🛒 Customer',
        employee: '👤 Employee',
        founder: '⭐ Founder',
        investor: '💰 Investor',
        acquired_by: '🔄 Acquired By',
        acquired: '🔄 Acquired',
        related: '🔗 Related',
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Entity Relationships</h3>
                <button
                    onClick={() => {
                        setIsAdding(!isAdding);
                        setEditingId(null);
                    }}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2"
                >
                    {isAdding ? '✖️ Cancel' : '+ Add Relationship'}
                </button>
            </div>

            {isAdding && (
                <div className="mb-6">
                    <InlineRelationshipForm
                        entityId={entityId}
                        onCancel={() => setIsAdding(false)}
                        onSuccess={() => setIsAdding(false)}
                    />
                </div>
            )}

            {relationships.length === 0 && !isAdding ? (
                <div className="text-center py-12 text-gray-500">
                    <div className="text-5xl mb-4">🔗</div>
                    <p className="text-lg">No relationships mapped yet</p>
                    <p className="text-sm">Connect this entity with related entities</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {relationships.map((rel) => (
                        <div key={rel.id}>
                            {editingId === rel.id ? (
                                <InlineRelationshipForm
                                    entityId={entityId}
                                    relationshipId={rel.id}
                                    initialData={{
                                        to_entity: String(rel.to_entity),
                                        relationship_type: rel.relationship_type,
                                        description: rel.description,
                                        confidence: (rel.confidence || 0.5) * 100,
                                        source: rel.source || '',
                                        start_date: rel.start_date || '',
                                        end_date: rel.end_date || '',
                                        is_active: rel.is_active !== undefined ? rel.is_active : true,
                                    }}
                                    onCancel={handleCancelEdit}
                                    onSuccess={handleCancelEdit}
                                />
                            ) : (
                                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-purple-300 transition-all group">
                                    <div className="flex justify-between items-start">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-2">
                                                <span className="text-lg">
                                                    {relationshipTypeLabels[rel.relationship_type]?.split(' ')[0] || '🔗'}
                                                </span>
                                                <h4 className="font-semibold text-gray-900">
                                                    {relationshipTypeLabels[rel.relationship_type]?.substring(2) || rel.relationship_type}
                                                </h4>
                                                {!rel.is_active && (
                                                    <span className="text-xs bg-gray-200 text-gray-600 px-2 py-0.5 rounded">
                                                        Inactive
                                                    </span>
                                                )}
                                            </div>
                                            <div className="mb-2">
                                                <button
                                                    onClick={() => navigate(`/entities/${rel.to_entity}`)}
                                                    className="text-blue-600 hover:text-blue-800 font-medium"
                                                >
                                                    {rel.to_entity_name || `Entity ${rel.to_entity}`}
                                                </button>
                                            </div>
                                            {rel.description && (
                                                <p className="text-sm text-gray-600 mb-2">{rel.description}</p>
                                            )}
                                            <div className="flex items-center gap-3 text-xs text-gray-500">
                                                {rel.confidence && (
                                                    <span>Confidence: {Math.round(rel.confidence * 100)}%</span>
                                                )}
                                                {rel.source && <span>Source: {rel.source}</span>}
                                                {rel.start_date && <span>Since: {new Date(rel.start_date).toLocaleDateString()}</span>}
                                                <span>By: {rel.created_by_username}</span>
                                            </div>
                                        </div>
                                        <div className="ml-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button
                                                onClick={() => handleEdit(rel)}
                                                className="text-purple-600 hover:text-purple-800 p-1 hover:bg-purple-50 rounded transition-colors"
                                                title="Edit relationship"
                                            >
                                                ✏️
                                            </button>
                                            <button
                                                onClick={() => {
                                                    if (window.confirm(`Delete this relationship?`)) {
                                                        deleteMutation.mutate(rel.id);
                                                    }
                                                }}
                                                disabled={deleteMutation.isPending}
                                                className="text-red-600 hover:text-red-800 p-1 hover:bg-red-50 rounded disabled:opacity-50 transition-colors"
                                                title="Delete relationship"
                                            >
                                                🗑️
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

// Notes Tab Component
const NotesTab: React.FC<{ entityId: string; notes: EntityNote[] }> = ({ entityId, notes }) => {
    const [isAdding, setIsAdding] = useState(false);
    const queryClient = useQueryClient();

    const deleteMutation = useMutation({
        mutationFn: (noteId: number) => entitiesService.deleteNote(noteId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-notes', entityId] });
        },
    });

    const noteTypeIcons: Record<string, string> = {
        general: '�',
        finding: '🔍',
        vulnerability: '⚠️',
        contact: '📞',
        technical: '⚙️',
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Research Notes</h3>
                <button
                    onClick={() => setIsAdding(!isAdding)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    + Add Note
                </button>
            </div>

            {isAdding && (
                <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                    <p className="text-gray-600">Add note form coming soon...</p>
                </div>
            )}

            {notes.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                    <div className="text-5xl mb-4">📝</div>
                    <p className="text-lg">No notes recorded yet</p>
                    <p className="text-sm">Add research findings and observations</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {notes.map((note) => (
                        <div key={note.id} className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-gray-300 transition-colors">
                            <div className="flex justify-between items-start mb-2">
                                <div className="flex items-center gap-2">
                                    <span className="text-xl">{noteTypeIcons[note.note_type] || '📝'}</span>
                                    <h4 className="font-semibold text-gray-900">{note.title}</h4>
                                    {note.is_important && (
                                        <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs font-medium">
                                            ⭐ Important
                                        </span>
                                    )}
                                </div>
                                <button
                                    onClick={() => deleteMutation.mutate(note.id)}
                                    disabled={deleteMutation.isPending}
                                    className="text-red-600 hover:text-red-800 disabled:opacity-50"
                                    title="Delete note"
                                >
                                    🗑️
                                </button>
                            </div>
                            <p className="text-gray-700 whitespace-pre-wrap mb-3">{note.content}</p>
                            {note.tags && (
                                <div className="flex items-center gap-2 flex-wrap mb-2">
                                    {(typeof note.tags === 'string' ? note.tags.split(',') : []).map((tag, index) => (
                                        <span key={index} className="px-2 py-1 bg-white text-gray-700 rounded text-xs border border-gray-200">
                                            #{tag.trim()}
                                        </span>
                                    ))}
                                </div>
                            )}
                            <div className="text-xs text-gray-500">
                                By {note.created_by_username} • {new Date(note.created_at).toLocaleString()}
                                {note.created_at !== note.updated_at && (
                                    <span> • Edited {new Date(note.updated_at).toLocaleString()}</span>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

// Search Results Tab Component
const SearchResultsTab: React.FC<{ entityId: string; results: EntitySearchResult[] }> = ({ entityId }) => {
    // Fetch search sessions for this entity
    const { data: sessions = [], isLoading } = useQuery({
        queryKey: ['entity-search-sessions', entityId],
        queryFn: () => entitiesService.getEntitySearchSessions(Number(entityId)),
    });

    // Fetch results for a specific session
    const [selectedSession, setSelectedSession] = useState<number | null>(null);
    const { data: sessionResults = [] } = useQuery({
        queryKey: ['session-results', selectedSession],
        queryFn: () => entitiesService.getSearchSessionResults(selectedSession!),
        enabled: !!selectedSession,
    });

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (sessions.length === 0) {
        return (
            <div className="text-center py-12 text-gray-500">
                <div className="text-5xl mb-4">🔍</div>
                <p className="text-lg font-medium mb-2">No search sessions yet</p>
                <p className="text-sm">Go to the Templates tab to execute searches for this entity</p>
            </div>
        );
    }

    const statusColors = {
        pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
        running: 'bg-blue-100 text-blue-800 border-blue-200',
        completed: 'bg-green-100 text-green-800 border-green-200',
        failed: 'bg-red-100 text-red-800 border-red-200',
    };

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Search Sessions ({sessions.length})
                </h3>

                <div className="space-y-4">
                    {sessions.map((session) => (
                        <div key={session.id} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                            {/* Session Header */}
                            <div
                                className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                                onClick={() => setSelectedSession(selectedSession === session.id ? null : session.id)}
                            >
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-2">
                                            <h4 className="font-semibold text-gray-900">
                                                {session.template_name}
                                            </h4>
                                            <span className={`px-2 py-1 rounded text-xs font-medium border ${statusColors[session.status]}`}>
                                                {session.status.toUpperCase()}
                                            </span>
                                            {session.result_count > 0 && (
                                                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                                                    {session.result_count} result{session.result_count !== 1 ? 's' : ''}
                                                </span>
                                            )}
                                        </div>

                                        <code className="block text-xs bg-gray-50 p-2 rounded border border-gray-200 text-gray-700 font-mono mb-2">
                                            {session.executed_query}
                                        </code>

                                        <div className="flex items-center gap-4 text-xs text-gray-500">
                                            <span>👤 {session.user_username}</span>
                                            <span>🕐 Started: {new Date(session.started_at).toLocaleString()}</span>
                                            {session.completed_at && (
                                                <span>✓ Completed: {new Date(session.completed_at).toLocaleString()}</span>
                                            )}
                                        </div>
                                    </div>

                                    <button className="ml-4 text-gray-400 hover:text-gray-600">
                                        {selectedSession === session.id ? '▼' : '▶'}
                                    </button>
                                </div>
                            </div>

                            {/* Session Results (Collapsible) */}
                            {selectedSession === session.id && (
                                <div className="border-t border-gray-200 bg-gray-50 p-4">
                                    {session.status === 'completed' && session.result_count > 0 ? (
                                        <div className="space-y-3">
                                            <h5 className="font-medium text-gray-900 mb-3">
                                                Search Results ({sessionResults.length})
                                            </h5>
                                            {sessionResults.map((result) => (
                                                <div key={result.id} className="bg-white rounded-lg p-4 border border-gray-200">
                                                    <div className="flex items-start gap-2 mb-2">
                                                        {result.is_verified && <span className="text-green-600 text-sm">✓</span>}
                                                        <div className="flex-1">
                                                            <a
                                                                href={result.url}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                className="text-blue-600 hover:text-blue-800 font-medium text-sm block mb-1"
                                                            >
                                                                {result.title}
                                                            </a>
                                                            <p className="text-xs text-gray-600 mb-2">{result.snippet}</p>
                                                            <div className="flex items-center gap-3 text-xs text-gray-500">
                                                                <span>Position: #{result.position}</span>
                                                                {result.relevance_score && (
                                                                    <span>📊 Relevance: {result.relevance_score}%</span>
                                                                )}
                                                                <span>{new Date(result.created_at).toLocaleDateString()}</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    {result.notes && (
                                                        <div className="mt-2 pt-2 border-t border-gray-200">
                                                            <p className="text-xs text-gray-700">
                                                                <span className="font-medium">Notes:</span> {result.notes}
                                                            </p>
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    ) : session.status === 'pending' ? (
                                        <div className="text-center py-4 text-gray-500">
                                            <p className="text-sm">⏳ Search is pending execution</p>
                                        </div>
                                    ) : session.status === 'running' ? (
                                        <div className="text-center py-4 text-gray-500">
                                            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500 mx-auto mb-2"></div>
                                            <p className="text-sm">Search is running...</p>
                                        </div>
                                    ) : session.status === 'failed' ? (
                                        <div className="text-center py-4 text-red-500">
                                            <p className="text-sm">❌ Search failed</p>
                                        </div>
                                    ) : (
                                        <div className="text-center py-4 text-gray-500">
                                            <p className="text-sm">No results found</p>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default EntityDetail;
