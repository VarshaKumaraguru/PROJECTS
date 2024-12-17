import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './EventsPage.css';
import logo from "../assets/images/BookTown.png";

const EventsPage = () => {
  const [isFormVisible, setFormVisible] = useState(false);
  const [events, setEvents] = useState([]);
  const [formData, setFormData] = useState({
    eventName: '',
    eventDescription: '',
    eventLocation: '',
    date: '',
    timings: ''
  });

  useEffect(() => {
    axios.get('http://localhost:5000/api/events')
      .then(response => setEvents(response.data))
      .catch(error => console.error('Error fetching events:', error));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const formattedDate = new Date(formData.date).toISOString().split('T')[0];
    const eventData = {
      ...formData,
      date: formattedDate,
    };

    axios.post('http://localhost:5000/api/events', eventData)
      .then(response => {
        setEvents([...events, eventData]);
        setFormData({ eventName: '', eventDescription: '', eventLocation: '', date: '', timings: '' });
        setFormVisible(false); 
      })
      .catch(error => console.error('Error adding event:', error));
  };

  return (
    <div className="events-page">
      <nav className="navbar">
        <img src={logo} alt="Logo" className="logo" />
        <button className="upload-event-button" onClick={() => setFormVisible(!isFormVisible)}>
          {isFormVisible ? 'Close Form' : 'Upload Event'}
        </button>
        {isFormVisible && (
          <form className="event-form" onSubmit={handleFormSubmit}>
            <input
              type="text"
              name="eventName"
              placeholder="Event Name"
              value={formData.eventName}
              onChange={handleInputChange}
              required
            />
            <input
              type="text"
              name="eventDescription"
              placeholder="Event Description"
              value={formData.eventDescription}
              onChange={handleInputChange}
              required
            />
            <input
              type="text"
              name="eventLocation"
              placeholder="Event Location"
              value={formData.eventLocation}
              onChange={handleInputChange}
              required
            />
            <input
              type="date"
              name="date"
              placeholder="Event Date"
              value={formData.date}
              onChange={handleInputChange}
              required
            />
            <input
              type="text"
              name="timings"
              placeholder="Event Timings (e.g., 4:30pm-9:30pm)"
              value={formData.timings}
              onChange={handleInputChange}
              required
            />
            <button type="submit">Submit</button>
          </form>
        )}
      </nav>

      <h1 className="events-heading">Events</h1>

      <div className="event-cards">
        {events.map((event, index) => (
          <div className="event-card" key={index}>
            <h3>{event.eventName}</h3> 
            <p><strong>Description:</strong> {event.eventDescription}</p> 
            <p><strong>Date:</strong> {new Date(event.date).toLocaleDateString()}</p> 
            <p><strong>Timings:</strong> {event.timings}</p> 
            <p><strong>Location:</strong> {event.eventLocation}</p> 
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventsPage;
