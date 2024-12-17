import React, { useState } from 'react';
import './SellerInterface.css';
import logo from "../assets/images/BookTown.png";

const SellerInterface = () => {
  const [state, setState] = useState('Standard');
  const [bookDetails, setBookDetails] = useState({
    sellerEmail: '',  
    bookName: '',
    author: '',
    rentalPeriod: '',
    city: '',
    printRunNumber: '',
    paperbackType: '',
  });
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBookDetails({ ...bookDetails, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    if (!bookDetails.sellerEmail || !bookDetails.bookName || !bookDetails.author || !bookDetails.city || !bookDetails.rentalPeriod) {
      setError("All required fields must be filled!");
      return;
    }

    if (state === 'Collectible' && (!bookDetails.printRunNumber || !bookDetails.paperbackType)) {
      setError("Print Run Number and Paperback Type are required for Collectible books");
      return;
    }

    const formData = new FormData();
    formData.append('sellerEmail', bookDetails.sellerEmail);  
    formData.append('bookName', bookDetails.bookName);
    formData.append('author', bookDetails.author);
    formData.append('rentalPeriod', bookDetails.rentalPeriod);
    formData.append('city', bookDetails.city);
    formData.append('state', state);

    if (state === 'Collectible') {
      formData.append('printRunNumber', bookDetails.printRunNumber);
      formData.append('paperbackType', bookDetails.paperbackType);
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/add_book', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setSuccessMessage(result.message);
        setTimeout(() => {
          alert('Book details submitted successfully!');
          setBookDetails({
            sellerEmail: '',  
            bookName: '',
            author: '',
            rentalPeriod: '',
            city: '',
            printRunNumber: '',
            paperbackType: '',
          });
          setState('Standard');
        }, 1000);
      } else {
        setError(result.message || 'Failed to submit book details');
      }
    } catch (error) {
      console.error('Error submitting book details:', error);
      setError('There was an error submitting the book details');
    }
  };

  return (
    <div className="seller-interface">
      <nav className="navbar">
        <img src={logo} alt="Logo" className="logo" />
        <div className="nav-buttons">
          <button onClick={() => window.location.href = '/events'}>Upcoming Events</button>
          <button onClick={() => window.location.href = '/reviews'}>Reviews</button>
          <button onClick={() => window.location.href = '/'}>Home</button>
          <button onClick={() => window.location.href = '/'}>Logout</button>
        </div>
      </nav>

      <div className="form-container">
        <h2>Enter Book Details</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Seller's Email:
            <input 
              type="email" 
              name="sellerEmail" 
              value={bookDetails.sellerEmail} 
              onChange={handleChange} 
              required 
            />
          </label>

          <label>
            Book Name:
            <input 
              type="text" 
              name="bookName" 
              value={bookDetails.bookName} 
              onChange={handleChange} 
              required 
            />
          </label>

          <label>
            Author:
            <input 
              type="text" 
              name="author" 
              value={bookDetails.author} 
              onChange={handleChange} 
              required 
            />
          </label>

          <label>
            Rental Period:
            <input 
              type="text" 
              name="rentalPeriod" 
              value={bookDetails.rentalPeriod} 
              onChange={handleChange} 
              required 
            />
          </label>

          <label>
            Seller's City:
            <input 
              type="text" 
              name="city" 
              value={bookDetails.city} 
              onChange={handleChange} 
              required 
            />
          </label>

          <label>
            State of the Book:
            <select 
              name="state" 
              value={state} 
              onChange={(e) => setState(e.target.value)}
            >
              <option value="Standard">Standard</option>
              <option value="Collectible">Collectible</option>
            </select>
          </label>

          {state === 'Collectible' && (
            <>
              <label>
                Print Run Number:
                <input 
                  type="text" 
                  name="printRunNumber" 
                  value={bookDetails.printRunNumber} 
                  onChange={handleChange} 
                  required 
                />
              </label>

              <label>
                Paperback Type:
                <input 
                  type="text" 
                  name="paperbackType" 
                  value={bookDetails.paperbackType} 
                  onChange={handleChange} 
                  required 
                />
              </label>
            </>
          )}

          {error && <p className="error-message">{error}</p>}
          {successMessage && <p className="success-message">{successMessage}</p>}

          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
};

export default SellerInterface;
