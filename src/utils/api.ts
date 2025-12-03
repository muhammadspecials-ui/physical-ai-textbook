import axios from 'axios';

// Use hardcoded localhost for development, or window location origin
const API_URL = typeof window !== 'undefined'
  ? (window.location.hostname === 'localhost' ? 'http://localhost:8000' : window.location.origin)
  : 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  signup: async (data: {
    email: string;
    name: string;
    password: string;
    software_experience: string;
    hardware_experience: string;
  }) => {
    const response = await api.post('/api/auth/signup', data);
    if (response.data.token && typeof window !== 'undefined') {
      localStorage.setItem('auth_token', response.data.token);
    }
    return response.data;
  },

  login: async (data: { email: string; password: string }) => {
    const response = await api.post('/api/auth/login', data);
    if (response.data.token && typeof window !== 'undefined') {
      localStorage.setItem('auth_token', response.data.token);
    }
    return response.data;
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  },

  getMe: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

// Chat API
export const chatAPI = {
  sendMessage: async (data: {
    question: string;
    selected_text?: string;
    session_id?: string;
  }) => {
    const response = await api.post('/api/chat', data);
    return response.data;
  },
};

// Content API
export const contentAPI = {
  personalize: async (data: { content: string; page_path: string }) => {
    const response = await api.post('/api/personalize', data);
    return response.data;
  },

  translate: async (data: { content: string }) => {
    const response = await api.post('/api/translate', data);
    return response.data;
  },
};

export default api;
