import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api'; 
axios.defaults.withCredentials = true;

export const signup = async (userData) => {
  return await axios.post(`${API_URL}/signup`, userData);
};

export const login = async (userData) => {
  return await axios.post(`${API_URL}/login`, userData);
};

export const getUsers = async () => {
  return await axios.get(`${API_URL}/users`);
};

export const getMessages = async (chatId) => {
  return await axios.post(`${API_URL}/messages/decrypt`, { receiver: chatId });
};

export const sendMessage = async (message) => {
  console.log(message);
  return await axios.post(`${API_URL}/messages`, message);
};