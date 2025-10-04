// User types
export interface User {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    date_joined: string;
}

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    password2: string;
    first_name?: string;
    last_name?: string;
}

export interface AuthTokens {
    access: string;
    refresh: string;
}

export interface AuthResponse {
    user: User;
    tokens: AuthTokens;
}

// Dork types
export interface DorkCategory {
    id: number;
    name: string;
    description: string;
    color: string;
    created_at: string;
    dork_count?: number;
}

export interface GoogleDork {
    id: number;
    title: string;
    query: string;
    description: string;
    category: number;
    category_name: string;
    category_data?: DorkCategory;
    tags: string;
    risk_level: 'low' | 'medium' | 'high' | 'critical';
    difficulty: 'beginner' | 'intermediate' | 'advanced';
    difficulty_level?: 'beginner' | 'intermediate' | 'advanced'; // Alias for difficulty
    example_usage?: string;
    notes?: string;
    is_active: boolean;
    usage_count: number;
    execution_count?: number; // Added execution_count
    created_by?: number;
    created_by_username?: string;
    created_at: string;
    updated_at: string;
    is_bookmarked?: boolean;
    supports_entities?: boolean;
    entity_placeholders?: string[];
}

export interface SearchResult {
    id: number;
    session: number;
    dork: number;
    dork_data?: GoogleDork;
    title: string;
    url: string;
    snippet: string;
    position: number;
    is_relevant: boolean;
    notes?: string;
    created_at: string;
}

export interface SearchSession {
    id: number;
    name: string;
    description?: string;
    user: number;
    user_username: string;
    is_active: boolean;
    result_count: number;
    created_at: string;
    updated_at: string;
}

export interface DorkBookmark {
    id: number;
    user: number;
    user_username: string;
    dork: number;
    dork_data: GoogleDork;
    notes?: string;
    created_at: string;
}

// Entity types
export interface EntityType {
    id: number;
    name: string;
    display_name?: string;
    description: string;
    icon?: string;
    color: string;
    required_fields: string[];
    optional_fields: string[];
    created_at: string;
    entity_count?: number;
}

export interface Entity {
    id: number;
    name: string;
    entity_type: number;
    entity_type_name: string;
    entity_type_data?: EntityType;
    aliases?: string[];
    description?: string;
    industry?: string;
    location?: string;
    founded_date?: string;
    website?: string;
    domains?: string[];
    social_media?: Record<string, string>;
    tags: string | string[];  // Can be string or array
    status: 'active' | 'completed' | 'on_hold' | 'archived';
    priority: 'low' | 'medium' | 'high' | 'critical';
    created_by: number;
    created_by_username: string;
    created_at: string;
    updated_at: string;
    last_researched?: string;
    search_count?: number;
    results_found?: number;
    attribute_count?: number;
    search_session_count?: number;
    relationship_count?: number;
}

export interface EntityAttribute {
    id: number;
    entity: number;
    attribute_name: string;
    attribute_value: string;
    attribute_type: 'text' | 'url' | 'email' | 'phone' | 'date' | 'number' | 'json';
    is_verified: boolean;
    is_public?: boolean;
    source?: string;
    confidence?: number;
    created_at: string;
    updated_at: string;
}

export interface EntitySearchTemplate {
    id: number;
    name: string;
    description: string;
    entity_type: number;
    entity_type_name: string;
    template_query: string;
    category: string;
    risk_level: 'low' | 'medium' | 'high' | 'critical';
    expected_results?: string;
    usage_tips?: string;
    is_active: boolean;
    created_at: string;
}

export interface EntitySearchSession {
    id: number;
    entity: number;
    entity_name: string;
    search_template: number;
    template_name: string;
    session_name?: string;
    executed_query: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    result_count: number;
    user: number;
    user_username: string;
    started_at: string;
    completed_at?: string;
}

export interface EntitySearchResult {
    id: number;
    search_session: number;
    title: string;
    url: string;
    snippet: string;
    position: number;
    relevance_score?: number;
    is_verified: boolean;
    notes?: string;
    created_at: string;
}

export interface EntityRelationship {
    id: number;
    from_entity: number;
    from_entity_name: string;
    to_entity: number;
    to_entity_name: string;
    relationship_type: string;
    description?: string;
    confidence?: number;
    source?: string;
    start_date?: string;
    end_date?: string;
    is_active?: boolean;
    strength: number;
    is_verified: boolean;
    created_by: number;
    created_by_username: string;
    created_at: string;
    updated_at?: string;
}

export interface EntityNote {
    id: number;
    entity: number;
    title: string;
    content: string;
    note_type: 'general' | 'finding' | 'vulnerability' | 'contact' | 'technical';
    tags: string;
    is_important: boolean;
    created_by: number;
    created_by_username: string;
    created_at: string;
    updated_at: string;
}

// Chatbot types
export interface ChatSession {
    id: number;
    user: number;
    user_username: string;
    title: string;
    entity?: number;
    entity_name?: string;
    message_count: number;
    created_at: string;
    updated_at: string;
}

export interface ChatMessage {
    id: number;
    session: number;
    role: 'user' | 'assistant';
    message: string;
    timestamp: string;
    tokens_used?: number;
    entity_context?: any;
}

export interface SendMessageData {
    message: string;
    entity_id?: number;
}

export interface ChatFeedback {
    id: number;
    message: number;
    feedback_type: 'helpful' | 'not_helpful' | 'incorrect' | 'inappropriate';
    comment?: string;
    created_at: string;
}

// API Response types
export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

export interface ApiError {
    detail?: string;
    message?: string;
    [key: string]: any;
}
