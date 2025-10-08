import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/useAuth';

const Navbar = () => {
    const { user, isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    return (
        <nav className="bg-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex">
                        <div className="flex-shrink-0 flex items-center">
                            <Link to="/" className="text-2xl font-bold text-primary-600">
                                InfoExtractor
                            </Link>
                        </div>
                        {isAuthenticated && (
                            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                <Link
                                    to="/dashboard"
                                    className="border-transparent text-gray-500 hover:border-primary-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                >
                                    Dashboard
                                </Link>
                                <Link
                                    to="/dorks"
                                    className="border-transparent text-gray-500 hover:border-primary-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                >
                                    Dorks
                                </Link>
                                <Link
                                    to="/entities"
                                    className="border-transparent text-gray-500 hover:border-primary-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                >
                                    Entities
                                </Link>
                                <Link
                                    to="/chatbot"
                                    className="border-transparent text-gray-500 hover:border-primary-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                >
                                    Chatbot
                                </Link>
                                <Link
                                    to="/crawler"
                                    className="border-transparent text-gray-500 hover:border-primary-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                >
                                    🕷️ Crawler
                                </Link>
                                <Link
                                    to="/breach-checker"
                                    className="border-transparent text-gray-500 hover:border-primary-500 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                                >
                                    🔐 Breach Checker
                                </Link>
                            </div>
                        )}
                    </div>
                    <div className="flex items-center">
                        {isAuthenticated ? (
                            <div className="flex items-center space-x-4">
                                <span className="text-sm text-gray-700">
                                    Welcome, <span className="font-medium">{user?.username}</span>
                                </span>
                                <button
                                    onClick={handleLogout}
                                    className="btn-secondary text-sm"
                                >
                                    Logout
                                </button>
                            </div>
                        ) : (
                            <div className="flex items-center space-x-4">
                                <Link to="/login" className="btn-secondary text-sm">
                                    Sign in
                                </Link>
                                <Link to="/register" className="btn-primary text-sm">
                                    Sign up
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
