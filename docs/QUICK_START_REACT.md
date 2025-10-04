# 🚀 Quick Start Guide - Information Extractor

## Prerequisites
- Python 3.11+ with Django 5.2.6
- Node.js 18+ with npm
- Virtual environment activated

## Step 1: Start Django Backend

```powershell
# Navigate to project root
cd D:\MP@

# Activate virtual environment
.\env\Scripts\Activate.ps1

# Run Django server
python manage.py runserver
```

✅ Backend running at: **http://127.0.0.1:8000**
✅ API Documentation: **http://127.0.0.1:8000/api/docs/**

## Step 2: Start React Frontend

```powershell
# Open new terminal
# Navigate to frontend folder
cd D:\MP@\frontend

# Start development server
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

## Step 3: Test the Application

1. **Open Browser**: Go to http://localhost:5173
2. **Create Account**: Click "Sign up" and register
3. **Login**: Use your credentials to log in
4. **Dashboard**: You'll see the main dashboard with feature cards

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Django server won't start
```powershell
# Check if virtual environment is activated
.\env\Scripts\Activate.ps1

# Check installed packages
pip list

# If missing packages:
pip install -r requirements_api.txt
```

**Problem**: Database errors
```powershell
# Run migrations
python manage.py migrate
```

### Frontend Issues

**Problem**: React server won't start
```powershell
# Reinstall dependencies
cd frontend
npm install

# Clear cache and restart
npm run dev
```

**Problem**: Login fails
- Check Django backend is running
- Check CORS settings in Django settings.py
- Check API base URL in `frontend/src/services/api.ts`

## 📡 API Endpoints

### Authentication
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login
- POST `/api/auth/logout/` - Logout
- GET `/api/auth/profile/` - Get user profile

### Dorks
- GET `/api/dorks/categories/` - List categories
- GET `/api/dorks/dorks/` - List dorks
- POST `/api/dorks/dorks/{id}/execute/` - Execute dork
- POST `/api/dorks/dorks/{id}/bookmark/` - Toggle bookmark

### Entities
- GET `/api/dorks/entity-types/` - List entity types
- GET `/api/dorks/entities/` - List entities
- POST `/api/dorks/entities/` - Create entity

### Chatbot
- GET `/api/chatbot/sessions/` - List chat sessions
- POST `/api/chatbot/sessions/{id}/send_message/` - Send message

## 🎯 Next Steps

1. **Test Authentication**: Create account and login
2. **Explore API Docs**: Visit http://127.0.0.1:8000/api/docs/
3. **Build Features**: Start implementing dorks/entities/chatbot pages

## 📝 Development Workflow

1. Make changes to React components in `frontend/src/`
2. Vite will auto-reload the page
3. Check browser console for errors
4. Use React DevTools for debugging

## 🔑 Default Test User

If you need to create a superuser for admin:
```powershell
python manage.py createsuperuser
```

Then access admin at: **http://127.0.0.1:8000/admin/**

## 💡 Useful Commands

### Backend
```powershell
# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Shell
python manage.py shell
```

### Frontend
```powershell
# Install new package
npm install package-name

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📚 Project Structure

```
D:\MP@\
├── InformationExtractor/      # Django project settings
├── accounts/                   # User authentication app
├── googledorks/               # Dorks & entities app
├── chatbot/                   # Chatbot app
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── contexts/        # React contexts
│   │   └── types/           # TypeScript types
│   └── package.json
├── env/                       # Python virtual environment
└── manage.py
```

## 🎨 Key Features

- ✅ JWT Authentication with auto-refresh
- ✅ Protected routes
- ✅ Type-safe API calls
- ✅ TailwindCSS styling
- ✅ React Query for state management
- ✅ Responsive design

## 🚀 You're Ready!

Both servers should now be running:
- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:5173

Start building amazing features! 🎉
