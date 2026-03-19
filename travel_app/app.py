from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import datetime
import mysql.connector
from flask_bcrypt import Bcrypt
from functools import wraps
# import time # Removed for instant frontend feedback

app = Flask(__name__)
app.secret_key = 'e26c9a48944af098a95c3183cff7e327e3996acf3ddcd1e7ab2570c1ec84b27c' # !!! IMPORTANT: CHANGE THIS TO A STRONG, UNIQUE KEY !!!
bcrypt = Bcrypt(app)

# --- MySQL Database Configuration for XAMPP ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # XAMPP's root user usually has NO PASSWORD by default
    'database': 'travel_booker_db'
}

# Function to get a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        print("DEBUG: Successfully connected to MySQL database.")
        return conn
    except mysql.connector.Error as err:
        print(f"ERROR: Error connecting to MySQL: {err}")
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied: Check your username and password in db_config.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{db_config['database']}' does not exist. Did you create it in phpMyAdmin?")
        elif err.errno == mysql.connector.errorcode.CR_CONN_ERROR:
            print("Connection error: Is XAMPP's MySQL/MariaDB server running?")
        return None

# --- Dummy Data (Keep this as is for initial search results) ---
flights = [
    {"id": "F001", "airline": "Air India", "origin": "MAA", "destination": "DEL", "departure": "2025-07-10 08:00", "arrival": "2025-07-10 11:00", "price": 4500, "available_seats": 50},
    {"id": "F002", "airline": "IndiGo", "origin": "DEL", "destination": "MAA", "departure": "2025-07-10 10:00", "arrival": "2025-07-10 13:00", "price": 4200, "seats_available": 60},
    {"id": "F003", "airline": "SpiceJet", "origin": "BOM", "destination": "BLR", "departure": "2025-07-11 09:00", "arrival": "2025-07-11 10:30", "price": 3800, "seats_available": 40},
    {"id": "F004", "airline": "Vistara", "origin": "BLR", "destination": "BOM", "departure": "2025-07-11 11:00", "arrival": "2025-07-11 12:30", "price": 3900, "seats_available": 55},
    {"id": "F005", "airline": "Air India", "origin": "MAA", "destination": "DEL", "departure": "2025-07-12 14:00", "arrival": "2025-07-12 17:00", "price": 4700, "seats_available": 70},
    {"id": "F006", "airline": "IndiGo", "origin": "BOM", "destination": "MAA", "departure": "2025-07-12 16:00", "arrival": "2025-07-12 18:00", "price": 5100, "seats_available": 48},
    {"id": "F007", "airline": "SpiceJet", "origin": "DEL", "destination": "BOM", "departure": "2025-07-13 07:00", "arrival": "2025-07-13 09:00", "price": 4000, "seats_available": 65},
    {"id": "F008", "airline": "Vistara", "origin": "BLR", "destination": "DEL", "departure": "2025-07-13 09:30", "arrival": "2025-07-13 12:00", "price": 4300, "seats_available": 52},
]

hotels = [
    {"id": "H001", "name": "Grand Hyatt", "location": "Chennai", "price_per_night": 7500, "rooms_available": 20},
    {"id": "H002", "name": "Taj Coromandel", "location": "Chennai", "price_per_night": 9000, "rooms_available": 15},
    {"id": "H003", "name": "The Leela Palace", "location": "Bengaluru", "price_per_night": 10000, "rooms_available": 10},
    {"id": "H004", "name": "ITC Gardenia", "location": "Bengaluru", "price_per_night": 8500, "rooms_available": 25},
    {"id": "H005", "name": "The Oberoi", "location": "Mumbai", "price_per_night": 12000, "rooms_available": 8},
    {"id": "H006", "name": "Trident Nariman Point", "location": "Mumbai", "price_per_night": 9500, "rooms_available": 30},
    {"id": "H007", "name": "The Imperial", "location": "Delhi", "price_per_night": 11000, "rooms_available": 12},
    {"id": "H008", "name": "Roseate House", "location": "Delhi", "price_per_night": 7000, "rooms_available": 18},
]

# --- Admin Credentials (Hardcoded as requested) ---
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = bcrypt.generate_password_hash('adminpass').decode('utf-8') # Hashed password for 'adminpass'

# --- Helper functions for user authentication ---
def login_required(f):
    """Decorator to check if a user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_login_required(f):
    """Decorator to check if an admin is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            return redirect(url_for('admin_login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

# Main home page route - now requires login
@app.route('/')
@login_required
def index():
    user_name = session.get('user_name', 'Guest')
    return render_template('index.html', user_name=user_name)

# User Login Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        if conn is None:
            return jsonify({"success": False, "message": "Database connection error."}), 500

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, name, email, password_hash FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and bcrypt.check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name'] # Store user's name in session
                return jsonify({"success": True, "message": "Login successful!"})
            else:
                return jsonify({"success": False, "message": "Invalid email or password."}), 401
        except mysql.connector.Error as err:
            print(f"ERROR: Error during user login: {err}")
            return jsonify({"success": False, "message": f"Error during login: {err}"}), 500
        finally:
            if conn:
                cursor.close()
                conn.close()
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('login_page'))

# User Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        if not name or not email or not phone or not password:
            return jsonify({"success": False, "message": "All fields are required."}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        if conn is None:
            return jsonify({"success": False, "message": "Database connection error."}), 500

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({"success": False, "message": "Email already registered."}), 409

            query = "INSERT INTO users (name, email, phone, password_hash) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, phone, hashed_password))
            conn.commit()
            user_id = cursor.lastrowid
            print(f"New user registered: {name} ({email}) with ID: {user_id}")
            return jsonify({"success": True, "message": "Registration successful!", "id": user_id})
        except mysql.connector.Error as err:
            print(f"ERROR: Error registering user: {err}")
            conn.rollback()
            return jsonify({"success": False, "message": f"Error during registration: {err}"}), 500
        finally:
            if conn:
                cursor.close()
                conn.close()
    return render_template('register.html')

# API endpoint to search flights
@app.route('/api/flights', methods=['GET'])
@login_required
def search_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')

    results = []
    for flight in flights:
        match_origin = not origin or origin.upper() == flight['origin'].upper()
        match_destination = not destination or destination.upper() == flight['destination'].upper()
        
        if match_origin and match_destination:
            results.append(flight)
    
    return jsonify(results)

# API endpoint to search hotels
@app.route('/api/hotels', methods=['GET'])
@login_required
def search_hotels():
    location = request.args.get('location')
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')

    results = []
    for hotel in hotels:
        match_location = not location or location.upper() == hotel['location'].upper()

        if match_location:
            results.append(hotel)
    
    return jsonify(results)

# API endpoint to initiate a booking (before payment)
@app.route('/api/book_initiate', methods=['POST'])
@login_required
def book_initiate():
    data = request.get_json()
    item_id = data.get('id')
    item_type = data.get('type')
    price = data.get('price')

    user_id = session.get('user_id')
    user_name = session.get('user_name') # Get user's name from session
    if not user_id or not user_name: # Ensure user_name is also available
        return jsonify({"success": False, "message": "User not logged in or user name not found in session."}), 401

    conn = get_db_connection()
    if conn is None:
        return jsonify({"success": False, "message": "Database connection error."}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        # Fetch user name and phone from the database using user_id (redundant if user_name is in session, but good for validation)
        cursor.execute("SELECT name, phone FROM users WHERE id = %s", (user_id,))
        user_info = cursor.fetchone()
        if not user_info:
            return jsonify({"success": False, "message": "User not found."}), 404
        
        # Use user_info['name'] for consistency, or user_name from session if preferred
        actual_user_name = user_info['name'] 

        # Simulate booking logic (updates in-memory dummy data)
        booked_item_data = None
        if item_type == 'flight':
            item_list = flights
            item_name_key = 'airline'
        elif item_type == 'hotel':
            item_list = hotels
            item_name_key = 'name'
        else:
            return jsonify({"success": False, "message": "Invalid item type"}), 400

        for item in item_list:
            if item['id'] == item_id:
                if item.get('available_seats', item.get('rooms_available', 0)) > 0:
                    # Do NOT decrement availability here. Decrement AFTER successful payment.
                    booked_item_data = item
                    break
                else:
                    return jsonify({"success": False, "message": f"No availability for {item_type} {item_id}"}), 400

        if booked_item_data:
            # Insert a booking record with 'pending' status, including person_name
            query = """
                INSERT INTO bookings (item_id, item_type, item_name, person_name, user_id, price, status, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            price_for_db = None
            if isinstance(price, str):
                cleaned_price = price.replace('$', '').replace('/night', '').strip()
                try:
                    price_for_db = float(cleaned_price)
                except ValueError:
                    print(f"ERROR: Could not convert price '{price}' to float. Setting to 0.0.")
                    price_for_db = 0.0
            else:
                price_for_db = float(price)
            
            cursor.execute(query, (
                item_id,
                item_type,
                booked_item_data.get(item_name_key, 'Unknown'),
                actual_user_name, # Insert the user's name here
                user_id,
                price_for_db,
                'confirmed', # Set status to 'confirmed' upon initiation
                'pending' # Initial payment status is pending
            ))
            conn.commit()
            booking_id = cursor.lastrowid # Get the ID of the newly inserted booking
            print(f"Booking initiated (status: confirmed, payment_status: pending): {item_type.capitalize()} {booked_item_data.get(item_name_key, 'item')} for user ID: {user_id}, Booking ID: {booking_id}")
            
            # Store booking details in session for the payment page
            session['current_booking'] = {
                'booking_id': booking_id,
                'item_id': item_id,
                'item_type': item_type,
                'item_name': booked_item_data.get(item_name_key, 'Unknown'),
                'price': price_for_db,
                'user_id': user_id
            }
            return jsonify({"success": True, "message": "Booking initiated. Proceed to payment.", "booking_id": booking_id})
        else:
            return jsonify({"success": False, "message": f"{item_type.capitalize()} with ID {item_id} not found."}), 404
    except mysql.connector.Error as err:
        print(f"ERROR: Error initiating booking: {err}")
        conn.rollback()
        return jsonify({"success": False, "message": f"Error during booking initiation: {err}"}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()

# Payment Page Route
@app.route('/payment')
@login_required
def payment_page():
    # Retrieve booking details from session
    current_booking = session.get('current_booking')
    if not current_booking:
        print("DEBUG: No current_booking found in session for payment page. Redirecting to index.")
        return redirect(url_for('index')) # Redirect if no pending booking
    
    print(f"DEBUG: Payment page loaded. Session 'current_booking': {current_booking}")
    return render_template('payment.html', booking=current_booking)

# API endpoint to process simulated payment (UPDATED to always succeed immediately)
@app.route('/api/process_payment', methods=['POST'])
@login_required
def process_payment():
    data = request.get_json()
    booking_id_from_frontend = data.get('booking_id')
    card_number = data.get('cardNumber')

    print(f"DEBUG: Received payment request from frontend. booking_id: {booking_id_from_frontend}, card_number: {card_number}")
    current_booking_from_session = session.get('current_booking')
    print(f"DEBUG: Session 'current_booking': {current_booking_from_session}")

    if not current_booking_from_session:
        print(f"ERROR: 'current_booking' is None in session. Cannot proceed with payment.")
        return jsonify({"success": False, "message": "Invalid or expired booking session. (No session data)"}), 400
    
    # --- CRITICAL FIX: Convert frontend booking_id to integer for comparison ---
    try:
        booking_id_from_frontend_int = int(booking_id_from_frontend)
    except ValueError:
        print(f"ERROR: Frontend booking_id '{booking_id_from_frontend}' cannot be converted to integer.")
        return jsonify({"success": False, "message": "Invalid booking ID format from frontend."}), 400

    session_booking_id = current_booking_from_session.get('booking_id')
    
    print(f"DEBUG: Comparing IDs. Session ID: {session_booking_id} (Type: {type(session_booking_id)}), Frontend ID (converted): {booking_id_from_frontend_int} (Type: {type(booking_id_from_frontend_int)})")

    if session_booking_id != booking_id_from_frontend_int: # Comparison with converted type
        print(f"ERROR: Session ID mismatch. Session booking_id: {session_booking_id}, Frontend booking_id (converted): {booking_id_from_frontend_int}")
        return jsonify({"success": False, "message": "Invalid or expired booking session. (ID mismatch)"}), 400

    conn = get_db_connection()
    if conn is None:
        print("ERROR: Database connection failed in process_payment.")
        return jsonify({"success": False, "message": "Database connection error after payment simulation."}), 500

    try:
        cursor = conn.cursor()
        # Update both status and payment_status to 'confirmed' and 'completed'
        update_query = "UPDATE bookings SET status = 'confirmed', payment_status = 'completed' WHERE id = %s"
        print(f"DEBUG: Attempting to update booking ID {booking_id_from_frontend_int} status to 'confirmed' and payment_status to 'completed'.")
        cursor.execute(update_query, (booking_id_from_frontend_int,))
        
        # Check if any rows were affected by the update
        if cursor.rowcount == 0:
            print(f"WARNING: No rows updated for booking ID {booking_id_from_frontend_int}. Booking might not exist or already completed. This could be a logic error or race condition.")
            # Depending on desired behavior, might return success or a specific message here
            # For now, we'll proceed as if it was a success if no error was raised.
        
        conn.commit() # Explicitly commit the transaction
        print(f"DEBUG: Database commit successful for booking ID {booking_id_from_frontend_int}. Rows affected: {cursor.rowcount}")

        # Decrement availability in dummy data (now that payment is confirmed)
        if current_booking_from_session['item_type'] == 'flight':
            for flight in flights:
                if flight['id'] == current_booking_from_session['item_id']:
                    if 'available_seats' in flight:
                        flight['available_seats'] -= 1
                        print(f"DEBUG: Decremented available_seats for flight {flight['id']}. New count: {flight['available_seats']}")
                    elif 'seats_available' in flight:
                        flight['seats_available'] -= 1
                        print(f"DEBUG: Decremented seats_available for flight {flight['id']}. New count: {flight['seats_available']}")
                    break
        elif current_booking_from_session['item_type'] == 'hotel':
            for hotel in hotels:
                if hotel['id'] == current_booking_from_session['item_id']:
                    hotel['rooms_available'] -= 1
                    print(f"DEBUG: Decremented rooms_available for hotel {hotel['id']}. New count: {hotel['rooms_available']}")
                    break
        print(f"Booking {booking_id_from_frontend_int} confirmed and availability updated in dummy data.")
        session.pop('current_booking', None) # Clear pending booking from session
        return jsonify({"success": True, "message": "Payment processed successfully on backend."})
    except mysql.connector.Error as err:
        print(f"ERROR: MySQL error during payment processing for booking {booking_id_from_frontend_int}: {err}")
        conn.rollback() # Rollback in case of error
        return jsonify({"success": False, "message": f"Error updating booking status on backend: {err}"}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
            print(f"DEBUG: Database connection closed for process_payment.")


# Admin Login Page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username == ADMIN_USERNAME and bcrypt.check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            return jsonify({"success": True, "message": "Admin login successful!"})
        else:
            return jsonify({"success": False, "message": "Invalid admin credentials."}), 401
    return render_template('admin_login.html')

# Admin Logout
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login_page'))

# Admin Dashboard Page
@app.route('/admin_dashboard')
@admin_login_required
def admin_dashboard_page():
    return render_template('admin_dashboard.html')

# API endpoint to get all registered users (for Admin)
@app.route('/api/get_registered_users', methods=['GET'])
@admin_login_required
def get_registered_users():
    conn = get_db_connection()
    if conn is None:
        print("ERROR: Database connection failed in get_registered_users.")
        return jsonify({"success": False, "message": "Database connection error."}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, phone, registered_at FROM users ORDER BY registered_at DESC")
        users = cursor.fetchall()
        for user in users:
            if isinstance(user.get('registered_at'), datetime.datetime):
                user['registered_at'] = user['registered_at'].isoformat()
        return jsonify(users)
    except mysql.connector.Error as err:
        print(f"ERROR: Error fetching registered users from MySQL: {err}")
        return jsonify({"success": False, "message": f"Error fetching registered users: {err}"}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
            print(f"DEBUG: Database connection closed for get_registered_users.")

# API endpoint to get all bookings (for Admin)
@app.route('/api/get_all_bookings', methods=['GET'])
@admin_login_required
def get_all_bookings():
    conn = get_db_connection()
    if conn is None:
        print("ERROR: Database connection failed in get_all_bookings.")
        return jsonify({"success": False, "message": "Database connection error."}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        # Include person_name in the query
        query = """
            SELECT b.id, b.item_id, b.item_type, b.item_name, b.person_name, u.name AS user_name, u.phone AS user_phone, b.price, b.booking_time, b.status, b.payment_status
            FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            ORDER BY b.booking_time DESC
        """
        print("DEBUG: Fetching all bookings from database.")
        cursor.execute(query)
        bookings_data = cursor.fetchall()
        for booking in bookings_data:
            if isinstance(booking.get('booking_time'), datetime.datetime):
                booking['booking_time'] = booking['booking_time'].isoformat()
        print(f"DEBUG: Fetched {len(bookings_data)} bookings.")
        return jsonify(bookings_data)
    except mysql.connector.Error as err:
        print(f"ERROR: Error fetching bookings from MySQL: {err}")
        return jsonify({"success": False, "message": f"Error fetching bookings: {err}"}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()
            print(f"DEBUG: Database connection closed for get_all_bookings.")

if __name__ == '__main__':
    app.run(debug=True)
