import React, { useState } from 'react';
import {useNavigate } from 'react-router-dom';
import { login } from '../services/api';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await login({ email, password });
      // Handle success (e.g., store token, redirect)
      const userData = response.data.user;
      localStorage.setItem('user', JSON.stringify(userData));
      
      navigate('/chat');
    } catch (error) {
      // Handle error
      console.error('Login failed', error);
    }
  };

  const goToSignup = () => {
    navigate('/signup'); // Navigate to the signup page
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Login</button>
      </form>
      <button onClick={goToSignup}>Go to Signup</button>
    </div>
  );
};

export default LoginPage;
