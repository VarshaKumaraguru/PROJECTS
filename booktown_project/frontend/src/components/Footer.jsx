import React from 'react';
import './Footer.css';  // Import the CSS file for styling

const Footer = () => {
  return (
    <footer id="footer">
      <div className="footer-container">
        <div className="footer-logo">
          <img src="../static/images/logo.png" alt="EmoGroove Logo" />
        </div>

        <div id="about-section" className="footer-about">
          <h3>About EmoGroove</h3>
          <p>
            EmoGroove is your personalized music companion, helping you discover songs that resonate with your emotions in multiple languages. Feel the beat, find your mood!
          </p>
        </div>

        <div id="contact-section" className="footer-contact">
          <h3>Contact Us</h3>
          <p>Email: support@emogroove.com</p>
          <p>Phone: +1 234 567 890</p>
          <p>Address: 123 Music Lane, Melody City, 45678</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
