import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api'; // Change to your Flask API URL

export const signup = async (userData) => {
  return axios.post(`${API_URL}/signup`, userData);
};

export const login = async (userData) => {
  return axios.post(`${API_URL}/login`, userData);
};

export const getMessages = async () => {
  return axios.get(`${API_URL}/messages`);
};

export const sendMessage = async (message) => {
  return axios.post(`${API_URL}/messages`, message);
};
