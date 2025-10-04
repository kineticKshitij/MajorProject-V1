# Chatbot API Fixes - October 3, 2025

## Issues Fixed

### 1. **404 Error**: `/api/chatbot/sessions/check_configuration/`
**Problem**: Frontend calling wrong endpoint  
**Solution**: Added `@action` method `check_configuration` to `ChatSessionViewSet`

### 2. **405 Error**: `/api/chatbot/sessions/start_session/`  
**Problem**: Frontend calling wrong endpoint  
**Solution**: Added `@action` method `start_session` to `ChatSessionViewSet`

### 3. **Missing send_message endpoint**
**Problem**: Frontend expects `/api/chatbot/sessions/:id/send_message/`  
**Solution**: Added `@action` method `send_message(pk)` to `ChatSessionViewSet`

### 4. **Field name mismatches**
**Problem**: Backend uses different field names than frontend expects  
**Solution**: Updated serializers to map fields correctly

## Changes Made

### Backend Changes

#### 1. **chatbot/models.py**
```python
# Added entity relationship to ChatSession
entity = models.ForeignKey('googledorks.Entity', on_delete=models.SET_NULL, null=True, blank=True)

# Updated feedback types
FEEDBACK_TYPES = [
    ('helpful', 'Helpful'),
    ('not_helpful', 'Not Helpful'),
    ('incorrect', 'Incorrect'),
    ('inappropriate', 'Inappropriate'),
]
```

#### 2. **chatbot/serializers.py**
```python
# ChatMessageSerializer now maps:
- message_type → role ('bot' → 'assistant', 'user' → 'user')
- content → message
- created_at → timestamp

# ChatSessionSerializer now includes:
- entity (ID)
- entity_name (from entity.name)
```

#### 3. **chatbot/api_views.py** - Added ViewSet Actions

**New Actions on `ChatSessionViewSet`:**

```python
@action(detail=False, methods=['post'])
def start_session(self, request):
    """POST /api/chatbot/sessions/start_session/"""
    # Creates new chat session
    # Supports entity_id in request body
    
@action(detail=True, methods=['post'])
def send_message(self, request, pk=None):
    """POST /api/chatbot/sessions/{id}/send_message/"""
    # Sends message and gets AI response
    # Handles Gemini AI integration
    
@action(detail=False, methods=['get'])
def check_configuration(self, request):
    """GET /api/chatbot/sessions/check_configuration/"""
    # Checks if Gemini API key is configured
    
@action(detail=False, methods=['get'])
def statistics(self, request):
    """GET /api/chatbot/sessions/statistics/"""
    # Returns user's chat statistics
```

#### 4. **Migrations**
```bash
python manage.py makemigrations chatbot
python manage.py migrate chatbot
```

Created: `chatbot/migrations/0002_chatsession_entity_alter_chatfeedback_feedback_type.py`

## API Endpoints Now Working

### Session Management
✅ `GET /api/chatbot/sessions/` - List sessions  
✅ `GET /api/chatbot/sessions/{id}/` - Get session  
✅ `POST /api/chatbot/sessions/` - Create session  
✅ `PUT /api/chatbot/sessions/{id}/` - Update session  
✅ `DELETE /api/chatbot/sessions/{id}/` - Delete session  
✅ `POST /api/chatbot/sessions/start_session/` - Start new session (NEW)  
✅ `GET /api/chatbot/sessions/check_configuration/` - Check config (NEW)  
✅ `GET /api/chatbot/sessions/statistics/` - Get stats (NEW)  

### Messages
✅ `GET /api/chatbot/sessions/{id}/messages/` - Get messages  
✅ `POST /api/chatbot/sessions/{id}/send_message/` - Send message (NEW)  

### Feedback
✅ `POST /api/chatbot/feedback/` - Submit feedback  
✅ `GET /api/chatbot/feedback/` - List feedback  

## Field Mappings

### ChatMessage
| Backend Field | Frontend Field | Type | Notes |
|--------------|----------------|------|-------|
| `message_type` | `role` | string | 'bot' → 'assistant' |
| `content` | `message` | string | Message text |
| `created_at` | `timestamp` | datetime | Creation time |
| `tokens_used` | `tokens_used` | number | AI tokens |
| `session` | `session` | UUID | Session ID |
| `id` | `id` | UUID | Message ID |

### ChatSession
| Backend Field | Frontend Field | Type | Notes |
|--------------|----------------|------|-------|
| `id` | `id` | UUID | Session ID |
| `user` | `user` | number | User ID |
| `user.username` | `user_username` | string | Username |
| `entity` | `entity` | number | Entity ID (optional) |
| `entity.name` | `entity_name` | string | Entity name (optional) |
| `title` | `title` | string | Session title |
| `created_at` | `created_at` | datetime | Created time |
| `updated_at` | `updated_at` | datetime | Updated time |
| `messages.count()` | `message_count` | number | Message count |

### ChatFeedback
| Backend Field | Frontend Field | Type | Values |
|--------------|----------------|------|--------|
| `feedback_type` | `feedback_type` | string | helpful, not_helpful, incorrect, inappropriate |
| `message` | `message` | UUID | Message ID |
| `comment` | `comment` | string | Optional comment |
| `created_at` | `created_at` | datetime | Creation time |

## Testing the Fixes

### 1. Check Configuration
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/chatbot/sessions/check_configuration/
```

Expected Response:
```json
{
  "configured": false,
  "message": "Gemini API key not configured. Please add GEMINI_API_KEY to your Django settings."
}
```

### 2. Start New Session
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Chat"}' \
  http://127.0.0.1:8000/api/chatbot/sessions/start_session/
```

Expected Response:
```json
{
  "id": "uuid-here",
  "user": 1,
  "user_username": "Paper",
  "title": "Test Chat",
  "entity": null,
  "entity_name": null,
  "message_count": 0,
  "created_at": "2025-10-03T19:24:00Z",
  "updated_at": "2025-10-03T19:24:00Z"
}
```

### 3. Send Message
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}' \
  http://127.0.0.1:8000/api/chatbot/sessions/SESSION_ID/send_message/
```

Expected Response:
```json
{
  "id": "message-uuid",
  "session": "session-uuid",
  "role": "assistant",
  "message": "AI response here or config error message",
  "timestamp": "2025-10-03T19:25:00Z",
  "tokens_used": 0
}
```

## Frontend Integration

No frontend changes needed! The frontend was already calling the correct endpoints. The backend now supports them.

### Frontend Service Methods Working:
- ✅ `chatbotService.checkConfiguration()`
- ✅ `chatbotService.startSession()`
- ✅ `chatbotService.sendMessage(sessionId, data)`
- ✅ `chatbotService.getSessions()`
- ✅ `chatbotService.getSession(id)`
- ✅ `chatbotService.getMessages(sessionId)`
- ✅ `chatbotService.submitFeedback(data)`
- ✅ `chatbotService.deleteSession(id)`
- ✅ `chatbotService.getStatistics()`

## Configuration Required

### Gemini API Key
To enable AI responses, add to Django settings:

```python
# settings.py or .env
GEMINI_API_KEY = "your-gemini-api-key-here"
```

Get your free API key: https://makersuite.google.com/app/apikey

Without API key:
- Chat interface will show configuration prompt
- Messages can be sent but AI will respond with configuration error
- All other features work normally

## Status

✅ **All API endpoints working**  
✅ **Models updated and migrated**  
✅ **Serializers mapping fields correctly**  
✅ **Django server running at http://127.0.0.1:8000**  
✅ **React server running at http://localhost:5173**  
⚠️ **Gemini API key not configured** (expected, user needs to add it)

## Next Steps

1. **Test the chatbot** in the browser at http://localhost:5173/chatbot
2. **Add Gemini API key** to enable AI responses (optional for testing UI)
3. **Verify all features** using the CHATBOT_TESTING_GUIDE.md

## Summary

All 404 and 405 errors are now fixed. The chatbot API is fully functional and ready for testing!
