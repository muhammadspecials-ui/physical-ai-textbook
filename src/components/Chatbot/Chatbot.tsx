import React, { useState, useRef, useEffect } from 'react';
import { chatAPI } from '../../utils/api';
import styles from './Chatbot.module.css';

export default function Chatbot(): JSX.Element {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([
        { role: 'assistant', content: 'Hi! I\'m your AI tutor. Ask me anything about Physical AI and Robotics!' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setLoading(true);

        try {
            const response = await chatAPI.sendMessage({
                question: userMessage,
                selected_text: '',
            });

            setMessages(prev => [...prev, { role: 'assistant', content: response.answer }]);
        } catch (error: any) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please make sure the backend server is running on port 8000.'
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Voice Recognition State
    const [isRecording, setIsRecording] = useState(false);
    const recognitionRef = useRef<any>(null);

    // Initialize Speech Recognition
    useEffect(() => {
        if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
            const SpeechRecognition = (window as any).webkitSpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.interimResults = false;
            recognitionRef.current.lang = 'en-US';

            recognitionRef.current.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript;
                setInput(transcript);
                setIsRecording(false);
                // Optional: Auto-send after voice input
                // handleSend(); 
            };

            recognitionRef.current.onerror = (event: any) => {
                console.error('Speech recognition error', event.error);
                setIsRecording(false);
            };

            recognitionRef.current.onend = () => {
                setIsRecording(false);
            };
        }
    }, []);

    const toggleRecording = () => {
        if (!recognitionRef.current) {
            alert('Speech recognition is not supported in this browser.');
            return;
        }

        if (isRecording) {
            recognitionRef.current.stop();
        } else {
            recognitionRef.current.start();
            setIsRecording(true);
        }
    };

    const speakText = (text: string) => {
        if ('speechSynthesis' in window) {
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        } else {
            alert('Text-to-speech is not supported in this browser.');
        }
    };

    return (
        <>
            {/* Chatbot Toggle Button */}
            <button
                className={styles.chatToggle}
                onClick={() => setIsOpen(!isOpen)}
                aria-label="Toggle chatbot"
            >
                {isOpen ? '✕' : '💬'}
            </button>

            {/* Chatbot Window */}
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader}>
                        <div className={styles.chatHeaderContent}>
                            <div className={styles.chatAvatar}>🤖</div>
                            <div>
                                <div className={styles.chatTitle}>AI Tutor</div>
                                <div className={styles.chatStatus}>
                                    <span className={styles.statusDot}></span>
                                    Online
                                </div>
                            </div>
                        </div>
                        <button
                            className={styles.closeButton}
                            onClick={() => setIsOpen(false)}
                            aria-label="Close chat"
                        >
                            ✕
                        </button>
                    </div>

                    <div className={styles.chatMessages}>
                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.assistantMessage
                                    }`}
                            >
                                {msg.role === 'assistant' && (
                                    <div className={styles.messageAvatar}>🤖</div>
                                )}
                                <div className={styles.messageContent}>
                                    {msg.content}
                                    {msg.role === 'assistant' && (
                                        <button
                                            onClick={() => speakText(msg.content)}
                                            style={{
                                                background: 'none',
                                                border: 'none',
                                                cursor: 'pointer',
                                                marginLeft: '8px',
                                                opacity: 0.7,
                                                fontSize: '1.1em'
                                            }}
                                            title="Read aloud"
                                        >
                                            🔊
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className={`${styles.message} ${styles.assistantMessage}`}>
                                <div className={styles.messageAvatar}>🤖</div>
                                <div className={styles.messageContent}>
                                    <div className={styles.typingIndicator}>
                                        <span></span>
                                        <span></span>
                                        <span></span>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className={styles.chatInput}>
                        <button
                            className={`${styles.voiceButton} ${isRecording ? styles.recording : ''}`}
                            onClick={toggleRecording}
                            title={isRecording ? "Stop recording" : "Start voice input"}
                        >
                            {isRecording ? '⏹️' : '🎤'}
                        </button>
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder={isRecording ? "Listening..." : "Ask me anything..."}
                            disabled={loading}
                        />
                        <button
                            onClick={handleSend}
                            disabled={loading || !input.trim()}
                            className={styles.sendButton}
                        >
                            {loading ? '⏳' : '➤'}
                        </button>
                    </div>
                </div>
            )}
        </>
    );
}
