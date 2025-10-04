import React, { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';

interface InlineRelationshipFormProps {
    entityId: string;
    relationshipId?: number;
    initialData?: {
        to_entity: string;
        relationship_type: string;
        description?: string;
        confidence?: number;
        source?: string;
        start_date?: string;
        end_date?: string;
        is_active?: boolean;
    };
    onCancel: () => void;
    onSuccess?: () => void;
}

const InlineRelationshipForm: React.FC<InlineRelationshipFormProps> = ({
    entityId,
    relationshipId,
    initialData,
    onCancel,
    onSuccess
}) => {
    const queryClient = useQueryClient();
    const isEditing = !!relationshipId;

    const [formData, setFormData] = useState({
        to_entity: initialData?.to_entity || '',
        relationship_type: initialData?.relationship_type || 'related',
        description: initialData?.description || '',
        confidence: initialData?.confidence || 50,
        source: initialData?.source || '',
        start_date: initialData?.start_date || '',
        end_date: initialData?.end_date || '',
        is_active: initialData?.is_active ?? true,
    });

    const [errors, setErrors] = useState<Record<string, string>>({});
    const [entitySearch, setEntitySearch] = useState('');

    // Fetch entities for the dropdown
    const { data: entitiesData } = useQuery({
        queryKey: ['entities-search', entitySearch],
        queryFn: () => entitiesService.getEntities({ search: entitySearch }),
        enabled: entitySearch.length > 0,
    });

    const createMutation = useMutation({
        mutationFn: (data: any) => entitiesService.createRelationship(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-relationships', entityId] });
            queryClient.invalidateQueries({ queryKey: ['entity', entityId] });
            onSuccess?.();
            onCancel();
        },
    });

    const updateMutation = useMutation({
        mutationFn: (data: any) => entitiesService.updateRelationship(relationshipId!, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-relationships', entityId] });
            queryClient.invalidateQueries({ queryKey: ['entity', entityId] });
            onSuccess?.();
            onCancel();
        },
    });

    const validate = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.to_entity) {
            newErrors.to_entity = 'Target entity is required';
        }
        if (formData.to_entity === entityId) {
            newErrors.to_entity = 'Cannot create relationship to the same entity';
        }
        if (!formData.relationship_type) {
            newErrors.relationship_type = 'Relationship type is required';
        }
        if (formData.confidence < 0 || formData.confidence > 100) {
            newErrors.confidence = 'Confidence must be between 0 and 100';
        }
        if (formData.start_date && formData.end_date && formData.start_date > formData.end_date) {
            newErrors.end_date = 'End date must be after start date';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!validate()) {
            return;
        }

        const submitData = {
            from_entity: entityId,
            to_entity: formData.to_entity,
            relationship_type: formData.relationship_type,
            description: formData.description || null,
            confidence: formData.confidence / 100, // Convert to 0-1 range
            source: formData.source || null,
            start_date: formData.start_date || null,
            end_date: formData.end_date || null,
            is_active: formData.is_active,
        };

        if (isEditing) {
            updateMutation.mutate(submitData);
        } else {
            createMutation.mutate(submitData);
        }
    };

    const isSubmitting = createMutation.isPending || updateMutation.isPending;

    const relationshipTypes = [
        { value: 'parent_company', label: '🏢 Parent Company', icon: '🏢' },
        { value: 'subsidiary', label: '🏪 Subsidiary', icon: '🏪' },
        { value: 'partner', label: '🤝 Partner', icon: '🤝' },
        { value: 'competitor', label: '⚔️ Competitor', icon: '⚔️' },
        { value: 'supplier', label: '📦 Supplier', icon: '📦' },
        { value: 'customer', label: '🛒 Customer', icon: '🛒' },
        { value: 'employee', label: '👤 Employee', icon: '👤' },
        { value: 'founder', label: '⭐ Founder', icon: '⭐' },
        { value: 'investor', label: '💰 Investor', icon: '💰' },
        { value: 'acquired_by', label: '🔄 Acquired By', icon: '🔄' },
        { value: 'acquired', label: '🔄 Acquired', icon: '🔄' },
        { value: 'related', label: '🔗 Related', icon: '🔗' },
    ];

    return (
        <form onSubmit={handleSubmit} className="bg-purple-50 rounded-lg p-4 border-2 border-purple-200 animate-fadeIn">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                {/* Target Entity */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Target Entity <span className="text-red-500">*</span>
                    </label>
                    <input
                        type="text"
                        value={entitySearch}
                        onChange={(e) => setEntitySearch(e.target.value)}
                        placeholder="Search for an entity..."
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${errors.to_entity ? 'border-red-500' : 'border-gray-300'
                            }`}
                        disabled={isSubmitting}
                        autoFocus
                    />
                    {errors.to_entity && <p className="text-red-500 text-xs mt-1">{errors.to_entity}</p>}

                    {/* Entity Search Results */}
                    {entitySearch && entitiesData && entitiesData.results.length > 0 && (
                        <div className="mt-2 max-h-40 overflow-y-auto bg-white border border-gray-300 rounded-lg shadow-lg">
                            {entitiesData.results
                                .filter(e => String(e.id) !== entityId)
                                .map((entity) => (
                                    <button
                                        key={entity.id}
                                        type="button"
                                        onClick={() => {
                                            setFormData({ ...formData, to_entity: String(entity.id) });
                                            setEntitySearch(entity.name);
                                        }}
                                        className="w-full text-left px-3 py-2 hover:bg-gray-100 transition-colors flex items-center gap-2"
                                    >
                                        <span>{entity.entity_type_data?.icon || '📌'}</span>
                                        <span className="font-medium">{entity.name}</span>
                                        <span className="text-xs text-gray-500">
                                            ({entity.entity_type_data?.display_name})
                                        </span>
                                    </button>
                                ))}
                        </div>
                    )}
                </div>

                {/* Relationship Type */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Relationship Type <span className="text-red-500">*</span>
                    </label>
                    <select
                        value={formData.relationship_type}
                        onChange={(e) => setFormData({ ...formData, relationship_type: e.target.value })}
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${errors.relationship_type ? 'border-red-500' : 'border-gray-300'
                            }`}
                        disabled={isSubmitting}
                    >
                        {relationshipTypes.map((type) => (
                            <option key={type.value} value={type.value}>
                                {type.label}
                            </option>
                        ))}
                    </select>
                    {errors.relationship_type && (
                        <p className="text-red-500 text-xs mt-1">{errors.relationship_type}</p>
                    )}
                </div>
            </div>

            {/* Description Field */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                </label>
                <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Describe this relationship..."
                    rows={2}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    disabled={isSubmitting}
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                {/* Source Field */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Source
                    </label>
                    <input
                        type="text"
                        value={formData.source}
                        onChange={(e) => setFormData({ ...formData, source: e.target.value })}
                        placeholder="e.g., LinkedIn"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        disabled={isSubmitting}
                    />
                </div>

                {/* Start Date */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Start Date
                    </label>
                    <input
                        type="date"
                        value={formData.start_date}
                        onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        disabled={isSubmitting}
                    />
                </div>

                {/* End Date */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        End Date
                    </label>
                    <input
                        type="date"
                        value={formData.end_date}
                        onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${errors.end_date ? 'border-red-500' : 'border-gray-300'
                            }`}
                        disabled={isSubmitting}
                    />
                    {errors.end_date && <p className="text-red-500 text-xs mt-1">{errors.end_date}</p>}
                </div>
            </div>

            {/* Confidence Slider */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Confidence: {formData.confidence}%
                </label>
                <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={formData.confidence}
                    onChange={(e) => setFormData({ ...formData, confidence: parseInt(e.target.value) })}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
                    disabled={isSubmitting}
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Low</span>
                    <span>Medium</span>
                    <span>High</span>
                </div>
            </div>

            {/* Active Checkbox */}
            <div className="mb-4">
                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="checkbox"
                        checked={formData.is_active}
                        onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                        className="w-4 h-4 text-purple-600 rounded focus:ring-2 focus:ring-purple-500"
                        disabled={isSubmitting}
                    />
                    <span className="text-sm text-gray-700">
                        Active relationship
                    </span>
                </label>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-end gap-2">
                <button
                    type="button"
                    onClick={onCancel}
                    disabled={isSubmitting}
                    className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                    Cancel
                </button>
                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                    {isSubmitting ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                            Saving...
                        </>
                    ) : (
                        <>
                            {isEditing ? '💾 Update' : '➕ Add'} Relationship
                        </>
                    )}
                </button>
            </div>
        </form>
    );
};

export default InlineRelationshipForm;
