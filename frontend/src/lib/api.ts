import axios from 'axios';

// In production, Next.js rewrites /api/* → backend via next.config.js
// In dev, falls back to direct localhost:8000
const BASE_URL =
  typeof window !== 'undefined'
    ? ''  // browser: use relative URLs (Next.js rewrites handle routing)
    : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error(`API Error ${error.response.status}:`, error.response.data);
    } else if (error.request) {
      console.error('API no response — backend offline?', error.message);
    }
    return Promise.reject(error);
  }
);
