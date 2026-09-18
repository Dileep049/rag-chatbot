import axios from 'axios';

const API_ROOT = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_BASE = `${API_ROOT}/api`;

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor attaching Bearer token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('citizen_admin_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const loginAdmin = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

export const checkAdminStatus = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const askChat = async (question, category = null, history = []) => {
  const payload = { question };
  if (category && category !== 'all') {
    payload.category = category;
  } else {
    payload.category = null;
  }
  
  if (history && history.length > 0) {
    payload.history = history.map(h => ({
      role: h.sender === 'user' ? 'user' : 'assistant',
      content: h.text
    }));
  }

  const response = await api.post('/chat', payload);
  return response.data;
};

export const getCategories = async () => {
  const response = await api.get('/categories');
  return response.data;
};

export const getDocuments = async () => {
  const response = await api.get('/documents');
  return response.data;
};

export const uploadDocument = async (file, category, overwrite = false) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('category', category);
  formData.append('overwrite', overwrite ? 'true' : 'false');

  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const deleteDocument = async (documentName) => {
  const response = await api.delete(`/documents/${encodeURIComponent(documentName)}`);
  return response.data;
};

export const reindexSingleDocument = async (documentName) => {
  const response = await api.post(`/documents/reindex/${encodeURIComponent(documentName)}`);
  return response.data;
};

export const reindexDocuments = async () => {
  const response = await api.post('/documents/reindex-all');
  return response.data;
};

export default api;
