# Quick Start Guide: React + JWT Migration

## 🎯 Current Status

**Phase 1 Complete**: Backend API foundation with JWT authentication
**Next Phase**: Create additional API endpoints OR start React frontend

## 🚀 Test the API Now

### 1. Start the Development Server
```powershell
cd d:\MP@
.\env\Scripts\Activate.ps1
python manage.py runserver
```

### 2. Open API Documentation
Visit: http://127.0.0.1:8000/api/docs/

This gives you an interactive Swagger UI to test all endpoints!

### 3. Test Authentication Flow

#### Register a New User
```http
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "Test",
  "last_name": "User"
}
```

#### Login and Get Tokens
```http
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "SecurePass123!"
}
```

**Response will contain:**
```json
{
  "user": { ... },
  "refresh": "REFRESH_TOKEN_HERE",
  "access": "ACCESS_TOKEN_HERE",
  "message": "Welcome back, Test User!"
}
```

#### Get User Profile (Protected Route)
```http
GET http://127.0.0.1:8000/api/auth/user/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 🔧 Next Steps - Choose Your Path

### Option A: Complete Backend API First (Recommended)
Build all API endpoints before starting React:

1. **Dorks API** (~2-3 hours)
   - Create `googledorks/serializers.py`
   - Create `googledorks/api_views.py`
   - Create `googledorks/api_urls.py`
   - Endpoints for: list, create, update, delete, execute, bookmark

2. **Entities API** (~2-3 hours)
   - Create entity serializers
   - Create entity API views
   - Endpoints for: CRUD, templates, search sessions, analytics

3. **Chatbot API** (~1-2 hours)
   - Create chatbot serializers
   - Create chatbot API views
   - WebSocket support for real-time chat (optional)

### Option B: Start React Frontend Now
Begin building the React app while APIs are in progress:

1. **Initialize React Project**
   ```powershell
   npm create vite@latest frontend -- --template react
   cd frontend
   npm install
   ```

2. **Install Dependencies**
   ```powershell
   npm install react-router-dom axios @tanstack/react-query jwt-decode
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. **Configure TailwindCSS**
   Edit `tailwind.config.js`:
   ```javascript
   export default {
     content: ["./index.html", "./src/**/*.{js,jsx}"],
     theme: { extend: {} },
     plugins: [],
   }
   ```

4. **Create Basic Structure**
   - Setup React Router
   - Create AuthContext
   - Build Login/Register forms
   - Test JWT authentication

## 📋 Recommended Development Order

### Week 1: Complete Backend (5-8 hours)
- [x] ~~Authentication API~~ ✅ DONE
- [ ] Dorks API endpoints
- [ ] Categories API endpoints
- [ ] Basic testing

### Week 2: Complete Backend + Start React (8-10 hours)
- [ ] Entities API endpoints
- [ ] Chatbot API endpoints
- [ ] Initialize React project
- [ ] Setup TailwindCSS
- [ ] Create auth components

### Week 3: Core React Components (10-12 hours)
- [ ] Dashboard layout
- [ ] Dorks components
- [ ] Entities components
- [ ] Navigation and routing

### Week 4: Advanced Features (10-12 hours)
- [ ] Chatbot interface
- [ ] Search functionality
- [ ] Real-time updates
- [ ] Polish and testing

## 🛠️ Development Tools

### VS Code Extensions (Recommended)
- REST Client - Test API in VS Code
- Thunder Client - API testing GUI
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets

### Browser Extensions
- React Developer Tools
- Redux DevTools
- JSON Viewer

### Testing Tools
- Postman (API testing)
- Thunder Client (VS Code)
- Browser DevTools

## 📝 Sample API Test (VS Code REST Client)

Create `api-tests.http`:
```http
### Register User
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "username": "developer",
  "email": "dev@example.com",
  "password": "DevPass123!",
  "password2": "DevPass123!"
}

### Login
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "developer",
  "password": "DevPass123!"
}

### Get Profile (use token from login response)
GET http://127.0.0.1:8000/api/auth/user/
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

## 🎨 React Project Structure Preview

```
frontend/
├── src/
│   ├── api/
│   │   ├── axios.js              # Axios instance with JWT
│   │   ├── auth.js               # Auth API calls
│   │   ├── dorks.js              # Dorks API calls
│   │   └── entities.js           # Entities API calls
│   ├── components/
│   │   ├── common/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Button.jsx
│   │   │   └── Card.jsx
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── RegisterForm.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   └── dorks/
│   │       ├── DorkList.jsx
│   │       ├── DorkCard.jsx
│   │       └── DorkForm.jsx
│   ├── contexts/
│   │   └── AuthContext.jsx       # JWT auth context
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useDorks.js
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   └── Dorks.jsx
│   ├── App.jsx
│   └── main.jsx
├── tailwind.config.js
└── package.json
```

## 💡 Pro Tips

1. **Test API First**: Use Swagger UI to test before coding React
2. **Use React Query**: Better than raw axios for API state
3. **Atomic Commits**: Commit after each working feature
4. **Component Library**: Build reusable components first
5. **Mobile First**: Design for mobile, enhance for desktop

## 🚨 Common Issues & Solutions

### Issue: CORS Errors
**Solution**: Ensure Django server is running and CORS is configured

### Issue: Token Expired
**Solution**: Implement automatic token refresh in axios interceptor

### Issue: Protected Routes Not Working
**Solution**: Check token in localStorage and AuthContext

### Issue: Styling Not Applied
**Solution**: Verify Tailwind configuration and imports

## 📚 Learning Resources

### Django REST Framework
- Official Docs: https://www.django-rest-framework.org/
- Tutorial: https://www.django-rest-framework.org/tutorial/quickstart/

### React + JWT
- JWT Decode: https://github.com/auth0/jwt-decode
- React Router: https://reactrouter.com/
- React Query: https://tanstack.com/query/latest

### TailwindCSS
- Official Docs: https://tailwindcss.com/docs
- Components: https://tailwindui.com/
- Cheat Sheet: https://nerdcave.com/tailwind-cheat-sheet

## 🎯 Your Next Command

Choose one:

### Option A: Test Current API
```powershell
# Start server and test with Swagger UI
python manage.py runserver
# Then visit: http://127.0.0.1:8000/api/docs/
```

### Option B: Create Dorks API
```powershell
# I can help you create the dorks API endpoints next
# Just ask: "Create the dorks API endpoints"
```

### Option C: Start React Frontend
```powershell
# Initialize React project
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

## 🎉 What You've Accomplished

✅ Complete JWT authentication system
✅ User registration and login APIs
✅ Token refresh and blacklisting
✅ API documentation with Swagger
✅ CORS configured for React
✅ Migrations applied successfully
✅ Backward compatibility maintained

**You're 20% done with the migration!** 🚀

---

**Need help?** Just ask:
- "Create the dorks API"
- "Setup React frontend"
- "Test the authentication"
- "Show me example React components"
