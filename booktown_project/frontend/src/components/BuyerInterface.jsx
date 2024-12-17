import React, { useEffect, useState } from 'react';
import './BuyerInterface.css';
import logo from "../assets/images/BookTown.png";

const BuyerInterface = () => {
  const [books, setBooks] = useState([]); 
  const [filteredBooks, setFilteredBooks] = useState([]); 
  const [searchQuery, setSearchQuery] = useState(''); 
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/books');
        const data = await response.json();

        if (response.ok) {
          setBooks(data.books || []); 
          setFilteredBooks(data.books || []); 
        } else {
          setError(data.message || 'Failed to fetch books');
        }
      } catch (err) {
        console.error('Error fetching books:', err);
        setError('There was an error fetching the books');
      }
    };

    fetchBooks();
  }, []);

  const handleSearch = (event) => {
    const query = event.target.value.toLowerCase();
    setSearchQuery(query);
    const filtered = books.filter((book) =>
      book.bookName.toLowerCase().includes(query)
    );
    setFilteredBooks(filtered);
  };

  return (
    <div className="buyer-interface">
      <nav className="navbar">
        <div className="logo">
          <img src={logo} alt="Logo" />
        </div>
        <div className="navbar-buttons">
          <button onClick={() => window.location.href = '/events'}>Upcoming Events</button>
          <button onClick={() => window.location.href = '/'}>Home</button>
          <button onClick={() => window.location.href = '/'}>Logout</button>
          <button onClick={() => window.location.href = '/reviews'}>Reviews</button>
        </div>
      
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search for books..."
            value={searchQuery}
            onChange={handleSearch}
          />
        </div>
      </nav>

      <h1>Available Books</h1>
      {error && <p className="error-message">{error}</p>}
      <div className="book-grid">
        {filteredBooks.length === 0 && !error && <p>No books available</p>}
        {filteredBooks.map((book, index) => (
          <div className="book-card" key={index}>
            <h2>{book.bookName || 'No Title Provided'}</h2>
            <p><strong>Author:</strong> {book.author || 'Unknown Author'}</p>
            <p><strong>Seller Email:</strong> {book.sellerEmail || 'Unknown Seller'}</p>
            <p><strong>Rental Period:</strong> {book.rentalPeriod || 'Not Specified'}</p>
            <p><strong>City:</strong> {book.city || 'Not Provided'}</p>
            <p><strong>State:</strong> {book.state || 'Not Mentioned'}</p>
            {book.state === 'Collectible' && (
              <>
                <p><strong>Print Run Number:</strong> {book.printRunNumber || 'N/A'}</p>
                <p><strong>Paperback Type:</strong> {book.paperbackType || 'N/A'}</p>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BuyerInterface;