from flask import Flask, request, jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import psycopg2
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    try:
        conn = psycopg2.connect(
            database="booktown_db",  
            user="postgres",  
            password="1234",  
            host="127.0.0.1",  
            port="5432"  
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/api/signin', methods=['POST'])
def sign_in():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')
    user_type = data.get('userType')  

    if not username or not password or not confirm_password or not user_type:
        return jsonify({"message": "Missing required fields"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    table = 'sellers' if user_type == 'seller' else 'buyers'

    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {table} WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            return jsonify({"message": "Username already exists"}), 400

        cursor.execute(f"INSERT INTO {table} (username, password) VALUES (%s, %s)", (username, hashed_password))

        connection.commit()

        return jsonify({"message": f"{user_type.capitalize()} registered successfully"}), 201
    except Exception as e:
        print(f"Sign-in error: {e}")
        return jsonify({"message": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('userType')  

    if not username or not password or not user_type:
        return jsonify({"message": "Missing required fields"}), 400

    table = 'sellers' if user_type == 'seller' else 'buyers'

    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor()

        cursor.execute(f"SELECT password FROM {table} WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result and check_password_hash(result[0], password):
            return jsonify({"message": f"{user_type.capitalize()} login successful"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"message": str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor:  # Ensure cursor exists and is valid
            cursor.close()
        if 'connection' in locals() and connection:  # Ensure connection exists
            connection.close()

@app.route('/api/seller', methods=['POST'])
def seller():
    data = request.form
    email = data.get('SellerEmail')
    state = data.get('state')
    book_name = data.get('bookName')
    author = data.get('author')
    rental_period = data.get('rentalPeriod')
    city = data.get('city')
    print_run_number = data.get('printRunNumber')
    paperback_type = data.get('paperbackType')

    print("Received data:", data)

    if not book_name or not author or not rental_period or not city or not state:
        return jsonify({"message": "Missing required fields"}), 400

    if state == 'Collectible':
        if not print_run_number or not paperback_type:
            return jsonify({"message": "Print Run Number and Paperback Type are required for Collectible state"}), 400
        
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        cursor = connection.cursor()

        cursor.execute(""" 
            INSERT INTO books (seller_email, book_name, author, rental_period, seller_city, state_of_book, print_run_number, paperback_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            email,
            book_name, 
            author, 
            rental_period, 
            city, 
            state, 
            print_run_number if state == 'Collectible' else None,  
            paperback_type if state == 'Collectible' else None  
        ))

        connection.commit()

        return jsonify({"message": "Book details saved successfully"}), 201

    except Exception as e:
        print(f"Seller endpoint error: {e}")
        return jsonify({"message": str(e)}), 500
    
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"message": "Database connection failed"}), 500

        with connection.cursor() as cursor:
            query = """
            SELECT book_name, author, rental_period, seller_city, state_of_book, seller_email, print_run_number, paperback_type
            FROM books
            """
            cursor.execute(query)
            books = cursor.fetchall()

        if not books:
            return jsonify({"message": "No books found", "books": []}), 200

        book_list = [
            {
                "bookName": book[0] if book[0] is not None else "No Title Provided",  
                "author": book[1] if book[1] is not None else "Unknown Author",      
                "rentalPeriod": book[2] if book[2] is not None else "Not Specified",  
                "city": book[3] if book[3] is not None else "Not Provided",         
                "state": book[4] if book[4] is not None else "Not Mentioned",        
                "sellerEmail": book[5] if book[5] is not None else "Unknown Seller", 
                "printRunNumber": book[6] if book[6] is not None else "",            
                "paperbackType": book[7] if book[7] is not None else "",            
            }
            for book in books
        ]

        return jsonify({"books": book_list}), 200

    except Exception as e:
        print(f"Error fetching books: {e}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500

    finally:
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        data = request.form
        seller_email = data['sellerEmail']  
        book_name = data['bookName']
        author = data['author']
        rental_period = data['rentalPeriod']
        city = data['city']
        state = data['state']
        print_run_number = data.get('printRunNumber')
        paperback_type = data.get('paperbackType')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books 
            (book_name, author, rental_period, seller_city, state_of_book, seller_email, print_run_number, paperback_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (book_name, author, rental_period, city, state, seller_email, 
            print_run_number if state == 'Collectible' else None, 
            paperback_type if state == 'Collectible' else None))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Book details submitted successfully!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to submit book details"}), 500


@app.route('/api/events', methods=['POST'])
def add_event():
    try:
        data = request.json
        event_name = data['eventName']
        event_description = data['eventDescription']
        event_location = data['eventLocation']
        date_input = data['date']  
        timings = data['timings']

        try:
            formatted_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Expected yyyy-mm-dd.'}), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(""" 
                    INSERT INTO events (event_name, event_description, event_location, date, timings)
                    VALUES (%s, %s, %s, %s, %s);
                """, (event_name, event_description, event_location, formatted_date, timings))
                conn.commit()
        return jsonify({'message': 'Event added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(""" 
                    SELECT event_name, event_description, event_location, date, timings
                    FROM events;
                """)
                events = cursor.fetchall()
                formatted_events = [{
                    'eventName': event[0],
                    'eventDescription': event[1],
                    'eventLocation': event[2],
                    'date': event[3].strftime('%Y-%m-%d'),  
                    'timings': event[4]
                } for event in events]
                return jsonify(formatted_events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':

        try:
            data = request.json
            book_name = data['bookName']
            author = data['author']
            review = data['review']
            rating = data['rating']

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO reviews (book_name, author, review, rating)
                        VALUES (%s, %s, %s, %s);
                    """, (book_name, author, review, rating))
                    conn.commit()
            return jsonify({'message': 'Review added successfully!'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'GET':
        
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT book_name, author, review, rating FROM reviews;")
                    reviews = cursor.fetchall()
                    reviews_list = [{'book_name': review[0], 'author': review[1], 'review': review[2], 'rating': review[3]} for review in reviews]
            return jsonify(reviews_list), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
