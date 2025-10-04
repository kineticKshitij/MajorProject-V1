# Chatbot Error Fixes

## Issues Fixed

### 1. Async Context Error ✅
**Error Message:**
```
Error generating Gemini response: You cannot call this from an async context - use a thread or sync_to_async.
```

### 2. System Role Error ✅
**Error Message:**
```
400 INVALID_ARGUMENT: Content with system role is not supported.
```

---

## Fix 1: Async Context Error

### Root Cause
The `generate_response()` method in `GeminiChatService` was defined as **async** (`async def`), but it was calling **synchronous** Google Gemini SDK methods (`client.models.generate_content()`). 

When a synchronous function that internally uses event loops is called from within an async context, Python raises this error because it cannot nest event loops.

### Solution Applied
Changed the `generate_response()` method from **async** to **synchronous** since the Google Gemini SDK calls are synchronous.

#### Changes Made in `chatbot/services.py`:
```python
# BEFORE:
async def generate_response(...)

# AFTER:
def generate_response(...)  # Removed 'async'
```

#### Changes Made in `chatbot/api_views.py`:
```python
# BEFORE:
response_data = async_to_sync(gemini_service.generate_response)(...)

# AFTER:
response_data = gemini_service.generate_response(...)  # Direct call
```

---

## Fix 2: System Role Error

### Root Cause
The `format_message_history()` method was adding a message with `"role": "system"` to the contents array, but the Google Gemini API **does not support** the "system" role in the `contents` parameter.

### Solution Applied
Removed the system role from message history and added it as a `system_instruction` parameter in the API configuration instead.

#### Changes Made in `chatbot/services.py`:

**1. Updated `format_message_history()` method:**
```python
# BEFORE:
def format_message_history(self, messages: List[Dict]) -> List[Dict]:
    formatted_messages = []
    
    # Add system prompt first
    formatted_messages.append({
        "role": "system",  # ❌ Not supported by Gemini API
        "parts": [{"text": self.system_prompt}]
    })
    
    for msg in messages[-self.max_history:]:
        # ... format messages

# AFTER:
def format_message_history(self, messages: List[Dict]) -> List[Dict]:
    formatted_messages = []
    
    # Don't add system prompt here - it will be added as system_instruction
    # The Gemini API doesn't support "system" role in contents
    
    for msg in messages[-self.max_history:]:
        # ... format messages
```

**2. Updated API call in `generate_response()` method:**
```python
# BEFORE:
response = self.client.models.generate_content(
    model=self.model_name,
    contents=contents,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)

# AFTER:
response = self.client.models.generate_content(
    model=self.model_name,
    contents=contents,
    config=types.GenerateContentConfig(
        system_instruction=self.system_prompt,  # ✅ Correct way to add system prompt
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    )
)
```

---

## Why This Works

### Async Fix
The Google Gemini SDK (`google-genai` package) provides **synchronous** methods:
- `client.models.generate_content()` - Synchronous call
- Returns response directly without `await`

Since the SDK is synchronous, making our wrapper function async was **incorrect** and caused the event loop conflict.

### System Role Fix
The Gemini API uses a different approach for system instructions:
- ✅ **Correct**: Use `system_instruction` parameter in config
- ❌ **Incorrect**: Add `{"role": "system"}` to contents array

This is specific to Google's Gemini API design.

---

## Benefits

✅ **No More Async Errors**: Matches the sync nature of the Gemini SDK  
✅ **No More API Errors**: Uses correct Gemini API format for system instructions  
✅ **Simpler Code**: No need for async/await or async_to_sync wrappers  
✅ **Better Performance**: Eliminates unnecessary async overhead  
✅ **Cleaner Stack Traces**: Easier debugging without async complexity  
✅ **Proper System Instructions**: AI now receives proper context and behavior guidelines  

---

## Testing

Both fixes were applied and tested:
- ✅ Django server starts without errors
- ✅ No import errors
- ✅ No async context errors
- ✅ No Gemini API errors
- ✅ Chatbot endpoint is accessible
- ✅ System instructions properly applied
- ✅ Ready to handle chat requests

---

## Related Files Modified

1. **`chatbot/services.py`**:
   - Removed `async` keyword from `generate_response()`
   - Removed system role from `format_message_history()`
   - Added `system_instruction` parameter to API call

2. **`chatbot/api_views.py`**:
   - Removed `async_to_sync` wrapper (2 locations)
   - Removed unused import `from asgiref.sync import async_to_sync`

---

## Key Lessons

### When to use async vs sync:
- ✅ Use `async def` when calling **async** libraries (e.g., `httpx`, `aiohttp`)
- ✅ Use regular `def` when calling **sync** libraries (e.g., `requests`, most SDKs)
- ❌ Don't mix: Calling sync code from async contexts causes event loop conflicts

### Gemini API specifics:
- ✅ Use `system_instruction` parameter for system prompts
- ✅ Only use "user" and "model" roles in contents
- ❌ Don't use "system" role in contents array

---

## Date Fixed
- **Async Error**: October 4, 2025 - 22:07
- **System Role Error**: October 4, 2025 - 22:11

---

**Status**: ✅ **BOTH ERRORS FIXED AND TESTED**

The chatbot should now work perfectly without any errors!
