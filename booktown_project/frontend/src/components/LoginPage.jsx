import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Auth.css';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const userType = queryParams.get('userType') || 'buyer'; 

  const handleLogin = async (e) => {
    e.preventDefault();
    setSuccessMessage('');
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          userType, 
        }),
      });
  
      const result = await response.json();
  
      if (response.ok) {
        localStorage.setItem('username', username);
        localStorage.setItem('userType', userType);
  
        setSuccessMessage(result.message);
        setTimeout(() => {
          if (userType === 'seller') {
            navigate('/seller-interface');
          } else {
            navigate('/buyer-interface');
          }
        }, 1000);
      } else {
        setError(result.message || 'Login failed');
      }
    } catch (err) {
      setError('Error connecting to the server');
    }
  };

  return (
    <div className="auth-container">
      <h1>{userType === 'seller' ? 'Seller Login' : 'Buyer Login'}</h1>
      <form className="auth-form" onSubmit={handleLogin}>
        <label>Username</label>
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label>Password</label>
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && <p className="error-message">{error}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <button type="submit">Log In</button>
      </form>
    </div>
  );
};

export default LoginPage;