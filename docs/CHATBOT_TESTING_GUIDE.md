# 🧪 Chatbot Testing Guide

## Quick Start

### 1. Ensure Django Server is Running
```bash
cd d:\MP@
python manage.py runserver
```
Server should be at: http://127.0.0.1:8000

### 2. React Dev Server is Running
```bash
cd d:\MP@\frontend
npm run dev
```
Server is at: http://localhost:5173 ✅

### 3. Configure Gemini API Key (REQUIRED)

The chatbot requires Google's Gemini AI API key. Without it, you'll see a configuration prompt.

**Option 1: Environment Variable**
```bash
# In your terminal or .env file
export GEMINI_API_KEY="your-api-key-here"
```

**Option 2: Django Settings**
```python
# In InformationExtractor/settings.py
GEMINI_API_KEY = "your-api-key-here"
```

**Get API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy key to Django
5. Restart Django server

---

## 📋 Testing Checklist

### ✅ Phase 1: Access & Authentication
1. Open http://localhost:5173/chatbot
2. Should redirect to /login if not authenticated
3. Log in with your credentials (e.g., username: "Paper")
4. Should redirect back to /chatbot

### ✅ Phase 2: API Configuration
**If API key is NOT configured:**
- [ ] See ApiKeyPrompt component with warning icon
- [ ] Read setup instructions
- [ ] Click "Get API Key" link (opens Google AI Studio)
- [ ] Click "Refresh Page" after configuring
- [ ] Verify configuration check passes

**If API key IS configured:**
- [ ] Should proceed directly to chat interface

### ✅ Phase 3: First Session
- [ ] System automatically creates first chat session
- [ ] See empty state with welcome message
- [ ] See 3 example prompts:
  - "How do I find exposed databases?"
  - "What are the best dorks for finding API keys?"
  - "Help me research a company"
- [ ] Sidebar shows 1 session (e.g., "New Chat Session")

### ✅ Phase 4: Send Messages
**Test Basic Messaging:**
1. Type a message: "Hello, can you help me with Google dorking?"
2. Press Enter (or click Send button)
3. Verify:
   - [ ] User message appears (right-aligned, blue bubble, 👤 avatar)
   - [ ] Message shows in chat immediately
   - [ ] Loading animation appears (bouncing dots with 🤖 avatar)
   - [ ] AI response arrives (left-aligned, white bubble, 🤖 avatar)
   - [ ] Auto-scrolls to bottom
   - [ ] Timestamps show (e.g., "2 minutes ago")
   - [ ] Token usage shows on AI message (e.g., "145 tokens")

**Test Message Input Features:**
- [ ] Character counter updates (e.g., "25 / 4000")
- [ ] Shift+Enter creates new line (doesn't send)
- [ ] Enter sends message
- [ ] Textarea auto-expands as you type (max 200px height)
- [ ] Can't send empty messages
- [ ] Input clears after sending

**Test Long Messages:**
1. Type >3500 characters
2. Verify:
   - [ ] Warning appears: "Long message" (orange)
3. Type >3800 characters
4. Verify:
   - [ ] Warning changes: "Character limit approaching!" (red)

### ✅ Phase 5: Message Actions (AI Messages Only)
**Copy Button:**
1. Hover over an AI message
2. Click "Copy" button
3. Verify:
   - [ ] Button changes to green checkmark
   - [ ] Text says "Copied!"
   - [ ] Message is in clipboard (paste somewhere to verify)
   - [ ] Reverts to "Copy" after 2 seconds

**Feedback Buttons:**
1. Click thumbs up (👍) on an AI message
2. Verify:
   - [ ] Button turns green
   - [ ] Both buttons become disabled
   - [ ] Can't change feedback
3. Try on another message: click thumbs down (👎)
4. Verify:
   - [ ] Button turns red
   - [ ] Both buttons become disabled

### ✅ Phase 6: Session Management
**Create New Session:**
1. Click "+ New Chat" button (top-right or sidebar)
2. Verify:
   - [ ] New session created
   - [ ] Chat area clears
   - [ ] Empty state appears
   - [ ] Sidebar shows new session at top
   - [ ] URL updates with ?session=[new-id]
   - [ ] Session counter increments

**Switch Between Sessions:**
1. Click on a previous session in sidebar
2. Verify:
   - [ ] Session becomes highlighted (blue border)
   - [ ] Message history loads
   - [ ] URL updates
   - [ ] Header shows session title
3. Click on another session
4. Verify same behavior

**Delete Session:**
1. Hover over a session in sidebar
2. Click trash icon (🗑️)
3. Verify:
   - [ ] Confirmation dialog appears: "Are you sure you want to delete this chat session?"
   - [ ] Click "Cancel" → nothing happens
   - [ ] Click "OK" → session deleted
   - [ ] Session removed from sidebar
   - [ ] If was current session: chat clears, creates new session
   - [ ] If was not current: current session remains active

### ✅ Phase 7: Sidebar Features
**Session Display:**
- [ ] Each session shows:
  - Title (e.g., "Chat about Google dorking")
  - Message count (e.g., "5 messages")
  - Last updated time (e.g., "10 minutes ago")
  - Delete button
  - Entity badge (if applicable)
- [ ] Active session highlighted with blue left border
- [ ] Hover effects work

**Empty State:**
1. Delete all sessions
2. Verify:
   - [ ] Shows "No chat sessions yet"
   - [ ] Shows "Start a new conversation!"
   - [ ] Can still create new session

**Sidebar Footer:**
- [ ] Shows tips:
  - "Ask about Google dorking techniques"
  - "Get help with entity research"
  - "Learn security best practices"

### ✅ Phase 8: Responsive Design
**Desktop (≥ 1024px):**
- [ ] Sidebar always visible (320px width)
- [ ] Main chat area flexible
- [ ] No hamburger menu
- [ ] Smooth layout

**Mobile (< 1024px):**
1. Resize browser to mobile size
2. Verify:
   - [ ] Sidebar hidden by default
   - [ ] Hamburger menu visible (☰)
3. Click hamburger menu
4. Verify:
   - [ ] Sidebar slides in from left
   - [ ] Dark overlay covers chat area
   - [ ] Close button (✕) visible in sidebar
5. Click backdrop or close button
6. Verify:
   - [ ] Sidebar slides out
   - [ ] Overlay disappears

**Tablet:**
- [ ] Responsive breakpoints work smoothly
- [ ] Layout adapts appropriately

### ✅ Phase 9: Header Features
- [ ] Shows session title (or "New Chat")
- [ ] Shows entity name if applicable (e.g., "Entity: Microsoft")
- [ ] "+ New Chat" button works
- [ ] Hamburger menu works on mobile

### ✅ Phase 10: URL Navigation
**Direct URL Access:**
1. Copy URL with session ID (e.g., http://localhost:5173/chatbot?session=123)
2. Open in new tab
3. Verify:
   - [ ] Loads that specific session
   - [ ] Shows message history
   - [ ] Session highlighted in sidebar

**URL Updates:**
- [ ] Creating new session updates URL
- [ ] Switching sessions updates URL
- [ ] Can share URL with session ID

### ✅ Phase 11: Error Handling
**Network Errors:**
1. Stop Django server
2. Try sending a message
3. Verify:
   - [ ] Error message appears (not browser crash)
   - [ ] Can retry after server restarts

**Empty Session:**
- [ ] Handles empty message list gracefully
- [ ] Shows empty state

**API Failures:**
- [ ] Doesn't crash on API errors
- [ ] Shows helpful error messages

### ✅ Phase 12: Performance
**Message Loading:**
- [ ] Messages load quickly (<1s)
- [ ] No flickering or layout shifts
- [ ] Smooth scrolling

**Typing Experience:**
- [ ] No input lag
- [ ] Character counter updates instantly
- [ ] Textarea expansion smooth

**Session Switching:**
- [ ] Fast transition between sessions
- [ ] No delays in loading history

---

## 🐛 Common Issues & Solutions

### Issue: "Chatbot Configuration Required" message
**Solution:** 
1. Get Gemini API key from https://makersuite.google.com/app/apikey
2. Add to Django settings: `GEMINI_API_KEY = "your-key"`
3. Restart Django server
4. Refresh page

### Issue: Can't send messages
**Check:**
- [ ] Django server running?
- [ ] Session created?
- [ ] Message not empty?
- [ ] Check browser console for errors

### Issue: Sidebar not showing sessions
**Check:**
- [ ] Django backend running?
- [ ] API endpoint accessible: http://127.0.0.1:8000/api/chatbot/sessions/
- [ ] User authenticated?
- [ ] Check Network tab in DevTools

### Issue: AI responses not appearing
**Check:**
- [ ] GEMINI_API_KEY configured correctly?
- [ ] Check Django console for errors
- [ ] API quota not exceeded?
- [ ] Check backend logs

### Issue: Feedback buttons not working
**Check:**
- [ ] Only works on AI messages (not user messages)
- [ ] Can only submit feedback once per message
- [ ] Check Network tab for API call

---

## ✅ Test Results Expected

### All Green ✅
If everything is working:
- ✅ Can access chatbot after login
- ✅ Session management works (create, switch, delete)
- ✅ Messages send and receive correctly
- ✅ AI responses appear
- ✅ Copy and feedback features work
- ✅ Responsive on all screen sizes
- ✅ No console errors
- ✅ Smooth user experience

### Success Criteria
- **No TypeScript errors** ✅
- **No runtime errors** ✅
- **All features functional** ✅
- **Responsive design works** ✅
- **Professional UI/UX** ✅

---

## 📸 Screenshots to Verify

1. **Login Page**: Clean, professional
2. **Empty Chat State**: Welcome message with examples
3. **Chat with Messages**: User/AI bubbles, timestamps, actions
4. **Sidebar**: Session list with metadata
5. **Mobile View**: Sidebar overlay, hamburger menu
6. **API Key Prompt**: Warning with instructions
7. **Feedback Buttons**: Green (helpful) / Red (not helpful)
8. **Copy Button**: "Copied!" confirmation
9. **Character Counter**: Updates in real-time
10. **Loading State**: Bouncing dots animation

---

## 🎉 When Testing is Complete

✅ **All features working** → Ready for production!

Next steps:
1. Document any bugs found
2. Fix critical issues
3. Build Entities features next
4. Final deployment preparation

---

## 🔥 Quick Test Flow (5 minutes)

1. **Login** → http://localhost:5173/login
2. **Go to Chatbot** → http://localhost:5173/chatbot
3. **Send message** → "Hello!"
4. **Wait for AI response** → Should appear in ~2-5 seconds
5. **Copy AI message** → Click copy button
6. **Give feedback** → Click thumbs up
7. **Create new session** → Click "+ New Chat"
8. **Delete session** → Click trash icon on old session
9. **Mobile test** → Resize browser to mobile width
10. **Done!** ✅

---

**Status**: Ready for comprehensive testing! 🚀

**React Server**: http://localhost:5173 ✅ RUNNING  
**Django Server**: http://127.0.0.1:8000 (ensure it's running)
