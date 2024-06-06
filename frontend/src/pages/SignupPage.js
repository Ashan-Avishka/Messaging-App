import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '../services/api';

const SignupPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await signup({ username, email, password });
      const userData = response.data.message;

      if(userData == 'User created successfully') {
        navigate('/login');
      }
      // Handle success (e.g., redirect to login)
     
    } catch (error) {
      // Handle error
      console.error('Signup failed', error);
    }
  };

  const goToLogin = () => {
    navigate('/login'); // Navigate to the signup page
  };

  return (
    <div>
      <h2>Signup</h2>
      <form onSubmit={handleSignup}>
      <div>
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Signup</button>
      </form>
      <button onClick={goToLogin}>Back to Login</button>
    </div>
  );
};

export default SignupPage;
