import React from 'react';
import Layout from '@theme/Layout';
import LoginForm from '../components/Auth/LoginForm';
import { useHistory } from '@docusaurus/router';

export default function Login(): JSX.Element {
    const history = useHistory();

    const handleSuccess = () => {
        // Redirect to homepage after successful login
        history.push('/');
    };

    return (
        <Layout title="Login" description="Sign in to your account">
            <LoginForm onSuccess={handleSuccess} />
        </Layout>
    );
}
