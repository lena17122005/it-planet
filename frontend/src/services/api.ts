import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status !== 401) {
      return Promise.reject(error);
    }

    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      return Promise.reject(error);
    }

    try {
      const refreshResponse = await axios.post(`${baseURL}/api/v1/auth/refresh`, { refresh_token: refreshToken });
      localStorage.setItem('access_token', refreshResponse.data.access_token);
      localStorage.setItem('refresh_token', refreshResponse.data.refresh_token);
      error.config.headers.Authorization = `Bearer ${refreshResponse.data.access_token}`;
      return apiClient.request(error.config);
    } catch (refreshError) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return Promise.reject(refreshError);
    }
  }
);
