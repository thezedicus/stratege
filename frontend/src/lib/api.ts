import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
});

apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error('API Error:', err.response?.data || err.message);
    return Promise.reject(err);
  }
);

export type AnalysisInput = {
  activityType: string;
  budget: number;
  monthlyBudget: number;
  goal: string;
  maturity: string;
  websiteUrl?: string;
};
