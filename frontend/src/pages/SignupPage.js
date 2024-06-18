import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PrimaryBtn from '../components/PrimaryBtn';
import { signup } from '../services/api';
import { Button, Container } from 'react-bootstrap';
import './styles/SignupPage.css';

const SignupPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [conpassword, setConPassword] = useState('');
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
    <div className='containter-signup'>
      <div className='content-signup'>
      <h2>Create an Account</h2><br/>
      <form onSubmit={handleSignup}>

        <div class="input-group mb-3">
          <input type="text" class="form-control" value={username} onChange={(e) => setUsername(e.target.value)} placeholder='Username' required />
        </div>

        <div class="input-group mb-3">
          <input type="email" class="form-control" value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Email' required />
        </div>

        <div class="input-group mb-3">
          <input type="password" class="form-control" value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Password' required />
        </div>

        <div class="input-group mb-3">
          <input type="password" class="form-control" value={conpassword} onChange={(e) => setConPassword(e.target.value)} placeholder='Confirm Password' required />
        </div><br/>

        <PrimaryBtn text={'Back to Login'} className='secondary-btn gap' onClick={goToLogin}>Back to Login</PrimaryBtn>
        <PrimaryBtn type="submit" className='primary-btn' text={'Signup'}></PrimaryBtn>
      </form>
      
    </div>
    </div>
  );
};

export default SignupPage;
