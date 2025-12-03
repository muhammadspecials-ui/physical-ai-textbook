import React, { useState } from 'react';
import { useHistory } from '@docusaurus/router';
import { authAPI } from '../../utils/api';
import styles from './Auth.module.css';

interface SignupFormProps {
    onSuccess?: () => void;
}

export default function SignupForm({ onSuccess }: SignupFormProps): JSX.Element {
    const history = useHistory();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        software_experience: 'intermediate',
        hardware_experience: 'beginner',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await authAPI.signup(formData);
            if (onSuccess) {
                onSuccess();
            } else {
                history.push('/');
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Signup failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.authContainer}>
            <div className={styles.authCard}>
                <h1 className={styles.authTitle}>Create Account</h1>
                <p className={styles.authSubtitle}>Join the Physical AI community</p>

                {error && <div className={styles.errorMessage}>{error}</div>}

                <form onSubmit={handleSubmit} className={styles.authForm}>
                    <div className={styles.formGroup}>
                        <label htmlFor="name">Full Name</label>
                        <input
                            id="name"
                            type="text"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                            placeholder="John Doe"
                        />
                    </div>

                    <div className={styles.formGroup}>
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            type="email"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            required
                            placeholder="you@example.com"
                        />
                    </div>

                    <div className={styles.formGroup}>
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            required
                            placeholder="••••••••"
                            minLength={6}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <div className={styles.formGroup}>
                            <label htmlFor="software">Software Experience</label>
                            <select
                                id="software"
                                value={formData.software_experience}
                                onChange={(e) => setFormData({ ...formData, software_experience: e.target.value })}
                            >
                                <option value="beginner">Beginner</option>
                                <option value="intermediate">Intermediate</option>
                                <option value="advanced">Advanced</option>
                            </select>
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="hardware">Hardware Experience</label>
                            <select
                                id="hardware"
                                value={formData.hardware_experience}
                                onChange={(e) => setFormData({ ...formData, hardware_experience: e.target.value })}
                            >
                                <option value="beginner">Beginner</option>
                                <option value="intermediate">Intermediate</option>
                                <option value="advanced">Advanced</option>
                            </select>
                        </div>
                    </div>

                    <button
                        type="submit"
                        className={styles.submitButton}
                        disabled={loading}
                    >
                        {loading ? 'Creating Account...' : 'Sign Up'}
                    </button>
                </form>

                <p className={styles.authFooter}>
                    Already have an account?{' '}
                    <a href="/login" className={styles.authLink}>
                        Sign in
                    </a>
                </p>
            </div>
        </div>
    );
}
