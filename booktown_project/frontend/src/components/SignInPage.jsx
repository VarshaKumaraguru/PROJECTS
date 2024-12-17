import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import './Auth.css';

const SignUpPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const isSeller = location.pathname.includes('seller');
  const userType = isSeller ? 'seller' : 'buyer'; 

  const handleSignUp = async (e) => {
    e.preventDefault();
    setSuccessMessage('');
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/api/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          confirmPassword,
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
        setError(result.message || 'Sign-Up failed');
      }
    } catch (err) {
      setError('Error connecting to the server');
    }
  };

  return (
    <div className="auth-container">
      <h1>{isSeller ? 'Seller Sign Up' : 'Buyer Sign Up'}</h1>
      <form className="auth-form" onSubmit={handleSignUp}>
        <label>{isSeller ? 'Seller Username' : 'Buyer Username'}</label>
        <input
          type="text"
          placeholder={`Enter your ${isSeller ? 'seller' : 'buyer'} username`}
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

        <label>Confirm Password</label>
        <input
          type="password"
          placeholder="Confirm your password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        {error && <p className="error-message">{error}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <button type="submit">{isSeller ? 'Seller Sign Up' : 'Buyer Sign Up'}</button>
      </form>

      <div className="auth-footer">
        <p>
          Already have an account?{' '}
          <Link to={`/login?userType=${isSeller ? 'seller' : 'buyer'}`}>
            {isSeller ? 'Seller Login' : 'Buyer Login'}
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignUpPage;
