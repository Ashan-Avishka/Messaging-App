import React, { useState } from 'react';
import {useNavigate } from 'react-router-dom';
import PrimaryBtn from '../components/PrimaryBtn';
import { login } from '../services/api';
import { Button, Container } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEnvelope, faLock } from '@fortawesome/free-solid-svg-icons';
import './styles/LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await login({ email, password });

      if(response.data.message === 'Login successful'){
        const userData = response.data.user;
        localStorage.setItem('user', JSON.stringify(userData));
      
        navigate('/chat');
      }
      
    } catch (error) {
      // Handle error
      console.error('Login failed', error);
    }
  };

  const goToSignup = () => {
    navigate('/signup'); 
  };

  return (
    <div className='containter-login'>
      <div className='content-login'>
        <h2>User Login</h2><br></br>

        <form onSubmit={handleLogin}>
          <div class="input-group mb-3">
            <span class="input-group-text"><FontAwesomeIcon icon={faEnvelope} /></span>
            <input type="email" class="form-control" value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Email' required />
          </div>

          <div class="input-group mb-3">
            <span class="input-group-text"><FontAwesomeIcon icon={faLock} /></span>
            <input type="password" class="form-control" value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Password' required />
          </div>
          <PrimaryBtn className='primary-btn' type="submit" text={'Login'}></PrimaryBtn>
        </form><br/>

        <p>If you haven't a account please create a new account</p>
        <PrimaryBtn text={'Go to Signup'} className='secondary-btn' onClick={goToSignup}></PrimaryBtn>
      </div>
    </div>
  );
};

export default LoginPage;
