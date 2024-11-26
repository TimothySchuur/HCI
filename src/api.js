import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', // Base URL for the Flask backend
  headers: {
    'Content-Type': 'application/json',
  },
});

// Fetch data example
export const fetchData = async () => {
  return apiClient.get('/data');
};

// Submit data example
export const submitData = async (data) => {
  return apiClient.post('/submit', data);
};

// Register user
export const registerUser = async (userData) => {
  return apiClient.post('/register', userData);
};

// Login user
export const loginUser = async (credentials) => {
  return apiClient.post('/login', credentials);
};

export default {
  fetchData,
  submitData,
  registerUser,
  loginUser,
};
