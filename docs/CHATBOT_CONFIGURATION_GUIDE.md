# Chatbot Configuration Guide 🤖

## Issue
The chatbot is returning an error: **"I apologize, but I'm having trouble processing your request right now. Please try again later."**

## Root Cause
The **GEMINI_API_KEY** is not configured in your Django settings. Without this API key, the chatbot cannot communicate with Google's Gemini AI service.

## Solution: Configure Gemini API Key

### Step 1: Get Your Gemini API Key

1. **Visit Google AI Studio:**
   - Go to: https://makersuite.google.com/app/apikey
   - Or: https://aistudio.google.com/app/apikey

2. **Sign in with your Google account**

3. **Create a new API key:**
   - Click "Create API Key"
   - Select "Create API key in new project" (or use existing project)
   - Copy the generated API key

### Step 2: Add API Key to Your Project

You have **two options**:

#### Option A: Using Environment Variable (Recommended)

1. **Create a `.env` file** in your project root (`D:\MP@\.env`):
   ```bash
   GEMINI_API_KEY=your-api-key-here
   ```

2. **Install python-dotenv** (if not already installed):
   ```bash
   pip install python-dotenv
   ```

3. **Update `settings.py`** to load from .env:
   ```python
   # At the top of settings.py
   from pathlib import Path
   from dotenv import load_dotenv
   import os
   
   # Load environment variables
   load_dotenv()
   
   # ... rest of settings
   
   # Gemini API Configuration (around line 158)
   GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
   ```

#### Option B: Directly in Settings (Quick Test)

1. **Open `InformationExtractor/settings.py`**

2. **Find line 158** and replace:
   ```python
   GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
   ```
   
   With:
   ```python
   GEMINI_API_KEY = 'your-api-key-here'  # Replace with your actual key
   ```

   **⚠️ Warning:** Don't commit this to Git! Use Option A for production.

### Step 3: Restart Django Server

1. **Stop the Django server** (Ctrl+C in the terminal running `python manage.py runserver`)

2. **Start it again**:
   ```bash
   python manage.py runserver
   ```

3. **Verify configuration:**
   - Check the terminal output
   - You should **NOT** see: "GEMINI_API_KEY not configured. Chatbot will not function."
   - If configured correctly, you'll see: "Django version 5.2.6, using settings..."

### Step 4: Test the Chatbot

1. **Refresh your browser** at http://localhost:5174/chatbot

2. **Start a new chat**

3. **Send a test message**: "hello"

4. **Expected result:** You should get a friendly AI response instead of an error!

## Gemini API Details

### Free Tier Limits
- **60 requests per minute**
- **1,500 requests per day**
- **32,000 tokens per request**

This is **more than enough for development and testing**!

### Pricing
- **Free tier:** Great for development
- **Pay-as-you-go:** Only pay for what you use
- Check current pricing: https://ai.google.dev/pricing

## Troubleshooting

### Issue: "GEMINI_API_KEY not configured"
**Solution:** Make sure you:
1. Added the API key to settings or .env
2. Restarted the Django server
3. Used the correct API key format (no quotes in .env, quotes in settings.py)

### Issue: "API key not valid"
**Solution:**
1. Double-check the API key (copy-paste carefully)
2. Verify the API key is active in Google AI Studio
3. Try generating a new API key

### Issue: Still getting error responses
**Solution:**
1. Check Django terminal for detailed error logs
2. Look for lines starting with "Error generating Gemini response:"
3. Verify your internet connection
4. Check if the Gemini API service is accessible from your location

### Issue: Frontend shows "Chatbot Configuration Required"
**Solution:**
1. This means the `check_configuration` endpoint returned `configured: false`
2. Follow steps above to add API key
3. Restart Django server
4. Refresh browser

## Testing Commands

### Check if API key is loaded:
```bash
cd D:\MP@
python manage.py shell
```

Then in the Python shell:
```python
from django.conf import settings
print(f"API Key configured: {bool(settings.GEMINI_API_KEY)}")
print(f"API Key (first 10 chars): {settings.GEMINI_API_KEY[:10] if settings.GEMINI_API_KEY else 'Not set'}")
```

### Test the Gemini service directly:
```python
from chatbot.services import GeminiChatService

service = GeminiChatService()
print(f"Service configured: {service.is_configured()}")
```

## Quick Setup Script

Create a file `setup_chatbot.py` in your project root:

```python
import os

print("Chatbot Configuration Setup")
print("-" * 50)

api_key = input("Enter your Gemini API key: ").strip()

# Create or update .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update existing key or add new one
    found = False
    for i, line in enumerate(lines):
        if line.startswith('GEMINI_API_KEY='):
            lines[i] = f'GEMINI_API_KEY={api_key}\n'
            found = True
            break
    
    if not found:
        lines.append(f'\nGEMINI_API_KEY={api_key}\n')
    
    with open(env_path, 'w') as f:
        f.writelines(lines)
else:
    with open(env_path, 'w') as f:
        f.write(f'GEMINI_API_KEY={api_key}\n')

print(f"\n✅ API key saved to {env_path}")
print("✅ Please restart your Django server!")
print("\nTo test, run: python manage.py shell")
print("Then: from django.conf import settings; print(settings.GEMINI_API_KEY[:10])")
```

Run it with:
```bash
python setup_chatbot.py
```

## Current Status

- ✅ Chatbot code is working correctly
- ✅ Frontend UI is properly built
- ✅ API endpoints are configured
- ✅ Error handling is in place
- ❌ **GEMINI_API_KEY is not configured** ← This is the only issue!

## Summary

The chatbot is **fully functional** but needs the Gemini API key to work. Once you:

1. Get API key from https://makersuite.google.com/app/apikey
2. Add it to `.env` or `settings.py`
3. Restart Django server
4. Refresh browser

The chatbot will work perfectly! 🎉

## Additional Features

Once configured, your chatbot will:
- ✅ Answer questions about Google dorking
- ✅ Suggest relevant dorks from your database
- ✅ Provide entity research guidance
- ✅ Remember conversation context
- ✅ Generate appropriate chat titles
- ✅ Track usage metrics

Happy chatting! 🤖💬
