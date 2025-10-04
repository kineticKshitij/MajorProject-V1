import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
    const { user } = useAuth();

    const cards = [
        {
            title: 'Google Dorks',
            description: 'Explore and execute Google dork queries',
            link: '/dorks',
            icon: '🔍',
            color: 'bg-blue-500',
        },
        {
            title: 'Entities',
            description: 'Manage and search entities',
            link: '/entities',
            icon: '🏢',
            color: 'bg-green-500',
        },
        {
            title: 'Chatbot',
            description: 'AI-powered information assistant',
            link: '/chatbot',
            icon: '💬',
            color: 'bg-purple-500',
        },
        {
            title: 'Bookmarks',
            description: 'Your saved dorks',
            link: '/bookmarks',
            icon: '⭐',
            color: 'bg-yellow-500',
        },
    ];

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">
                    Welcome back, {user?.first_name || user?.username}! 👋
                </h1>
                <p className="mt-2 text-gray-600">
                    Here's what you can do with Information Extractor
                </p>
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {cards.map((card) => (
                    <Link
                        key={card.title}
                        to={card.link}
                        className="card hover:shadow-lg transition-shadow duration-200"
                    >
                        <div className="flex items-center justify-center mb-4">
                            <div
                                className={`${card.color} w-16 h-16 rounded-full flex items-center justify-center text-3xl`}
                            >
                                {card.icon}
                            </div>
                        </div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                            {card.title}
                        </h3>
                        <p className="text-gray-600">{card.description}</p>
                    </Link>
                ))}
            </div>

            <div className="mt-12 grid grid-cols-1 gap-6 lg:grid-cols-3">
                <div className="card">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                        Recent Activity
                    </h3>
                    <p className="text-gray-500 text-sm">No recent activity yet</p>
                </div>

                <div className="card">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                        Quick Stats
                    </h3>
                    <div className="space-y-2">
                        <div className="flex justify-between">
                            <span className="text-gray-600">Dorks Executed</span>
                            <span className="font-semibold">0</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Entities Tracked</span>
                            <span className="font-semibold">0</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Chat Sessions</span>
                            <span className="font-semibold">0</span>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                        Quick Links
                    </h3>
                    <div className="space-y-2">
                        <Link
                            to="/dorks"
                            className="block text-primary-600 hover:text-primary-700"
                        >
                            Browse Dorks →
                        </Link>
                        <Link
                            to="/entities"
                            className="block text-primary-600 hover:text-primary-700"
                        >
                            Add Entity →
                        </Link>
                        <Link
                            to="/chatbot"
                            className="block text-primary-600 hover:text-primary-700"
                        >
                            Start Chat →
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
