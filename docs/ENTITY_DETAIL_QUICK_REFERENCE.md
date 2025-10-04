# 🎯 EntityDetail Quick Reference

## File Location
```
frontend/src/components/EntityDetail.tsx
```

## Route
```
/entities/:id
```

## Usage
```typescript
import EntityDetail from './components/EntityDetail';

<Route path="/entities/:id" element={
    <ProtectedRoute><EntityDetail /></ProtectedRoute>
} />
```

## Features

### 5 Tabs
1. **📋 Overview** - Complete entity profile (basic info, online presence, metadata, stats)
2. **🏷️ Attributes** - Custom key-value pairs (can delete)
3. **🔗 Relationships** - Entity connections (clickable navigation)
4. **📝 Notes** - Research findings (can delete)
5. **🔍 Search Results** - Dork results (filter by verified)

### Actions
- ✏️ **Edit** - Placeholder (to be implemented)
- 🗑️ **Delete Entity** - Works with confirmation
- 🗑️ **Delete Attribute** - Works per attribute
- 🗑️ **Delete Note** - Works per note
- ← **Back** - Return to entities list
- 🔗 **Navigate** - Click related entities

### Data Loading
- **Main entity**: Always loaded
- **Attributes**: Loaded when Attributes tab active
- **Relationships**: Loaded when Relationships tab active
- **Notes**: Loaded when Notes tab active
- **Results**: Placeholder (empty state)

### Empty States
All tabs show friendly empty states with:
- Large emoji icon
- "No X yet" message  
- Helpful action hint

### Styling
- Color-coded priority badges (gray/blue/orange/red)
- Color-coded status badges (green/blue/yellow/gray)
- Entity type colors from API
- Hover effects on cards
- Responsive grid layouts

## API Endpoints Used
- `GET /api/dorks/entities/:id/` - Main details
- `GET /api/dorks/entities/:id/attributes/` - Attributes list
- `GET /api/dorks/entities/:id/relationships/` - Relationships
- `GET /api/dorks/entities/:id/notes/` - Notes list
- `DELETE /api/dorks/entities/:id/` - Delete entity
- `DELETE /api/dorks/entity-attributes/:id/` - Delete attribute
- `DELETE /api/dorks/entity-notes/:id/` - Delete note

## Props
None (uses URL params via `useParams()`)

## Dependencies
- React Router (`useParams`, `useNavigate`, `Link`)
- React Query (`useQuery`, `useMutation`, `useQueryClient`)
- entitiesService (all API calls)
- Types from `types/index.ts`

## Testing
1. Go to http://localhost:5173/entities
2. Click any entity card
3. Test all 5 tabs
4. Try delete operations
5. Navigate to related entities
6. Test back button

## Next Steps
- [ ] Build NewEntity form
- [ ] Build EditEntity form  
- [ ] Add Attribute form within tab
- [ ] Add Relationship form within tab
- [ ] Add Note form within tab

## Status
✅ COMPLETE - Production Ready

