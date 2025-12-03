import React, { useState } from 'react';
import { contentAPI } from '../../utils/api';
import { useAuth } from '../../contexts/AuthContext';
import styles from './ContentActions.module.css';

interface ContentActionsProps {
    content: string;
    pagePath: string;
}

const ContentActions: React.FC<ContentActionsProps> = ({ content, pagePath }) => {
    const { user } = useAuth();
    const [personalizedContent, setPersonalizedContent] = useState<string | null>(null);
    const [translatedContent, setTranslatedContent] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [activeView, setActiveView] = useState<'original' | 'personalized' | 'translated'>('original');

    const handlePersonalize = async () => {
        if (!user) {
            alert('Please log in to personalize content');
            return;
        }

        setLoading(true);
        try {
            const response = await contentAPI.personalize({ content, page_path: pagePath });
            setPersonalizedContent(response.personalized_content);
            setActiveView('personalized');
        } catch (error) {
            console.error('Personalization error:', error);
            alert('Failed to personalize content');
        } finally {
            setLoading(false);
        }
    };

    const handleTranslate = async () => {
        setLoading(true);
        try {
            const response = await contentAPI.translate({ content });
            setTranslatedContent(response.translated_content);
            setActiveView('translated');
        } catch (error) {
            console.error('Translation error:', error);
            alert('Failed to translate content');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.buttonGroup}>
                <button
                    onClick={() => setActiveView('original')}
                    className={`${styles.button} ${activeView === 'original' ? styles.active : ''}`}
                >
                    📖 Original
                </button>

                {user && (
                    <button
                        onClick={handlePersonalize}
                        disabled={loading}
                        className={`${styles.button} ${activeView === 'personalized' ? styles.active : ''}`}
                    >
                        ✨ Personalize for Me
                    </button>
                )}

                <button
                    onClick={handleTranslate}
                    disabled={loading}
                    className={`${styles.button} ${activeView === 'translated' ? styles.active : ''}`}
                >
                    🌐 اردو میں (Urdu)
                </button>
            </div>

            {loading && (
                <div className={styles.loadingBar}>
                    <div className={styles.loadingProgress}></div>
                </div>
            )}

            {activeView === 'personalized' && personalizedContent && (
                <div className={styles.contentBox}>
                    <div className={styles.badge}>Personalized for your experience level</div>
                    <div dangerouslySetInnerHTML={{ __html: personalizedContent }} />
                </div>
            )}

            {activeView === 'translated' && translatedContent && (
                <div className={styles.contentBox} dir="rtl">
                    <div className={styles.badge}>Urdu Translation</div>
                    <div dangerouslySetInnerHTML={{ __html: translatedContent }} />
                </div>
            )}
        </div>
    );
};

export default ContentActions;
