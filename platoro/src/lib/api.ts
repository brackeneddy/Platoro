import axios from 'axios';

const BASE_URL = 'https://jz9dh44oaj.execute-api.us-east-1.amazonaws.com/dev';

// Add Axios interceptor for token injection
axios.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('platoro_token');
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
  }
  return config;
});

export const signup = async (name: string, email: string, password: string) => {
  try {
    const response = await axios.post(`${BASE_URL}/account/signup`, {
      name,
      email,
      password,
    });
    return response.data;
  } catch (error: any) {
    console.error('Signup error:', error.response?.data || error.message);
    throw error;
  }
};

export const login = async (email: string, password: string) => {
  try {
    const response = await axios.post(`${BASE_URL}/account/login`, {
      email,
      password,
    });
    return response.data;
  } catch (error: any) {
    console.error('Login error:', error.response?.data || error.message);
    throw error;
  }
};
