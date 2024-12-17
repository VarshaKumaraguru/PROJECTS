import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ReviewPage.css';
import logo from "../assets/images/BookTown.png";

const ReviewsPage = () => {
  const [isFormVisible, setFormVisible] = useState(false);
  const [reviews, setReviews] = useState([]);
  const [formData, setFormData] = useState({
    bookName: '',
    author: '',
    review: '',
    rating: ''
  });

  useEffect(() => {
    axios.get('http://localhost:5000/api/reviews')
      .then(response => setReviews(response.data))
      .catch(error => console.error('Error fetching reviews:', error));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();

    const reviewData = {
      ...formData
    };

    axios.post('http://localhost:5000/api/reviews', reviewData)
      .then(response => {
        setReviews([...reviews, reviewData]);
        setFormData({ bookName: '', author: '', review: '', rating: '' });
        setFormVisible(false); 
      })
      .catch(error => console.error('Error adding review:', error));
  };

  return (
    <div className="reviews-page">
      <nav className="navbar">
        <img src={logo} alt="Logo" className="logo" />
        <button className="write-review-button" onClick={() => setFormVisible(!isFormVisible)}>
          {isFormVisible ? 'Close Form' : 'Write a Review'}
        </button>
        {isFormVisible && (
          <form className="review-form" onSubmit={handleFormSubmit}>
            <input
              type="text"
              name="bookName"
              placeholder="Book Name"
              value={formData.bookName}
              onChange={handleInputChange}
              required
            />
            <input
              type="text"
              name="author"
              placeholder="Author"
              value={formData.author}
              onChange={handleInputChange}
              required
            />
            <textarea
              name="review"
              placeholder="Write your review"
              value={formData.review}
              onChange={handleInputChange}
              required
            />
            <input
              type="number"
              name="rating"
              placeholder="Rating (1-5)"
              value={formData.rating}
              onChange={handleInputChange}
              required
              min="1"
              max="5"
            />
            <button type="submit">Submit</button>
          </form>
        )}
      </nav>

      <h1 className="events-heading">Reviews</h1>

      <div className="review-cards">
        {reviews.map((review, index) => (
          <div className="review-card" key={index}>
            <h3>{review.book_name}</h3>
            <p><strong>Author:</strong> {review.author}</p>
            <p><strong>Review:</strong> {review.review}</p>
            <p><strong>Rating:</strong> {review.rating} / 5</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReviewsPage;