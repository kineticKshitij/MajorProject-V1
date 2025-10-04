import api from './api';
import type {
    Entity,
    EntityType,
    EntityAttribute,
    EntitySearchTemplate,
    EntitySearchSession,
    EntitySearchResult,
    EntityRelationship,
    EntityNote,
    PaginatedResponse,
} from '../types';

export const entitiesService = {
    // Entity Types
    async getEntityTypes(): Promise<EntityType[]> {
        const response = await api.get<PaginatedResponse<EntityType>>('/dorks/entity-types/');
        return response.data.results; // Return results array from paginated response
    },

    async getEntityType(id: number): Promise<EntityType> {
        const response = await api.get<EntityType>(`/dorks/entity-types/${id}/`);
        return response.data;
    },

    // Entities
    async getEntities(params?: {
        page?: number;
        search?: string;
        entity_type?: number;
        status?: string;
        priority?: string;
    }): Promise<PaginatedResponse<Entity>> {
        const response = await api.get<PaginatedResponse<Entity>>('/dorks/entities/', {
            params,
        });
        return response.data;
    },

    async getEntity(id: string | number): Promise<Entity> {
        const response = await api.get<Entity>(`/dorks/entities/${id}/`);
        return response.data;
    },

    async createEntity(data: Partial<Entity>): Promise<Entity> {
        const response = await api.post<Entity>('/dorks/entities/', data);
        return response.data;
    },

    async updateEntity(id: string | number, data: Partial<Entity>): Promise<Entity> {
        const response = await api.put<Entity>(`/dorks/entities/${id}/`, data);
        return response.data;
    },

    async deleteEntity(id: string | number): Promise<void> {
        await api.delete(`/dorks/entities/${id}/`);
    },

    async getEntityStatistics(): Promise<{
        total_entities: number;
        status_distribution: Array<{ status: string; count: number }>;
        type_distribution: Array<{ entity_type__name: string; count: number }>;
    }> {
        const response = await api.get('/dorks/entities/statistics/');
        return response.data;
    },

    // Entity Attributes
    async getEntityAttributes(entityId: string | number): Promise<EntityAttribute[]> {
        const response = await api.get<EntityAttribute[]>(
            `/dorks/entities/${entityId}/attributes/`
        );
        return response.data;
    },

    async createEntityAttribute(
        entityId: string | number,
        data: Partial<EntityAttribute>
    ): Promise<EntityAttribute> {
        const response = await api.post<EntityAttribute>(
            `/dorks/entities/${entityId}/attributes/`,
            data
        );
        return response.data;
    },

    async updateAttribute(
        id: number,
        data: Partial<EntityAttribute>
    ): Promise<EntityAttribute> {
        const response = await api.put<EntityAttribute>(
            `/dorks/entity-attributes/${id}/`,
            data
        );
        return response.data;
    },

    async deleteAttribute(id: number): Promise<void> {
        await api.delete(`/dorks/entity-attributes/${id}/`);
    },

    // Entity Search Templates
    async getSearchTemplates(params?: {
        entity_type?: number;
        category?: string;
    }): Promise<EntitySearchTemplate[]> {
        const response = await api.get<EntitySearchTemplate[]>(
            '/dorks/entity-search-templates/',
            { params }
        );
        return response.data;
    },

    async getSearchTemplate(id: number): Promise<EntitySearchTemplate> {
        const response = await api.get<EntitySearchTemplate>(
            `/dorks/entity-search-templates/${id}/`
        );
        return response.data;
    },

    // Entity Search Sessions
    async getSearchSessions(params?: {
        page?: number;
        entity?: number;
        status?: string;
    }): Promise<PaginatedResponse<EntitySearchSession>> {
        const response = await api.get<PaginatedResponse<EntitySearchSession>>(
            '/dorks/entity-search-sessions/',
            { params }
        );
        return response.data;
    },

    async getSearchSession(id: number): Promise<EntitySearchSession> {
        const response = await api.get<EntitySearchSession>(
            `/dorks/entity-search-sessions/${id}/`
        );
        return response.data;
    },

    async createSearchSession(
        data: Partial<EntitySearchSession>
    ): Promise<EntitySearchSession> {
        const response = await api.post<EntitySearchSession>(
            '/dorks/entity-search-sessions/',
            data
        );
        return response.data;
    },

    async getSearchSessionResults(id: number): Promise<EntitySearchResult[]> {
        const response = await api.get<EntitySearchResult[]>(
            `/dorks/entity-search-sessions/${id}/results/`
        );
        return response.data;
    },

    async getEntitySearchSessions(entityId: string | number): Promise<EntitySearchSession[]> {
        const response = await api.get<EntitySearchSession[]>(
            `/dorks/entities/${entityId}/search_sessions/`
        );
        return response.data;
    },

    // Entity Relationships
    async getEntityRelationships(
        entityId: string | number
    ): Promise<{
        outgoing: EntityRelationship[];
        incoming: EntityRelationship[];
    }> {
        const response = await api.get(`/dorks/entities/${entityId}/relationships/`);
        return response.data;
    },

    async createRelationship(
        data: Partial<EntityRelationship>
    ): Promise<EntityRelationship> {
        const response = await api.post<EntityRelationship>(
            '/dorks/entity-relationships/',
            data
        );
        return response.data;
    },

    async updateRelationship(
        id: number,
        data: Partial<EntityRelationship>
    ): Promise<EntityRelationship> {
        const response = await api.put<EntityRelationship>(
            `/dorks/entity-relationships/${id}/`,
            data
        );
        return response.data;
    },

    async deleteRelationship(id: number): Promise<void> {
        await api.delete(`/dorks/entity-relationships/${id}/`);
    },

    // Entity Notes
    async getEntityNotes(entityId: string | number): Promise<EntityNote[]> {
        const response = await api.get<EntityNote[]>(
            `/dorks/entities/${entityId}/notes/`
        );
        return response.data;
    },

    async createNote(data: Partial<EntityNote>): Promise<EntityNote> {
        const response = await api.post<EntityNote>('/dorks/entity-notes/', data);
        return response.data;
    },

    async updateNote(id: number, data: Partial<EntityNote>): Promise<EntityNote> {
        const response = await api.put<EntityNote>(`/dorks/entity-notes/${id}/`, data);
        return response.data;
    },

    async deleteNote(id: number): Promise<void> {
        await api.delete(`/dorks/entity-notes/${id}/`);
    },
};
