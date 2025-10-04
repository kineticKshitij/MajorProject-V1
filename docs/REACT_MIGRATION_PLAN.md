# React + JWT Migration Plan

## 🎯 Overview
Migrate Django template-based frontend to a modern React SPA with TailwindCSS and JWT authentication.

## 📋 Architecture Design

### Current Architecture
```
Django Monolith
├── Server-rendered templates
├── Session-based authentication
├── Django forms and views
└── Bootstrap 5 styling
```

### New Architecture
```
Backend (Django REST API)          Frontend (React SPA)
├── Django REST Framework          ├── React 18+ with Vite
├── JWT Authentication             ├── TailwindCSS
├── API Endpoints                  ├── React Router
├── CORS Configuration             ├── Axios for API calls
└── Admin Portal (unchanged)       └── React Query for state
```

## 🔧 Phase 1: Backend API Setup

### 1.1 Install Required Packages
```bash
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install drf-spectacular  # API documentation
```

### 1.2 Django Settings Configuration
```python
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at top
    # ... existing middleware
]

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### 1.3 API URL Structure
```
/api/
├── /auth/
│   ├── /login/          (POST) - JWT token
│   ├── /register/       (POST) - User registration
│   ├── /refresh/        (POST) - Refresh token
│   ├── /logout/         (POST) - Blacklist token
│   └── /user/           (GET)  - Current user info
├── /dorks/
│   ├── /                (GET, POST)
│   ├── /{id}/           (GET, PUT, DELETE)
│   ├── /{id}/execute/   (POST)
│   └── /{id}/bookmark/  (POST)
├── /categories/
│   ├── /                (GET, POST)
│   └── /{id}/           (GET, PUT, DELETE)
├── /entities/
│   ├── /                (GET, POST)
│   ├── /{id}/           (GET, PUT, DELETE)
│   ├── /types/          (GET)
│   ├── /templates/      (GET)
│   └── /analytics/      (GET)
├── /search/
│   ├── /sessions/       (GET, POST)
│   ├── /results/        (GET, POST)
│   └── /export/         (GET)
└── /chatbot/
    ├── /sessions/       (GET, POST)
    ├── /messages/       (POST)
    └── /{id}/messages/  (GET)
```

## 🎨 Phase 2: React Frontend Setup

### 2.1 Initialize React Project
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

### 2.2 Install Dependencies
```bash
# Core dependencies
npm install react-router-dom axios
npm install @tanstack/react-query
npm install jwt-decode

# TailwindCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# UI Components (optional but recommended)
npm install @headlessui/react @heroicons/react
npm install react-hot-toast  # For notifications

# Form handling
npm install react-hook-form
npm install @hookform/resolvers zod

# Development
npm install -D @types/node
```

### 2.3 Project Structure
```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── axios.js
│   │   ├── auth.js
│   │   ├── dorks.js
│   │   ├── entities.js
│   │   └── chatbot.js
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Modal.jsx
│   │   │   └── Navbar.jsx
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── RegisterForm.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── dorks/
│   │   │   ├── DorkList.jsx
│   │   │   ├── DorkCard.jsx
│   │   │   ├── DorkForm.jsx
│   │   │   └── DorkDetail.jsx
│   │   ├── entities/
│   │   │   ├── EntityDashboard.jsx
│   │   │   ├── EntityList.jsx
│   │   │   ├── EntityForm.jsx
│   │   │   └── EntityDetail.jsx
│   │   └── chatbot/
│   │       ├── ChatInterface.jsx
│   │       ├── MessageBubble.jsx
│   │       └── SessionList.jsx
│   ├── contexts/
│   │   └── AuthContext.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useDorks.js
│   │   └── useEntities.js
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Dorks.jsx
│   │   ├── Entities.jsx
│   │   ├── Profile.jsx
│   │   └── Chatbot.jsx
│   ├── utils/
│   │   ├── storage.js
│   │   └── helpers.js
│   ├── App.jsx
│   └── main.jsx
├── tailwind.config.js
├── vite.config.js
└── package.json
```

### 2.4 TailwindCSS Configuration
```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

## 🔐 Phase 3: JWT Authentication Implementation

### 3.1 Django Serializers
```python
# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
```

### 3.2 React Auth Context
```javascript
// src/contexts/AuthContext.jsx
import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../api/axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        if (decoded.exp * 1000 > Date.now()) {
          loadUser();
        } else {
          logout();
        }
      } catch (error) {
        logout();
      }
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    const response = await api.post('/auth/login/', { username, password });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    await loadUser();
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  const loadUser = async () => {
    const response = await api.get('/auth/user/');
    setUser(response.data);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### 3.3 Axios Configuration with JWT
```javascript
// src/api/axios.js
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    let token = localStorage.getItem('access_token');
    
    if (token) {
      const decoded = jwtDecode(token);
      const isExpired = decoded.exp * 1000 < Date.now();
      
      if (isExpired) {
        // Refresh token
        const refreshToken = localStorage.getItem('refresh_token');
        try {
          const response = await axios.post(
            'http://localhost:8000/api/auth/refresh/',
            { refresh: refreshToken }
          );
          token = response.data.access;
          localStorage.setItem('access_token', token);
        } catch (error) {
          // Refresh failed, redirect to login
          localStorage.clear();
          window.location.href = '/login';
        }
      }
      
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
```

## 📊 Phase 4: Core Components Migration

### 4.1 Component Examples

#### Navbar Component
```jsx
// src/components/common/Navbar.jsx
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-gray-900 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold">
            Google Dorks Toolkit
          </Link>
          
          <div className="flex gap-4">
            <Link to="/dorks" className="hover:text-blue-400">Dorks</Link>
            <Link to="/entities" className="hover:text-blue-400">Entities</Link>
            <Link to="/chatbot" className="hover:text-blue-400">AI Assistant</Link>
            
            {user ? (
              <>
                <Link to="/profile" className="hover:text-blue-400">
                  {user.username}
                </Link>
                <button onClick={logout} className="hover:text-red-400">
                  Logout
                </button>
              </>
            ) : (
              <Link to="/login" className="hover:text-blue-400">Login</Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
```

#### Dork Card Component
```jsx
// src/components/dorks/DorkCard.jsx
export default function DorkCard({ dork, onExecute, onBookmark }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold text-gray-900">{dork.title}</h3>
        <span className={`px-2 py-1 text-xs rounded ${getRiskColor(dork.risk_level)}`}>
          {dork.risk_level}
        </span>
      </div>
      
      <p className="text-gray-600 mb-4">{dork.description}</p>
      
      <div className="bg-gray-100 p-3 rounded mb-4">
        <code className="text-sm text-gray-800">{dork.query}</code>
      </div>
      
      <div className="flex gap-2">
        <button
          onClick={() => onExecute(dork.id)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Execute
        </button>
        <button
          onClick={() => onBookmark(dork.id)}
          className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
        >
          Bookmark
        </button>
      </div>
    </div>
  );
}

function getRiskColor(level) {
  const colors = {
    low: 'bg-green-100 text-green-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800',
  };
  return colors[level] || colors.low;
}
```

## 🚀 Phase 5: Implementation Steps

### Step 1: Backend API (Week 1)
1. Install packages: `pip install djangorestframework djangorestframework-simplejwt django-cors-headers`
2. Update Django settings
3. Create serializers for all models
4. Create API ViewSets and URLs
5. Test API endpoints with Postman/Thunder Client

### Step 2: React Setup (Week 1)
1. Initialize React project with Vite
2. Configure TailwindCSS
3. Setup React Router
4. Create basic layout and navigation
5. Configure Axios and API client

### Step 3: Authentication (Week 2)
1. Create Django JWT views
2. Create React auth context
3. Build login/register forms
4. Implement protected routes
5. Test token refresh flow

### Step 4: Core Features (Weeks 3-4)
1. Migrate Dorks functionality
2. Migrate Entity management
3. Migrate Search sessions
4. Migrate Chatbot interface
5. Add loading states and error handling

### Step 5: Testing & Polish (Week 5)
1. Comprehensive testing
2. Performance optimization
3. Responsive design testing
4. Production build configuration
5. Deployment setup

## 📦 Deployment Configuration

### Production Settings
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]

# Serve React build
STATICFILES_DIRS = [
    BASE_DIR / 'frontend/dist'
]
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # React frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri /index.html;
    }

    # Django API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Django admin
    location /admin/ {
        proxy_pass http://localhost:8000;
    }
}
```

## 🎯 Benefits of Migration

1. **Better Performance**: Single Page Application, no page reloads
2. **Modern UI**: TailwindCSS utilities, responsive design
3. **API-First**: Reusable API for mobile apps, integrations
4. **Scalability**: Independent frontend/backend deployment
5. **Developer Experience**: Hot reload, better debugging
6. **Security**: Stateless JWT authentication
7. **Flexibility**: Easy to add mobile apps later

## ⚠️ Important Notes

1. **Admin Portal**: Keep Django admin unchanged - it's perfect as is
2. **Backward Compatibility**: Keep old URLs working during transition
3. **Testing**: Extensive testing required for each feature
4. **Documentation**: Update API documentation with drf-spectacular
5. **Environment Variables**: Use `.env` files for configuration

## 📚 Resources

- Django REST Framework: https://www.django-rest-framework.org/
- JWT Authentication: https://django-rest-framework-simplejwt.readthedocs.io/
- React Router: https://reactrouter.com/
- TailwindCSS: https://tailwindcss.com/
- React Query: https://tanstack.com/query/latest

## 🏁 Next Steps

1. Review this plan and get approval
2. Create a new git branch: `feature/react-migration`
3. Start with Phase 1: Backend API setup
4. Implement features incrementally
5. Keep old templates during transition for comparison
