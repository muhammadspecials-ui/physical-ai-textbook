import React from 'react';
import Layout from '@theme/Layout';
import SignupForm from '../components/Auth/SignupForm';
import { useHistory } from '@docusaurus/router';

export default function Signup(): JSX.Element {
    const history = useHistory();

    const handleSuccess = () => {
        // Redirect to homepage after successful signup
        history.push('/');
    };

    return (
        <Layout title="Sign Up" description="Create your account">
            <SignupForm onSuccess={handleSuccess} />
        </Layout>
    );
}
