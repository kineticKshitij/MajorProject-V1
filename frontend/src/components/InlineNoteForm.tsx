import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { entitiesService } from '../services/entitiesService';

interface InlineNoteFormProps {
    entityId: string;
    noteId?: number;
    initialData?: {
        title: string;
        content: string;
        note_type?: string;
        is_important?: boolean;
        tags?: string[];
    };
    onCancel: () => void;
    onSuccess?: () => void;
}

const InlineNoteForm: React.FC<InlineNoteFormProps> = ({
    entityId,
    noteId,
    initialData,
    onCancel,
    onSuccess
}) => {
    const queryClient = useQueryClient();
    const isEditing = !!noteId;

    const [formData, setFormData] = useState({
        title: initialData?.title || '',
        content: initialData?.content || '',
        note_type: initialData?.note_type || 'general',
        is_important: initialData?.is_important || false,
        tags: initialData?.tags?.join(', ') || '',
    });

    const [errors, setErrors] = useState<Record<string, string>>({});

    const createMutation = useMutation({
        mutationFn: (data: any) => entitiesService.createNote(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-notes', entityId] });
            queryClient.invalidateQueries({ queryKey: ['entity', entityId] });
            onSuccess?.();
            onCancel();
        },
    });

    const updateMutation = useMutation({
        mutationFn: (data: any) => entitiesService.updateNote(noteId!, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity-notes', entityId] });
            queryClient.invalidateQueries({ queryKey: ['entity', entityId] });
            onSuccess?.();
            onCancel();
        },
    });

    const validate = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.title.trim()) {
            newErrors.title = 'Title is required';
        }
        if (!formData.content.trim()) {
            newErrors.content = 'Content is required';
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
            title: formData.title,
            content: formData.content,
            note_type: formData.note_type,
            is_important: formData.is_important,
            tags: formData.tags || null,
        };

        if (isEditing) {
            updateMutation.mutate(submitData);
        } else {
            createMutation.mutate(submitData);
        }
    };

    const isSubmitting = createMutation.isPending || updateMutation.isPending;

    const noteTypes = [
        { value: 'general', label: '📝 General', icon: '📝' },
        { value: 'finding', label: '🔍 Finding', icon: '🔍' },
        { value: 'vulnerability', label: '⚠️ Vulnerability', icon: '⚠️' },
        { value: 'contact', label: '📞 Contact', icon: '📞' },
        { value: 'technical', label: '⚙️ Technical', icon: '⚙️' },
    ];

    return (
        <form onSubmit={handleSubmit} className="bg-green-50 rounded-lg p-4 border-2 border-green-200 animate-fadeIn">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                {/* Title Field */}
                <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Title <span className="text-red-500">*</span>
                    </label>
                    <input
                        type="text"
                        value={formData.title}
                        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                        placeholder="e.g., Security Vulnerability Found"
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent ${errors.title ? 'border-red-500' : 'border-gray-300'
                            }`}
                        disabled={isSubmitting}
                        autoFocus
                    />
                    {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
                </div>

                {/* Note Type */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Note Type
                    </label>
                    <select
                        value={formData.note_type}
                        onChange={(e) => setFormData({ ...formData, note_type: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        disabled={isSubmitting}
                    >
                        {noteTypes.map((type) => (
                            <option key={type.value} value={type.value}>
                                {type.label}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Content Field */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Content <span className="text-red-500">*</span>
                </label>
                <textarea
                    value={formData.content}
                    onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                    placeholder="Enter your note content..."
                    rows={5}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent font-mono text-sm ${errors.content ? 'border-red-500' : 'border-gray-300'
                        }`}
                    disabled={isSubmitting}
                />
                {errors.content && <p className="text-red-500 text-xs mt-1">{errors.content}</p>}
            </div>

            {/* Tags Field */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tags
                </label>
                <input
                    type="text"
                    value={formData.tags}
                    onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                    placeholder="e.g., security, urgent, follow-up (comma-separated)"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    disabled={isSubmitting}
                />
                <p className="text-xs text-gray-500 mt-1">Separate multiple tags with commas</p>
            </div>

            {/* Important Checkbox */}
            <div className="mb-4">
                <label className="flex items-center gap-2 cursor-pointer">
                    <input
                        type="checkbox"
                        checked={formData.is_important}
                        onChange={(e) => setFormData({ ...formData, is_important: e.target.checked })}
                        className="w-4 h-4 text-yellow-600 rounded focus:ring-2 focus:ring-green-500"
                        disabled={isSubmitting}
                    />
                    <span className="text-sm text-gray-700 flex items-center gap-1">
                        ⭐ Mark as important
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
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                    {isSubmitting ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                            Saving...
                        </>
                    ) : (
                        <>
                            {isEditing ? '💾 Update' : '➕ Add'} Note
                        </>
                    )}
                </button>
            </div>
        </form>
    );
};

export default InlineNoteForm;
