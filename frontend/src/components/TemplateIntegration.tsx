import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';
import type { Entity, EntitySearchTemplate } from '../types';

interface TemplateIntegrationProps {
    entity: Entity;
}

// Query generation - replaces placeholders with entity data
const generateQuery = (template: string, entity: Entity): string => {
    let query = template;

    // Replace common placeholders
    const replacements: Record<string, string> = {
        '{name}': entity.name,
        '{entity_name}': entity.name,
        '{company}': entity.name,
        '{organization}': entity.name,
        '{domain}': entity.website ? new URL(entity.website).hostname : '',
        '{website}': entity.website || '',
        '{location}': entity.location || '',
        '{industry}': entity.industry || '',
    };

    // Also add aliases if they exist
    if (entity.aliases && entity.aliases.length > 0) {
        replacements['{alias}'] = entity.aliases[0];
    }

    // Add domains if they exist
    if (entity.domains && entity.domains.length > 0) {
        replacements['{domain}'] = entity.domains[0];
    }

    // Perform replacements
    Object.entries(replacements).forEach(([placeholder, value]) => {
        query = query.replace(new RegExp(placeholder, 'gi'), value);
    });

    return query;
};

// Risk level colors
const riskColors = {
    low: 'bg-green-100 text-green-800 border-green-200',
    medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    high: 'bg-orange-100 text-orange-800 border-orange-200',
    critical: 'bg-red-100 text-red-800 border-red-200',
};

const riskIcons = {
    low: '✓',
    medium: '⚠',
    high: '⚠️',
    critical: '🔴',
};

const TemplateIntegration: React.FC<TemplateIntegrationProps> = ({ entity }) => {
    const queryClient = useQueryClient();
    const [selectedTemplate, setSelectedTemplate] = useState<EntitySearchTemplate | null>(null);
    const [categoryFilter, setCategoryFilter] = useState<string>('all');

    // Fetch templates for this entity type
    const { data: templates = [], isLoading } = useQuery({
        queryKey: ['search-templates', entity.entity_type],
        queryFn: () => entitiesService.getSearchTemplates({
            entity_type: entity.entity_type,
        }),
    });

    // Execute search mutation
    const executeMutation = useMutation({
        mutationFn: async (template: EntitySearchTemplate) => {
            const executedQuery = generateQuery(template.template_query, entity);
            return entitiesService.createSearchSession({
                entity: entity.id,
                search_template: template.id,
                session_name: `${template.name} - ${entity.name}`,
                executed_query: executedQuery,
                status: 'pending',
            });
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-search-sessions', entity.id] });
            setSelectedTemplate(null);
        },
    });

    // Get unique categories
    const categories = Array.from(new Set(templates.map(t => t.category)));
    const filteredTemplates = categoryFilter === 'all'
        ? templates
        : templates.filter(t => t.category === categoryFilter);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (templates.length === 0) {
        return (
            <div className="text-center py-12">
                <div className="text-gray-400 text-5xl mb-4">🔍</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                    No Templates Available
                </h3>
                <p className="text-gray-600">
                    No search templates are available for {entity.entity_type_name} entities yet.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                        Search Templates
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                        {filteredTemplates.length} template{filteredTemplates.length !== 1 ? 's' : ''} available for {entity.entity_type_name}
                    </p>
                </div>

                {/* Category Filter */}
                {categories.length > 1 && (
                    <select
                        value={categoryFilter}
                        onChange={(e) => setCategoryFilter(e.target.value)}
                        className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        <option value="all">All Categories</option>
                        {categories.map(category => (
                            <option key={category} value={category}>
                                {category}
                            </option>
                        ))}
                    </select>
                )}
            </div>

            {/* Templates Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredTemplates.map((template) => {
                    const generatedQuery = generateQuery(template.template_query, entity);
                    const isExecuting = executeMutation.isPending && selectedTemplate?.id === template.id;

                    return (
                        <div
                            key={template.id}
                            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                        >
                            {/* Template Header */}
                            <div className="flex items-start justify-between mb-3">
                                <div className="flex-1">
                                    <h4 className="font-semibold text-gray-900 mb-1">
                                        {template.name}
                                    </h4>
                                    <p className="text-sm text-gray-600">
                                        {template.description}
                                    </p>
                                </div>
                                <span className={`px-2 py-1 rounded text-xs font-medium border ${riskColors[template.risk_level]}`}>
                                    {riskIcons[template.risk_level]} {template.risk_level.toUpperCase()}
                                </span>
                            </div>

                            {/* Category Badge */}
                            <div className="mb-3">
                                <span className="inline-block px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-medium">
                                    {template.category}
                                </span>
                            </div>

                            {/* Original Template Query */}
                            <div className="mb-3">
                                <label className="text-xs font-medium text-gray-700 mb-1 block">
                                    Template:
                                </label>
                                <code className="block text-xs bg-gray-50 p-2 rounded border border-gray-200 text-gray-700 font-mono">
                                    {template.template_query}
                                </code>
                            </div>

                            {/* Generated Query Preview */}
                            <div className="mb-3">
                                <label className="text-xs font-medium text-gray-700 mb-1 block">
                                    Generated Query:
                                </label>
                                <code className="block text-xs bg-blue-50 p-2 rounded border border-blue-200 text-blue-900 font-mono">
                                    {generatedQuery}
                                </code>
                            </div>

                            {/* Usage Tips */}
                            {template.usage_tips && (
                                <div className="mb-3 p-2 bg-yellow-50 border border-yellow-200 rounded">
                                    <p className="text-xs text-yellow-800">
                                        💡 <strong>Tip:</strong> {template.usage_tips}
                                    </p>
                                </div>
                            )}

                            {/* Expected Results */}
                            {template.expected_results && (
                                <div className="mb-3">
                                    <p className="text-xs text-gray-600">
                                        <strong>Expected:</strong> {template.expected_results}
                                    </p>
                                </div>
                            )}

                            {/* Execute Button */}
                            <button
                                onClick={() => {
                                    setSelectedTemplate(template);
                                    executeMutation.mutate(template);
                                }}
                                disabled={isExecuting || !template.is_active}
                                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                            >
                                {isExecuting ? (
                                    <>
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                        <span>Executing...</span>
                                    </>
                                ) : (
                                    <>
                                        <span>🔍</span>
                                        <span>Execute Search</span>
                                    </>
                                )}
                            </button>
                        </div>
                    );
                })}
            </div>

            {/* Success Message */}
            {executeMutation.isSuccess && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <p className="text-green-800 text-sm">
                        ✅ Search session created successfully! Check the Search Results tab to view results.
                    </p>
                </div>
            )}

            {/* Error Message */}
            {executeMutation.isError && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 text-sm">
                        ❌ Failed to execute search. Please try again.
                    </p>
                </div>
            )}
        </div>
    );
};

export default TemplateIntegration;
