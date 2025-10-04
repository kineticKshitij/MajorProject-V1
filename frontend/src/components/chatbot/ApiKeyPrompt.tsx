interface ApiKeyPromptProps {
    message: string;
}

const ApiKeyPrompt = ({ message }: ApiKeyPromptProps) => {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
            <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
                <div className="text-center">
                    {/* Icon */}
                    <div className="mx-auto w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mb-6">
                        <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                    </div>

                    {/* Title */}
                    <h2 className="text-2xl font-bold text-gray-900 mb-3">
                        Chatbot Configuration Required
                    </h2>

                    {/* Message */}
                    <p className="text-gray-600 mb-6">
                        {message}
                    </p>

                    {/* Instructions */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-left mb-6">
                        <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            How to configure the Gemini AI API:
                        </h3>
                        <ol className="space-y-3 text-sm text-gray-700">
                            <li className="flex items-start gap-2">
                                <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-semibold">1</span>
                                <div>
                                    <strong>Get an API key:</strong>
                                    <p className="text-gray-600 mt-1">
                                        Visit <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Google AI Studio</a> to generate your free Gemini API key.
                                    </p>
                                </div>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-semibold">2</span>
                                <div>
                                    <strong>Add to Django settings:</strong>
                                    <div className="mt-2 bg-gray-900 text-gray-100 p-3 rounded font-mono text-xs overflow-x-auto">
                                        <code>
                                            # In your settings.py or .env file<br />
                                            GEMINI_API_KEY = "your-api-key-here"
                                        </code>
                                    </div>
                                </div>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-semibold">3</span>
                                <div>
                                    <strong>Restart Django:</strong>
                                    <p className="text-gray-600 mt-1">
                                        Restart your Django development server to apply the changes.
                                    </p>
                                </div>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-semibold">4</span>
                                <div>
                                    <strong>Refresh this page:</strong>
                                    <p className="text-gray-600 mt-1">
                                        Once configured, reload this page to start chatting!
                                    </p>
                                </div>
                            </li>
                        </ol>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-4 justify-center">
                        <button
                            onClick={() => window.location.reload()}
                            className="btn-primary"
                        >
                            Refresh Page
                        </button>
                        <a
                            href="https://makersuite.google.com/app/apikey"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn-secondary"
                        >
                            Get API Key
                        </a>
                    </div>

                    {/* Note */}
                    <div className="mt-6 text-sm text-gray-500">
                        <p>
                            <strong>Note:</strong> The Gemini API offers a generous free tier.
                            You can check the limits and pricing on the{' '}
                            <a href="https://ai.google.dev/pricing" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                                official pricing page
                            </a>.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ApiKeyPrompt;
