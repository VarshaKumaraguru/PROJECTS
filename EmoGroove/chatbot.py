from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pwd@localhost/emogroove_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
     __tablename__ = "users"
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), unique=True, nullable=False)
     password = db.Column(db.String(200), nullable=False)

model = load_model(r'models\emotion_model.h5')
with open(r'models\tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open(r'models\label_encoder.pkl', 'rb') as handle:
    label_encoder = pickle.load(handle)


max_length = 100

client_id = ''
client_secret = ''
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def recommend_songs(emotion, language):
    emotion_to_playlist = {
        'joy': {'english': 'Happy Pop Hits', 'tamil': 'VIBE Panlaama', 'hindi': 'Bollywood Dance Music',
                'malayalam': 'Malayalam Chill Mix', 'telugu': 'DSP Dance Hits'},
        'sadness': {'english': 'Life Sucks', 'tamil': 'Sad Melodies Tamil', 'hindi': 'Sad Hindi Melodies',
                    'malayalam': 'Feel Good Malayalam', 'telugu': 'Sad Melodies Telugu'},
        'anger': {'english': 'Rage Beats', 'tamil': 'Fight Mood Tamil', 'hindi': 'Bollywood Workout',
                  'malayalam': 'Hip Hop Malayalam', 'telugu': 'Kiraak Telugu'},
        'love': {'english': 'Love Pop', 'tamil': 'Kaadhal Theeye', 'hindi': 'Bollywood Mush',
                 'malayalam': 'Romantic Malayalam', 'telugu': 'Purely Prema'},
        'fear': {'english': 'Chill Vibes', 'tamil': 'Iniya Iravu', 'hindi': 'Bollywood & Chill',
                 'malayalam': 'Malayalam Chill Mix', 'telugu': 'Mellow Telugu'},
        'surprise': {'english': 'Feel Good Indie', 'tamil': 'VIBE Panlaama', 'hindi': 'Happy Vibes',
                     'malayalam': 'Happy Vibes Malayalam', 'telugu': 'Feel Good Telugu'}
    }
    playlist_name = emotion_to_playlist.get(emotion, {}).get(language, 'mood booster')
    try:
        results = sp.search(q=playlist_name, type='playlist', limit=1)
        if results['playlists']['items']:
            playlist_id = results['playlists']['items'][0]['id']
            tracks = sp.playlist_tracks(playlist_id)
            song_recommendations = [
                f"{track['track']['name']} by {track['track']['artists'][0]['name']} - [Listen on Spotify]({track['track']['external_urls']['spotify']})"
                for track in tracks['items'] if track['track']
            ]
            return song_recommendations[:15]
        return ["No playlist recommendations available."]
    except Exception as e:
        print(f"Error: {e}")
        return ["Error connecting to Spotify or fetching songs."]


def predict_emotion_and_recommend_songs(text, language):
    input_sequence = tokenizer.texts_to_sequences([text])
    padded_input_sequence = pad_sequences(input_sequence, maxlen=max_length)
    prediction = model.predict(padded_input_sequence)
    predicted_label = np.argmax(prediction)
    emotion = label_encoder.inverse_transform([predicted_label])[0]
    songs = recommend_songs(emotion, language)
    return emotion, songs


@app.route('/')
def home():
    """Redirect to signup page initially."""
    if 'username' in session:
        # If user is already logged in, redirect to index/dashboard
        return redirect(url_for('index'))
    return redirect(url_for('signup'))

@app.route('/about')
def about():
    """Render the about section in the index.html template."""
    return render_template('index.html', section='about')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            print(f"Error during signup: {e}")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/index')
def index():
    """Render the homepage after login."""
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    flash('Please log in to access the homepage.', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))  


@app.route('/chat', methods=['GET'])
def chat_page():
    """Render the chat page."""
    if 'username' in session:
        return render_template('chat.html', username=session['username'])
    flash('Please log in to access the chat.', 'error')
    return redirect(url_for('login'))


@app.route('/chat', methods=['POST'])
def chat():
    """Handle the chat functionality to process user input."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input, JSON data is required'}), 400

        text = data.get('text')
        language = data.get('language')

        if not text or not language:
            return jsonify({'error': 'Both "text" and "language" are required'}), 400

        print(f"User Input Text: {text}")
        print(f"Selected Language: {language}")
        emotion, songs = predict_emotion_and_recommend_songs(text, language)
        return jsonify({'emotion': emotion, 'songs': songs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
