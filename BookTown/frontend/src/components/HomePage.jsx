import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import logo from '../assets/images/BookTown.png'; 
function HomePage() {
  const navigate = useNavigate(); 

  return (
    <div className="home-page">
      <div className="content-container">
        <div className="heading-container">
          <h1 className="kaushan-script-regular">Welcome to Booktown</h1>
          <h2 className="kaushan-script-regular">
            The place where every book has a story, and every story finds its reader
          </h2>
        </div>

        <div className="button-container">
          <button
            className="home-button"
            onClick={() => navigate('/sign-in/seller')}>Seller</button>
          <button
            className="home-button"
            onClick={() => navigate('/sign-in/buyer')}>Buyer</button>
        </div>
      </div>

      <footer className="footer">
        <div className="footer-container">
          <div className="footer-logo">
            <img src={logo} alt="Booktown Logo" />
          </div>

          <div className="footer-about">
            <h3>About Booktown</h3>
            <p>
            Booktown is a platform where book lovers can lend books—both standard and collectible editions.
            Discover upcoming book events, connect with readers, and write reviews for your favorite books.
            </p>
          </div>

          <div className="footer-contact">
            <h3>Contact Us</h3>
            <p>Email: support@booktown.com</p>
            <p>Phone: +1 234 567 890</p>
            <p>Address: 123 Book Lane, Storyville, 45678</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default HomePage;
