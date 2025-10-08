import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/layout/Navbar';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ForgotPassword from './components/auth/ForgotPassword';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import DorksList from './pages/dorks/DorksList';
import DorkDetail from './pages/dorks/DorkDetail';
import CreateDork from './pages/dorks/CreateDork';
import ChatInterface from './pages/chatbot/ChatInterface';
import CrawlerDashboard from './components/CrawlerDashboard';
import NewCrawlJob from './components/NewCrawlJob';
import CrawlJobDetail from './components/CrawlJobDetail';
import ProfilesList from './components/ProfilesList';
import PostsList from './components/PostsList';
import EntitiesList from './components/EntitiesList';
import EntityDetail from './components/EntityDetail';
import NewEntity from './components/NewEntity';
import EditEntity from './components/EditEntity';
import BreachChecker from './components/BreachChecker/BreachChecker';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50">
            <Navbar />
            <Routes>
              {/* Public routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />

              {/* Protected routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />

              {/* Placeholder routes - will be implemented */}
              <Route
                path="/dorks"
                element={
                  <ProtectedRoute>
                    <DorksList />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/dorks/create"
                element={
                  <ProtectedRoute>
                    <CreateDork />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/dorks/:id"
                element={
                  <ProtectedRoute>
                    <DorkDetail />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/entities"
                element={
                  <ProtectedRoute>
                    <EntitiesList />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/entities/new"
                element={
                  <ProtectedRoute>
                    <NewEntity />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/entities/:id"
                element={
                  <ProtectedRoute>
                    <EntityDetail />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/entities/:id/edit"
                element={
                  <ProtectedRoute>
                    <EditEntity />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/chatbot"
                element={
                  <ProtectedRoute>
                    <ChatInterface />
                  </ProtectedRoute>
                }
              />

              {/* Crawler routes */}
              <Route
                path="/crawler"
                element={
                  <ProtectedRoute>
                    <CrawlerDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crawler/new"
                element={
                  <ProtectedRoute>
                    <NewCrawlJob />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crawler/jobs/:id"
                element={
                  <ProtectedRoute>
                    <CrawlJobDetail />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crawler/profiles"
                element={
                  <ProtectedRoute>
                    <ProfilesList />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crawler/posts"
                element={
                  <ProtectedRoute>
                    <PostsList />
                  </ProtectedRoute>
                }
              />

              <Route
                path="/bookmarks"
                element={
                  <ProtectedRoute>
                    <div className="p-8">
                      <h1 className="text-2xl font-bold">Bookmarks Page - Coming Soon</h1>
                    </div>
                  </ProtectedRoute>
                }
              />

              {/* Breach Checker - Public access for demo */}
              <Route path="/breach-checker" element={<BreachChecker />} />

              {/* Redirect root to dashboard */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />

              {/* 404 route */}
              <Route path="*" element={<div className="p-8"><h1 className="text-2xl font-bold">404 - Page Not Found</h1></div>} />
            </Routes>
          </div>
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
