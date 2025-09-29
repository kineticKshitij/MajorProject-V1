# AI Chatbot Setup Guide

## Google Gemini API Configuration

### 1. Get Your API Key

1. Visit the [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" 
4. Copy the generated API key

### 2. Configure the Application

#### Option 1: Environment Variable (Recommended)
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac  
export GEMINI_API_KEY=your_api_key_here
```

#### Option 2: .env file
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

#### Option 3: Django Settings (Development Only)
Edit `InformationExtractor/settings.py`:
```python
GEMINI_API_KEY = 'your_api_key_here'
```

### 3. Test the Configuration

1. Start the Django server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to: `http://localhost:8000/chat/`

3. Try sending a message to the AI assistant

### 4. Chatbot Features

- **Intelligent Responses**: Powered by Google Gemini 2.0 Flash
- **Security Focus**: Specialized in Google dorking and ethical hacking
- **Session Management**: Persistent conversation history
- **Context Awareness**: Remembers conversation context
- **Feedback System**: Rate AI responses for improvement
- **Responsive UI**: Modern chat interface with typing indicators

### 5. API Usage Guidelines

- **Rate Limits**: Google AI Studio has usage quotas
- **Cost**: Check current pricing at [Google AI Pricing](https://ai.google.dev/pricing)
- **Best Practices**:
  - Keep conversations focused on security research
  - Provide context for better responses
  - Use feedback system to improve responses
  - Respect API usage limits

### 6. Troubleshooting

**"GEMINI_API_KEY not configured" Warning**
- Ensure API key is properly set in environment or .env file
- Restart Django server after setting environment variables

**"API Key is invalid" Error**
- Verify API key is copied correctly
- Check if API key has proper permissions
- Ensure Google AI Studio account is active

**"Rate limit exceeded" Error**
- You've reached Google AI Studio usage limits
- Wait for quota reset or upgrade your plan
- Check usage at [Google AI Studio](https://aistudio.google.com/)

**No Response from Chatbot**
- Check browser console for JavaScript errors
- Verify Django server is running
- Check API key configuration
- Review Django logs for error messages

### 7. Security Considerations

- **Never commit API keys** to version control
- **Use environment variables** in production
- **Rotate API keys** regularly
- **Monitor usage** to detect unauthorized access
- **Restrict API key permissions** if possible

### 8. Advanced Configuration

#### Custom System Prompt
Edit `CHATBOT_SYSTEM_PROMPT` in settings.py to customize AI behavior:

```python
CHATBOT_SYSTEM_PROMPT = """Your custom system prompt here..."""
```

#### Conversation History Limit
Adjust `CHATBOT_MAX_HISTORY` to control context length:

```python
CHATBOT_MAX_HISTORY = 10  # Number of previous messages to include
```

#### Model Selection
Change the Gemini model in settings.py:

```python
GEMINI_MODEL = 'gemini-2.0-flash-exp'  # or other available models
```