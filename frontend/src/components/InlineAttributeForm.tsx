import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';

interface InlineAttributeFormProps {
    entityId: string;
    attributeId?: number;
    initialData?: {
        key: string;
        value: string;
        value_type?: string;
        source?: string;
        confidence?: number;
        is_public?: boolean;
    };
    onCancel: () => void;
    onSuccess?: () => void;
}

const InlineAttributeForm: React.FC<InlineAttributeFormProps> = ({
    entityId,
    attributeId,
    initialData,
    onCancel,
    onSuccess
}) => {
    const queryClient = useQueryClient();
    const isEditing = !!attributeId;

    const [formData, setFormData] = useState({
        key: initialData?.key || '',
        value: initialData?.value || '',
        value_type: initialData?.value_type || 'text',
        source: initialData?.source || '',
        confidence: initialData?.confidence || 50,
        is_public: initialData?.is_public ?? true,
    });

    const [errors, setErrors] = useState<Record<string, string>>({});

    const createMutation = useMutation({
        mutationFn: (data: Record<string, unknown>) => entitiesService.createEntityAttribute(entityId, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-attributes', entityId] });
            queryClient.invalidateQueries({ queryKey: ['entity', entityId] });
            onSuccess?.();
            onCancel();
        },
    });

    const updateMutation = useMutation({
        mutationFn: (data: Record<string, unknown>) => entitiesService.updateAttribute(attributeId!, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-attributes', entityId] });
            queryClient.invalidateQueries({ queryKey: ['entity', entityId] });
            onSuccess?.();
            onCancel();
        },
    });

    const validate = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.key.trim()) {
            newErrors.key = 'Key is required';
        }
        if (!formData.value.trim()) {
            newErrors.value = 'Value is required';
        }
        if (formData.confidence < 0 || formData.confidence > 100) {
            newErrors.confidence = 'Confidence must be between 0 and 100';
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
            entity: entityId,
            attribute_name: formData.key,
            attribute_value: formData.value,
            attribute_type: formData.value_type,
            source: formData.source || null,
            confidence: formData.confidence / 100, // Convert to 0-1 range
            is_public: formData.is_public,
        };

        if (isEditing) {
            updateMutation.mutate(submitData);
        } else {
            createMutation.mutate(submitData);
        }
    };

    const isSubmitting = createMutation.isPending || updateMutation.isPending;

    return (
        <form onSubmit={handleSubmit} className="bg-blue-50 rounded-lg p-4 border-2 border-blue-200 animate-fadeIn">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                {/* Key Field */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Key <span className="text-red-500">*</span>
                    </label>
                    <input
                        type="text"
                        value={formData.key}
                        onChange={(e) => setFormData({ ...formData, key: e.target.value })}
                        placeholder="e.g., email, phone, address"
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.key ? 'border-red-500' : 'border-gray-300'
                            }`}
                        disabled={isSubmitting}
                        autoFocus
                    />
                    {errors.key && <p className="text-red-500 text-xs mt-1">{errors.key}</p>}
                </div>

                {/* Value Type */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Type
                    </label>
                    <select
                        value={formData.value_type}
                        onChange={(e) => setFormData({ ...formData, value_type: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={isSubmitting}
                    >
                        <option value="text">Text</option>
                        <option value="number">Number</option>
                        <option value="email">Email</option>
                        <option value="phone">Phone</option>
                        <option value="url">URL</option>
                        <option value="date">Date</option>
                        <option value="json">JSON</option>
                    </select>
                </div>
            </div>

            {/* Value Field */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Value <span className="text-red-500">*</span>
                </label>
                <textarea
                    value={formData.value}
                    onChange={(e) => setFormData({ ...formData, value: e.target.value })}
                    placeholder="Enter the attribute value"
                    rows={3}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.value ? 'border-red-500' : 'border-gray-300'
                        }`}
                    disabled={isSubmitting}
                />
                {errors.value && <p className="text-red-500 text-xs mt-1">{errors.value}</p>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                {/* Source Field */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Source
                    </label>
                    <input
                        type="text"
                        value={formData.source}
                        onChange={(e) => setFormData({ ...formData, source: e.target.value })}
                        placeholder="e.g., LinkedIn, Website, Manual"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={isSubmitting}
                    />
                </div>

                {/* Confidence Slider */}
                <div>
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
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        disabled={isSubmitting}
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                        <span>Low</span>
                        <span>Medium</span>
                        <span>High</span>
                    </div>
                </div>
            </div>

            {/* Public Checkbox */}
            <div className="mb-4">
                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="checkbox"
                        checked={formData.is_public}
                        onChange={(e) => setFormData({ ...formData, is_public: e.target.checked })}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                        disabled={isSubmitting}
                    />
                    <span className="text-sm text-gray-700">
                        Public (visible to all users)
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
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                    {isSubmitting ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                            Saving...
                        </>
                    ) : (
                        <>
                            {isEditing ? '💾 Update' : '➕ Add'} Attribute
                        </>
                    )}
                </button>
            </div>
        </form>
    );
};

export default InlineAttributeForm;
