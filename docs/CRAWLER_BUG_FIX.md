# Social Media Crawler - Bug Fix Documentation

## Issue: 400 Bad Request on Create Crawl Job

**Date**: October 3, 2025  
**Status**: ✅ RESOLVED

---

## Problem Description

When attempting to create a new crawl job through the frontend, the API returned a `400 Bad Request` error:

```
Bad Request: /api/crawler/jobs/
[03/Oct/2025 20:35:59] "POST /api/crawler/jobs/ HTTP/1.1" 400 52
```

---

## Root Cause Analysis

The issue was caused by a **validation mismatch** between the frontend and backend:

### Backend Issues:
1. **Required Field**: The `CrawlJob` model defined `target_username` as a **required** field (no `blank=True`)
2. **Strict Validation**: The `CreateCrawlJobSerializer` rejected empty strings for `target_username`
3. **Inflexible API**: The API didn't support providing only a `target_url` without a `target_username`

### Frontend Issues:
1. **Empty String Submission**: The form was sending empty strings (`''`) for optional fields
2. **No Data Cleaning**: The form submitted all fields including empty ones
3. **Poor Error Handling**: The user couldn't see what validation failed

---

## Solution Implemented

### 1. Backend Fixes

#### A. Updated Model (`socialcrawler/models.py`)
Made `target_username` optional in the database:

```python
# Before
target_username = models.CharField(max_length=255, help_text="Username or handle to crawl")

# After
target_username = models.CharField(max_length=255, blank=True, help_text="Username or handle to crawl")
```

**Migration Created**: `socialcrawler/migrations/0002_alter_crawljob_target_username.py`

#### B. Enhanced Serializer (`socialcrawler/serializers.py`)
Updated `CreateCrawlJobSerializer` with smarter validation:

```python
def validate(self, data):
    """Validate that at least username or URL is provided"""
    target_username = data.get('target_username', '').strip()
    target_url = data.get('target_url', '').strip()
    
    # Require at least one
    if not target_username and not target_url:
        raise serializers.ValidationError({
            'target_username': "Either target_username or target_url must be provided"
        })
    
    # Auto-extract username from URL if not provided
    if target_url and not target_username:
        import re
        username_match = re.search(r'/([^/]+?)/?$', target_url.rstrip('/'))
        if username_match:
            data['target_username'] = username_match.group(1)
    
    return data

def validate_target_username(self, value):
    """Validate username format"""
    if not value or not value.strip():
        return ''  # Allow empty strings now
    return value.lstrip('@').strip()  # Clean @ symbol
```

**Key Improvements**:
- ✅ Accepts either `target_username` OR `target_url`
- ✅ Auto-extracts username from URL (e.g., `https://github.com/torvalds` → `torvalds`)
- ✅ Strips `@` symbols (e.g., `@torvalds` → `torvalds`)
- ✅ Flexible validation with clear error messages

---

### 2. Frontend Fixes

#### Updated Form Handler (`frontend/src/components/NewCrawlJob.tsx`)
Improved data cleaning before API submission:

```typescript
const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate
    if (!formData.target_username?.trim() && !formData.target_url?.trim()) {
        alert('Please enter a username or URL');
        return;
    }

    // Clean up data - remove empty fields
    const cleanData: CreateCrawlJob = {
        platform: formData.platform,
        crawl_posts: formData.crawl_posts ?? true,
        crawl_followers: formData.crawl_followers ?? false,
        crawl_following: formData.crawl_following ?? false,
        max_posts: formData.max_posts ?? 50,
        max_followers: formData.max_followers ?? 100,
    };

    // Only include non-empty values
    if (formData.target_username?.trim()) {
        cleanData.target_username = formData.target_username.trim();
    }
    if (formData.target_url?.trim()) {
        cleanData.target_url = formData.target_url.trim();
    }
    if (formData.entity) {
        cleanData.entity = formData.entity;
    }

    createJobMutation.mutate(cleanData);
};
```

**Key Improvements**:
- ✅ Trims whitespace from all string inputs
- ✅ Only sends non-empty fields (no more empty strings)
- ✅ Sets proper defaults for optional fields
- ✅ Validates before submission

---

## Testing

### Test Cases

#### ✅ Test 1: Username Only
**Input**: 
- Platform: GitHub
- Username: `torvalds`

**Expected Result**: Job created successfully  
**Status**: ✅ PASS

---

#### ✅ Test 2: Username with @ Symbol
**Input**: 
- Platform: Reddit
- Username: `@python`

**Expected Result**: `@` stripped, job created with `python`  
**Status**: ✅ PASS

---

#### ✅ Test 3: URL Only
**Input**: 
- Platform: GitHub
- URL: `https://github.com/microsoft`

**Expected Result**: Username auto-extracted as `microsoft`, job created  
**Status**: ✅ PASS

---

#### ✅ Test 4: Both Username and URL
**Input**: 
- Platform: GitHub
- Username: `torvalds`
- URL: `https://github.com/torvalds`

**Expected Result**: Job created with provided username  
**Status**: ✅ PASS

---

#### ✅ Test 5: Empty Form
**Input**: 
- Platform: GitHub
- Username: (empty)
- URL: (empty)

**Expected Result**: Frontend validation blocks submission  
**Status**: ✅ PASS

---

## API Contract

### POST `/api/crawler/jobs/`

#### Request Body (All fields except `platform` are optional):

```json
{
    "platform": "github",           // REQUIRED: "github", "reddit", "twitter", etc.
    "target_username": "torvalds",  // OPTIONAL: Username to crawl
    "target_url": "https://...",    // OPTIONAL: Profile URL (username extracted if not provided)
    "crawl_posts": true,            // OPTIONAL: Default true
    "crawl_followers": false,       // OPTIONAL: Default false
    "crawl_following": false,       // OPTIONAL: Default false
    "max_posts": 50,                // OPTIONAL: Default 50, max 1000
    "max_followers": 100,           // OPTIONAL: Default 100, max 10000
    "entity": 123                   // OPTIONAL: Link to entity
}
```

#### Success Response (201 Created):

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user": 1,
    "user_username": "admin",
    "platform": "github",
    "target_username": "torvalds",
    "status": "in_progress",
    "progress": 0,
    "profiles_found": 0,
    "posts_found": 0,
    "created_at": "2025-10-03T20:45:00Z",
    ...
}
```

#### Error Response (400 Bad Request):

```json
{
    "target_username": ["Either target_username or target_url must be provided"],
    "max_posts": ["Cannot crawl more than 1000 posts at once"]
}
```

---

## Migration Steps

### Applied Migrations:
1. `python manage.py makemigrations socialcrawler`  
   → Created `0002_alter_crawljob_target_username.py`

2. `python manage.py migrate socialcrawler`  
   → Applied migration successfully

### Rollback (if needed):
```bash
python manage.py migrate socialcrawler 0001
```

---

## Files Modified

### Backend:
1. ✅ `socialcrawler/models.py` - Made `target_username` optional
2. ✅ `socialcrawler/serializers.py` - Enhanced validation logic
3. ✅ `socialcrawler/migrations/0002_alter_crawljob_target_username.py` - New migration

### Frontend:
1. ✅ `frontend/src/components/NewCrawlJob.tsx` - Improved form data cleaning

---

## Verification

### Steps to Verify:
1. ✅ Backend server restarted with new code
2. ✅ Migration applied successfully
3. ✅ Frontend can now create jobs with:
   - Username only ✅
   - URL only ✅
   - Both username and URL ✅
   - Cleaned usernames (@ stripped) ✅

### Current Status:
🟢 **All systems operational**

- Backend: http://127.0.0.1:8000/ ✅
- Frontend: http://localhost:5173/ ✅
- API: http://127.0.0.1:8000/api/crawler/ ✅

---

## Lessons Learned

1. **Always make fields optional if they're not truly required** - Don't force frontend to send empty strings
2. **Validate at the serializer level** - Use `validate()` method for cross-field validation
3. **Clean data before sending** - Frontend should never send empty strings
4. **Extract intelligence** - Auto-extract usernames from URLs when possible
5. **Provide clear error messages** - Help users understand what's wrong

---

## Next Steps

1. ✅ Bug fixed and tested
2. ⏳ Test with real crawl jobs (GitHub, Reddit)
3. ⏳ Add better error display in frontend UI
4. ⏳ Add form validation hints before submission
5. ⏳ Consider adding URL format hints per platform

---

## Support

If you encounter any issues:
1. Check Django logs for detailed error messages
2. Check browser console for frontend errors
3. Verify the migration is applied: `python manage.py showmigrations socialcrawler`
4. Test API directly with curl or Postman

---

**Status**: ✅ **RESOLVED**  
**Impact**: 🟢 **LOW** - Issue fixed, users can now create crawl jobs  
**Priority**: 🔴 **HIGH** - Core feature was broken
