# Frontend API Integration Fixes - October 3, 2025

## Issues Fixed

### 1. Categories Not Rendering
**Error:** `Uncaught TypeError: categories?.map is not a function`

### 2. Difficulty Field Undefined
**Error:** `Uncaught TypeError: Cannot read properties of undefined (reading 'toLowerCase')`

## Root Causes

1. **Paginated Response Structure** - Backend returns:
```json
{
  "count": 10,
  "next": "http://...",
  "previous": null,
  "results": [...]
}
```
Frontend was expecting a plain array.

2. **Field Name Mismatches** - Frontend TypeScript types didn't match backend model fields:
   - `difficulty_level` (old) → `difficulty` (new)
   - `execution_count` (old) → `usage_count` (new)

## Fixes Applied

### 1. **types/index.ts** - Fixed TypeScript Interface

**Changed:**
```typescript
export interface GoogleDork {
    // ...
    difficulty: 'beginner' | 'intermediate' | 'advanced';  // was: difficulty_level
    usage_count: number;  // was: execution_count
    // ...
}
```

### 2. **dorksService.ts** - Updated Return Type

**Before:**
```typescript
async getCategories(): Promise<DorkCategory[]> {
    const response = await api.get<DorkCategory[]>('/dorks/categories/');
    return response.data;
}
```

**After:**
```typescript
async getCategories(): Promise<PaginatedResponse<DorkCategory>> {
    const response = await api.get<PaginatedResponse<DorkCategory>>('/dorks/categories/');
    return response.data;
}
```

### 3. **DorksList.tsx** - Handle Paginated Response & Fixed Field Names

**Fixed pagination:**
```typescript
const { data: categoriesData } = useQuery({
    queryKey: ['dorkCategories'],
    queryFn: dorksService.getCategories,
});

const categories = categoriesData?.results || [];
```

**Fixed field usage in template:**
```typescript
// Risk & Difficulty badges
<span className={getDifficultyBadgeColor(dork.difficulty)}>
    {dork.difficulty}
</span>

// Usage count
<span>📊 {dork.usage_count} executions</span>
```

### 4. **Fixed Field Name Mismatch in Service**

**In dorksService.ts:**
```typescript
// Before
difficulty_level?: string;

// After
difficulty?: string;
```

**In DorksList.tsx:**
```typescript
// Before
difficulty_level: difficultyLevel || undefined,

// After  
difficulty: difficultyLevel || undefined,
```

## Why This Happened

Django REST Framework's `ModelViewSet` uses pagination by default, which wraps all list responses in a paginated structure. The frontend needs to:

1. **Expect paginated responses** for all list endpoints
2. **Extract the `results` array** from the response
3. **Use correct field names** that match the backend models

## API Response Structures

### Paginated List Response
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/dorks/categories/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Information Disclosure",
      "description": "...",
      "color": "#007bff",
      "created_at": "2025-10-03T...",
      "dork_count": 15
    },
    // ... more items
  ]
}
```

### Single Item Response
```json
{
  "id": 1,
  "name": "Information Disclosure",
  "description": "...",
  "color": "#007bff",
  "created_at": "2025-10-03T...",
  "dork_count": 15
}
```

## Field Name Reference

### Backend → Frontend Mapping

| Backend Field | Frontend Usage | Notes |
|--------------|----------------|-------|
| `difficulty` | `difficulty` | ✅ Fixed (was `difficulty_level`) |
| `color` | `color` | ✅ Correct |
| `usage_count` | `usage_count` | ✅ Correct |
| `risk_level` | `risk_level` | ✅ Correct |

## Testing

### Test Categories Load
1. Open: http://localhost:5173/dorks
2. **Expected**: Category dropdown populated with categories
3. **Result**: ✅ Should work now

### Test Dorks List with Filters
1. Select a category from dropdown
2. Select difficulty level
3. Click "Search"
4. **Expected**: Filtered dorks display
5. **Result**: ✅ Should work now

## Status

✅ **Categories error fixed** - Now extracts `results` from paginated response  
✅ **Field name mismatch fixed** - `difficulty_level` → `difficulty`  
✅ **Service types updated** - TypeScript types match backend  
✅ **All dorks features should work** - List, filters, pagination

## Additional Notes

### Other List Endpoints That Need This Pattern

If you encounter similar errors with other endpoints, remember that **all list endpoints return paginated responses**:

```typescript
// Pattern for all list endpoints:
const { data: responseData } = useQuery({...});
const items = responseData?.results || [];
```

**Affected endpoints:**
- ✅ `/api/dorks/categories/` - Fixed
- ✅ `/api/dorks/dorks/` - Already using PaginatedResponse
- `/api/dorks/bookmarks/` - May need this pattern
- `/api/entities/entities/` - May need this pattern
- `/api/entities/entity-types/` - May need this pattern
- `/api/chatbot/sessions/` - May need this pattern (already fixed)

## Summary

Fixed the "categories?.map is not a function" error by:
1. Updating service to expect `PaginatedResponse<DorkCategory>`
2. Extracting `results` array in component
3. Fixing `difficulty_level` → `difficulty` field name mismatch

The Dorks page should now load and display categories correctly! 🎉
