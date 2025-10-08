// Entity Management Types

// Entity Type Enums
export type EntityTypeName =
    | 'company'
    | 'person'
    | 'organization'
    | 'government'
    | 'educational'
    | 'domain'
    | 'project'
    | 'event';

export type PriorityLevel = 'low' | 'medium' | 'high' | 'critical';
export type EntityStatus = 'active' | 'completed' | 'on_hold' | 'archived';
export type ConfidenceLevel = 'low' | 'medium' | 'high' | 'verified';
export type AttributeValueType = 'text' | 'number' | 'date' | 'url' | 'email' | 'phone';
export type NoteType = 'observation' | 'finding' | 'hypothesis' | 'todo' | 'warning' | 'contact';
export type RelationshipType =
    | 'parent_company'
    | 'subsidiary'
    | 'partner'
    | 'competitor'
    | 'supplier'
    | 'customer'
    | 'employee'
    | 'founder'
    | 'investor'
    | 'acquired_by'
    | 'acquired'
    | 'related';

// Entity Type Interface
export interface EntityType {
    id: number;
    name: EntityTypeName;
    display_name: string;
    description: string;
    icon: string;
    color: string;
    is_active: boolean;
    created_at: string;
}

// Entity Attribute Interface
export interface EntityAttribute {
    id: number;
    entity: string;  // UUID
    key: string;
    value: string;
    value_type: AttributeValueType;
    is_public: boolean;
    source: string;
    confidence: ConfidenceLevel;
    created_at: string;
    updated_at: string;
}

// Entity Interface
export interface Entity {
    id: string;  // UUID
    name: string;
    entity_type: EntityType;
    entity_type_id?: number;
    aliases: string[];
    description: string;
    industry: string;
    location: string;
    founded_date?: string;
    website: string;
    domains: string[];
    social_media: Record<string, string>;
    priority: PriorityLevel;
    status: EntityStatus;
    tags: string[];
    created_by: number;
    created_by_username?: string;
    assigned_to: number[];
    assigned_to_usernames?: string[];
    created_at: string;
    updated_at: string;
    last_researched?: string;
    search_count: number;
    results_found: number;
    attributes?: EntityAttribute[];
    notes_count?: number;
    relationships_count?: number;
}

// Entity List Item (lightweight)
export interface EntityListItem {
    id: string;
    name: string;
    entity_type: {
        id: number;
        name: EntityTypeName;
        display_name: string;
        icon: string;
        color: string;
    };
    description: string;
    industry: string;
    location: string;
    website: string;
    priority: PriorityLevel;
    status: EntityStatus;
    tags: string[];
    created_by_username: string;
    created_at: string;
    updated_at: string;
    last_researched?: string;
    search_count: number;
    results_found: number;
}

// Create Entity Input
export interface CreateEntity {
    name: string;
    entity_type_id: number;
    aliases?: string[];
    description?: string;
    industry?: string;
    location?: string;
    founded_date?: string;
    website?: string;
    domains?: string[];
    social_media?: Record<string, string>;
    priority?: PriorityLevel;
    status?: EntityStatus;
    tags?: string[];
}

// Update Entity Input
export interface UpdateEntity extends Partial<CreateEntity> {
    assigned_to?: number[];
}

// Entity Relationship Interface
export interface EntityRelationship {
    id: number;
    from_entity: string;  // UUID
    from_entity_name?: string;
    to_entity: string;  // UUID
    to_entity_name?: string;
    to_entity_details?: EntityListItem;
    relationship_type: RelationshipType;
    description: string;
    confidence: ConfidenceLevel;
    source: string;
    start_date?: string;
    end_date?: string;
    is_active: boolean;
    created_by?: number;
    created_at: string;
    updated_at: string;
}

// Entity Note Interface
export interface EntityNote {
    id: number;
    entity: string;  // UUID
    title: string;
    content: string;
    note_type: NoteType;
    priority: PriorityLevel;
    tags: string[];
    is_private: boolean;
    created_by: number;
    created_by_username?: string;
    created_at: string;
    updated_at: string;
}

// Entity Search Template Interface
export interface EntitySearchTemplate {
    id: number;
    entity_type: number;
    entity_type_name?: string;
    name: string;
    description: string;
    query_template: string;
    category: string;
    risk_level: string;
    difficulty: string;
    is_active: boolean;
    usage_count: number;
    created_by?: number;
    created_at: string;
    updated_at: string;
}

// Entity Search Session Interface
export interface EntitySearchSession {
    id: string;  // UUID
    entity: string;  // UUID
    entity_name?: string;
    name: string;
    description: string;
    search_templates: number[];
    auto_execute: boolean;
    save_results: boolean;
    notify_completion: boolean;
    created_by: number;
    created_at: string;
    started_at?: string;
    completed_at?: string;
    total_searches: number;
    total_results: number;
    interesting_results: number;
}

// Entity Search Result Interface
export interface EntitySearchResult {
    id: string;  // UUID
    entity: string;  // UUID
    session?: string;  // UUID
    template: number;
    template_name?: string;
    title: string;
    url: string;
    snippet: string;
    domain: string;
    relevance_score: number;
    is_interesting: boolean;
    is_verified: boolean;
    contains_sensitive_info: boolean;
    extracted_info: Record<string, unknown>;
    tags: string[];
    notes: string;
    found_at: string;
    last_verified?: string;
    verification_status: 'not_checked' | 'accessible' | 'requires_auth' | 'not_found' | 'blocked';
}

// Filter Interfaces
export interface EntityFilters {
    search?: string;
    entity_type?: EntityTypeName;
    status?: EntityStatus;
    priority?: PriorityLevel;
    tags?: string[];
    created_by?: number;
    assigned_to?: number;
}

// Paginated Response
export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

// Statistics
export interface EntityStatistics {
    total_entities: number;
    active_entities: number;
    completed_entities: number;
    by_type: Record<EntityTypeName, number>;
    by_priority: Record<PriorityLevel, number>;
    by_status: Record<EntityStatus, number>;
    total_searches: number;
    total_results: number;
}
