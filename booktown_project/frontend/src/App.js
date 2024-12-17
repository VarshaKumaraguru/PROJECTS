import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage'; 
import SignInPage from './components/SignInPage'; 
import LoginPage from './components/LoginPage';
import SellerInterface from './components/SellerInterface';
import BuyerInterface from './components/BuyerInterface';
import EventsPage from './components/EventsPage';
import ReviewPage from './components/ReviewPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} /> 
        <Route path="/sign-in/:userType" element={<SignInPage />} /> 
        <Route path="/login" element={<LoginPage />} />
        <Route path="/seller-interface" element={<SellerInterface />} />
        <Route path="/buyer-interface" element={<BuyerInterface />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/reviews" element={<ReviewPage />} />

      </Routes>
    </Router>
  );
};

export default App;