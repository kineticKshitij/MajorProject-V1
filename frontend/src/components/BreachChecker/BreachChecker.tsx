import React, { useState } from 'react';
import axios from 'axios';
import './BreachChecker.css';

interface Breach {
    name: string;
    title: string;
    domain: string;
    breach_date: string;
    pwn_count: number;
    description: string;
    data_classes: string[];
    is_verified: boolean;
    logo_path?: string;
}

interface BreachResult {
    status: 'found' | 'safe' | 'error';
    email?: string;
    breach_count?: number;
    breaches?: Breach[];
    message?: string;
    most_recent_breach?: string;
    total_accounts_affected?: number;
}

const BreachChecker: React.FC = () => {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<BreachResult | null>(null);
    const [error, setError] = useState('');

    const validateEmail = (email: string): boolean => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    };

    const checkBreach = async () => {
        // Validation
        if (!email.trim()) {
            setError('Please enter an email address');
            return;
        }

        if (!validateEmail(email)) {
            setError('Please enter a valid email address');
            return;
        }

        setError('');
        setLoading(true);
        setResult(null);

        try {
            const response = await axios.post('http://localhost:8000/api/dorks/check-breach/', { email });
            setResult(response.data);
        } catch (err: any) {
            setError(err.response?.data?.message || 'An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !loading) {
            checkBreach();
        }
    };

    const formatDate = (dateString: string): string => {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const getRiskLevel = (breachCount: number): { level: string; color: string } => {
        if (breachCount === 0) return { level: 'Safe', color: 'green' };
        if (breachCount <= 2) return { level: 'Low Risk', color: 'yellow' };
        if (breachCount <= 5) return { level: 'Medium Risk', color: 'orange' };
        return { level: 'High Risk', color: 'red' };
    };

    return (
        <div className="breach-checker-container">
            <div className="breach-checker-header">
                <h1>🔐 Data Breach Checker</h1>
                <p className="subtitle">
                    Check if your email has been compromised in data breaches
                </p>
                <p className="disclaimer">
                    Powered by{' '}
                    <a href="https://haveibeenpwned.com" target="_blank" rel="noopener noreferrer">
                        Have I Been Pwned
                    </a>
                    {' '}- Used by security professionals worldwide
                </p>
            </div>

            <div className="breach-checker-input">
                <div className="input-group">
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Enter email address (e.g., test@example.com)"
                        disabled={loading}
                        className="email-input"
                    />
                    <button
                        onClick={checkBreach}
                        disabled={loading || !email}
                        className="check-button"
                    >
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Checking...
                            </>
                        ) : (
                            <>
                                <span>🔍</span>
                                Check Now
                            </>
                        )}
                    </button>
                </div>

                {error && (
                    <div className="alert alert-error">
                        ⚠️ {error}
                    </div>
                )}
            </div>

            {result && (
                <div className="breach-results">
                    {result.status === 'safe' && (
                        <div className="alert alert-success">
                            <div className="alert-icon">✅</div>
                            <div className="alert-content">
                                <h2>Great News!</h2>
                                <p>{result.message}</p>
                                <p className="tip">
                                    💡 <strong>Tip:</strong> Keep using strong, unique passwords and enable
                                    two-factor authentication whenever possible.
                                </p>
                            </div>
                        </div>
                    )}

                    {result.status === 'found' && result.breaches && (
                        <div className="alert alert-danger">
                            <div className="alert-icon">⚠️</div>
                            <div className="alert-content">
                                <h2>{result.breach_count} Data Breach{result.breach_count !== 1 ? 'es' : ''} Found</h2>
                                <p>
                                    This email was found in <strong>{result.breach_count}</strong> data breach
                                    {result.breach_count !== 1 ? 'es' : ''}, affecting approximately{' '}
                                    <strong>{result.total_accounts_affected?.toLocaleString()}</strong> total accounts.
                                </p>
                                <div className={`risk-badge risk-${getRiskLevel(result.breach_count!).color}`}>
                                    {getRiskLevel(result.breach_count!).level}
                                </div>

                                <div className="recommendations">
                                    <h3>🛡️ Recommended Actions:</h3>
                                    <ul>
                                        <li>Change your passwords immediately on all affected sites</li>
                                        <li>Enable two-factor authentication (2FA)</li>
                                        <li>Use unique passwords for each website</li>
                                        <li>Consider using a password manager</li>
                                        <li>Monitor your accounts for suspicious activity</li>
                                    </ul>
                                </div>

                                <div className="breaches-list">
                                    <h3>📋 Breach Details:</h3>
                                    {result.breaches.map((breach, index) => (
                                        <div key={index} className="breach-card">
                                            <div className="breach-header">
                                                {breach.logo_path && (
                                                    <img
                                                        src={`https://haveibeenpwned.com${breach.logo_path}`}
                                                        alt={breach.title}
                                                        className="breach-logo"
                                                        onError={(e) => {
                                                            (e.target as HTMLImageElement).style.display = 'none';
                                                        }}
                                                    />
                                                )}
                                                <div className="breach-title">
                                                    <h4>{breach.title}</h4>
                                                    {breach.domain && (
                                                        <span className="breach-domain">{breach.domain}</span>
                                                    )}
                                                </div>
                                                {breach.is_verified && (
                                                    <span className="verified-badge">✓ Verified</span>
                                                )}
                                            </div>

                                            <div className="breach-info">
                                                <p className="breach-date">
                                                    <strong>Breach Date:</strong> {formatDate(breach.breach_date)}
                                                </p>
                                                <p className="breach-count">
                                                    <strong>Accounts Affected:</strong> {breach.pwn_count.toLocaleString()}
                                                </p>
                                            </div>

                                            <div
                                                className="breach-description"
                                                dangerouslySetInnerHTML={{ __html: breach.description }}
                                            />

                                            {breach.data_classes && breach.data_classes.length > 0 && (
                                                <div className="data-compromised">
                                                    <strong>Data Compromised:</strong>
                                                    <div className="data-tags">
                                                        {breach.data_classes.map((dataClass, idx) => (
                                                            <span key={idx} className="data-tag">
                                                                {dataClass}
                                                            </span>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {result.status === 'error' && (
                        <div className="alert alert-error">
                            <div className="alert-icon">❌</div>
                            <div className="alert-content">
                                <h2>Error</h2>
                                <p>{result.message}</p>
                            </div>
                        </div>
                    )}
                </div>
            )}

            <div className="breach-checker-footer">
                <div className="info-box">
                    <h3>ℹ️ About This Tool</h3>
                    <p>
                        This tool uses the Have I Been Pwned database, which contains over
                        12 billion compromised accounts from 600+ data breaches. It's trusted
                        by security professionals worldwide.
                    </p>
                    <p>
                        <strong>Privacy:</strong> We don't store your email addresses. This check
                        is performed directly against the Have I Been Pwned API.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default BreachChecker;
