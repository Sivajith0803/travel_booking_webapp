// DEBUG: Confirm if script.js is loading and executing
console.log("script.js loaded and executing.");

// --- DOM Elements ---
// Global elements (modal)
const bookingModal = document.getElementById('booking-modal');
const modalMessage = document.getElementById('modal-message');
const closeButton = document.querySelector('.close-button');
const modalOkButton = document.getElementById('modal-ok-button'); // Ensure this ID is correct in HTML

// Registration Page Elements
const registrationForm = document.getElementById('registration-form');
const regNameInput = document.getElementById('reg-name');
const regEmailInput = document.getElementById('reg-email');
const regPhoneInput = document = document.getElementById('reg-phone'); // Corrected typo
const regPasswordInput = document.getElementById('reg-password');

// Login Page Elements
const loginForm = document.getElementById('login-form');
const loginEmailInput = document.getElementById('login-email');
const loginPasswordInput = document.getElementById('login-password');

// Admin Login Page Elements
const adminLoginForm = document.getElementById('admin-login-form');
const adminUsernameInput = document.getElementById('admin-username');
const adminPasswordInput = document.getElementById('admin-password');

// Admin Dashboard Page Elements
const viewRegistrationsBtn = document.getElementById('view-registrations-btn');
const viewBookingsBtn = document.getElementById('view-bookings-btn');
const dashboardResultsDiv = document.getElementById('dashboard-results');

// Main Page Search Elements
const flightSearchForm = document.getElementById('flight-search-form');
const flightOriginInput = document.getElementById('flight-origin');
const flightDestinationInput = document.getElementById('flight-destination');
const flightDateInput = document.getElementById('flight-date');
const flightResultsDiv = document.getElementById('flight-results');

const hotelSearchForm = document.getElementById('hotel-search-form');
const hotelLocationInput = document.getElementById('hotel-location');
const hotelCheckInInput = document.getElementById('hotel-check-in');
const hotelCheckOutInput = document.getElementById('hotel-check-out');
const hotelResultsDiv = document.getElementById('hotel-results');

// Payment Page Elements
const paymentForm = document.getElementById('payment-form');
const cardNumberInput = document.getElementById('card-number');
const bookingIdHiddenInput = document.getElementById('booking-id');


// --- Modal Functions ---
function showBookingModal(message) {
    if (modalMessage && bookingModal) {
        modalMessage.innerHTML = message;
        bookingModal.classList.add('active');
        document.body.classList.add('modal-open'); // Prevent scrolling
    }
}

function hideBookingModal() {
    if (bookingModal) {
        bookingModal.classList.remove('active');
        document.body.classList.remove('modal-open'); // Re-enable scrolling
    }
}

// Event Listeners for Modal
if (closeButton) {
    closeButton.addEventListener('click', hideBookingModal);
}
if (modalOkButton) {
    modalOkButton.addEventListener('click', hideBookingModal);
}
if (bookingModal) {
    bookingModal.addEventListener('click', (event) => {
        if (event.target === bookingModal) {
            hideBookingModal();
        }
    });
}


// --- Registration Form Submission Logic ---
if (registrationForm) {
    console.log("DEBUG: Registration form element found. Adding event listener.");
    registrationForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log("DEBUG: Registration form submitted.");

        const name = regNameInput.value;
        const email = regEmailInput.value;
        const phone = regPhoneInput.value;
        const password = regPasswordInput.value;

        if (!name || !email || !phone || !password) {
            showBookingModal('Please fill in all registration fields.');
            console.log("DEBUG: Missing registration fields.");
            return;
        }

        try {
            console.log(`DEBUG: Sending registration request for Name: ${name}, Email: ${email}, Phone: ${phone}`);
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, phone, password }),
            });

            console.log("DEBUG: Received response from /register.");
            const result = await response.json();
            console.log("DEBUG: Response JSON:", result);

            if (response.ok && result.success) {
                showBookingModal('Registration successful! Please log in.');
                console.log("DEBUG: Registration successful, redirecting to login.");
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                showBookingModal(`Registration failed: ${result.message || 'Unknown error'}`);
                console.error("ERROR: Registration failed:", result);
            }
        } catch (error) {
            console.error('ERROR: Network or API call error during registration:', error);
            showBookingModal('An error occurred during registration. Please try again.');
        }
    });
} else {
    console.warn("WARNING: Registration form element (ID 'registration-form') not found.");
}


// --- User Login Form Submission Logic ---
if (loginForm) {
    console.log("DEBUG: Login form element found. Adding event listener.");
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log("DEBUG: Login form submitted.");

        const email = loginEmailInput.value;
        const password = loginPasswordInput.value;

        if (!email || !password) {
            showBookingModal('Please enter your email and password.');
            console.log("DEBUG: Login: Email or password missing.");
            return;
        }

        try {
            console.log(`DEBUG: Sending login request for Email: ${email}`);
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            console.log("DEBUG: Received response from /login.");
            const result = await response.json();
            console.log("DEBUG: Response JSON:", result);

            if (response.ok && result.success) {
                showBookingModal('Login successful! Redirecting to main page.');
                console.log("DEBUG: Login successful, redirecting to home.");
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            } else {
                showBookingModal(`Login failed: ${result.message || 'Invalid credentials.'}`);
                console.error("ERROR: Login failed:", result);
            }
        } catch (error) {
            console.error('ERROR: Network or API call error during login:', error);
            showBookingModal('An error occurred during login. Please try again.');
        }
    });
} else {
    console.warn("WARNING: Login form element (ID 'login-form') not found.");
}


// --- Admin Login Form Submission Logic ---
if (adminLoginForm) {
    console.log("DEBUG: Admin Login form element found. Adding event listener.");
    adminLoginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log("DEBUG: Admin login form submitted.");

        const username = adminUsernameInput.value;
        const password = adminPasswordInput.value;

        if (!username || !password) {
            showBookingModal('Please enter admin username and password.');
            console.log("DEBUG: Admin login: Username or password missing.");
            return;
        }

        try {
            console.log(`DEBUG: Sending admin login request for Username: ${username}`);
            const response = await fetch('/admin_login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            console.log("DEBUG: Received response from /admin_login.");
            const result = await response.json();
            console.log("DEBUG: Response JSON:", result);

            if (response.ok && result.success) {
                showBookingModal('Admin login successful! Redirecting to dashboard.');
                console.log("DEBUG: Admin login successful, redirecting to dashboard.");
                setTimeout(() => {
                    window.location.href = '/admin_dashboard';
                }, 1500);
            } else {
                showBookingModal(`Admin login failed: ${result.message || 'Invalid credentials.'}`);
                console.error("ERROR: Admin login failed:", result);
            }
        } catch (error) {
            console.error('ERROR: Network or API call error during admin login:', error);
            showBookingModal('An error occurred during admin login. Please try again.');
        }
    });
} else {
    console.warn("WARNING: Admin login form element (ID 'admin-login-form') not found.");
}


// --- Admin Dashboard Functionality ---
if (viewRegistrationsBtn) {
    viewRegistrationsBtn.addEventListener('click', async () => {
        dashboardResultsDiv.innerHTML = '<p class="info-message">Fetching registered users...</p>';
        try {
            const response = await fetch('/api/get_registered_users');
            const users = await response.json();
            if (response.ok && Array.isArray(users)) {
                displayDashboardData(users, 'registrations');
            } else {
                dashboardResultsDiv.innerHTML = `<p class="error-message">Error: ${users.message || 'Failed to fetch users.'}</p>`;
                console.error("ERROR: Failed to fetch registered users:", users);
            }
        } catch (error) {
            console.error('ERROR: Network error fetching registered users:', error);
            dashboardResultsDiv.innerHTML = '<p class="error-message">Network error fetching registered users. Check console.</p>';
        }
    });
}

if (viewBookingsBtn) {
    viewBookingsBtn.addEventListener('click', async () => {
        dashboardResultsDiv.innerHTML = '<p class="info-message">Fetching all bookings...</p>';
        try {
            const response = await fetch('/api/get_all_bookings');
            const bookings = await response.json();
            if (response.ok && Array.isArray(bookings)) {
                displayDashboardData(bookings, 'bookings');
            } else {
                dashboardResultsDiv.innerHTML = `<p class="error-message">Error: ${bookings.message || 'Failed to fetch bookings.'}</p>`;
                console.error("ERROR: Failed to fetch all bookings:", bookings);
            }
        } catch (error) {
            console.error('ERROR: Network error fetching bookings:', error);
            dashboardResultsDiv.innerHTML = '<p class="error-message">Network error fetching bookings. Check console.</p>';
        }
    });
}

function displayDashboardData(data, type) {
    if (!dashboardResultsDiv) return;

    if (data.length === 0) {
        dashboardResultsDiv.innerHTML = `<p class="info-message">No ${type} found.</p>`;
        return;
    }

    let tableHtml = '<table><thead><tr>';
    let headers = [];

    if (type === 'registrations') {
        headers = ['ID', 'Name', 'Email', 'Phone', 'Registered At'];
    } else if (type === 'bookings') {
        // Updated headers to include "Booked By"
        headers = ['ID', 'Item Type', 'Item Name', 'Booked By', 'User Name (FK)', 'User Phone (FK)', 'Price', 'Booking Time', 'Status', 'Payment Status'];
    }
    
    headers.forEach(header => {
        tableHtml += `<th>${header}</th>`;
    });
    tableHtml += '</tr></thead><tbody>';

    data.forEach(item => {
        tableHtml += '<tr>';
        if (type === 'registrations') {
            tableHtml += `<td>${item.id || 'N/A'}</td>`;
            tableHtml += `<td>${item.name || 'N/A'}</td>`;
            tableHtml += `<td>${item.email || 'N/A'}</td>`;
            tableHtml += `<td>${item.phone || 'N/A'}</td>`;
            tableHtml += `<td>${new Date(item.registered_at).toLocaleString() || 'N/A'}</td>`;
        } else if (type === 'bookings') {
            tableHtml += `<td>${item.id || 'N/A'}</td>`;
            tableHtml += `<td>${item.item_type || 'N/A'}</td>`;
            tableHtml += `<td>${item.item_name || 'N/A'}</td>`;
            tableHtml += `<td>${item.person_name || 'N/A'}</td>`; // Display the new person_name
            tableHtml += `<td>${item.user_name || 'N/A'}</td>`; // User name from JOIN
            tableHtml += `<td>${item.user_phone || 'N/A'}</td>`; // User phone from JOIN
            tableHtml += `<td>$${item.price || 'N/A'}</td>`;
            tableHtml += `<td>${new Date(item.booking_time).toLocaleString() || 'N/A'}</td>`;
            tableHtml += `<td>${item.status || 'N/A'}</td>`;
            tableHtml += `<td>${item.payment_status || 'N/A'}</td>`;
        }
        tableHtml += '</tr>';
    });
    tableHtml += '</tbody></table>';
    dashboardResultsDiv.innerHTML = tableHtml;
}


// --- Flight Search Display and Booking Logic ---
function addBookNowListeners() {
    document.querySelectorAll('.book-now-button').forEach(button => {
        button.addEventListener('click', async () => {
            const type = button.dataset.type;
            const id = button.dataset.id;
            const itemDisplayName = button.dataset.airline || button.dataset.name;
            const price = button.dataset.price;

            // Initiate booking (this creates a pending booking in DB and stores in session)
            try {
                const response = await fetch('/api/book_initiate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: id, type: type, price: price }),
                });
                const result = await response.json();

                if (response.ok && result.success) {
                    showBookingModal(`Booking initiated for ${itemDisplayName}. Redirecting to payment...`);
                    setTimeout(() => {
                        window.location.href = '/payment';
                    }, 1500);
                } else {
                    showBookingModal(`Booking initiation failed: ${result.message || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Error during booking initiation API call:', error);
                showBookingModal('An error occurred during booking initiation. Please try again.');
            }
        });
    });
}

// Initial attachment of event listeners for search forms (main page)
if (flightSearchForm) {
    flightSearchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const origin = flightOriginInput.value;
        const destination = flightDestinationInput.value;
        const date = flightDateInput.value;
        if (!origin || !destination) {
            showBookingModal('Please enter both origin and destination for flight search.');
            return;
        }
        flightResultsDiv.innerHTML = '<p class="info-message">Searching for flights...</p>';
        try {
            const response = await fetch(`/api/flights?origin=${origin}&destination=${destination}&date=${date}`);
            const flights = await response.json();
            displayFlights(flights);
        } catch (error) {
            console.error('Error fetching flights:', error);
            flightResultsDiv.innerHTML = '<p class="error-message">Failed to load flights. Please try again.</p>';
        }
    });
}

if (hotelSearchForm) {
    hotelSearchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const location = hotelLocationInput.value;
        const checkIn = hotelCheckInInput.value;
        const checkOut = hotelCheckOutInput.value;
        if (!location) {
            showBookingModal('Please enter a location for hotel search.');
            return;
        }
        hotelResultsDiv.innerHTML = '<p class="info-message">Searching for hotels...</p>';
        try {
            const response = await fetch(`/api/hotels?location=${location}&check_in=${checkIn}&check_out=${checkOut}`);
            const hotels = await response.json();
            displayHotels(hotels);
        } catch (error) {
            console.error('Error fetching hotels:', error);
            hotelResultsDiv.innerHTML = '<p class="error-message">Failed to load hotels. Please try again.</p>';
        }
    });
}

function displayFlights(flights) {
    if (!flightResultsDiv) return;
    if (flights.length === 0) {
        flightResultsDiv.innerHTML = '<p class="info-message">No flights found for your criteria.</p>';
        return;
    }
    let flightsHtml = '<h3>Available Flights:</h3><ul class="results-list">';
    flights.forEach(flight => {
        const priceDisplay = flight.price ? `$${flight.price}` : 'N/A';
        flightsHtml += `
            <li>
                <div class="results-list-content">
                    <strong>${flight.airline}</strong><br>
                    ${flight.origin} to ${flight.destination}<br>
                    Departure: ${flight.departure}<br>
                    Arrival: ${flight.arrival}<br>
                    Price: <span class="price-display">${priceDisplay}</span><br>
                    Seats Available: ${flight.available_seats || 'N/A'}
                </div>
                <button class="book-now-button" data-type="flight" data-id="${flight.id}" data-airline="${flight.airline}" data-price="${priceDisplay}">Book Now</button>
            </li>
        `;
    });
    flightResultsDiv.innerHTML = flightsHtml + '</ul>';
    addBookNowListeners();
}

function displayHotels(hotels) {
    if (!hotelResultsDiv) return;
    if (hotels.length === 0) {
        hotelResultsDiv.innerHTML = '<p class="info-message">No hotels found for your criteria.</p>';
        return;
    }
    let hotelsHtml = '<h3>Available Hotels:</h3><ul class="results-list">';
    hotels.forEach(hotel => {
        const priceDisplay = hotel.price_per_night ? `$${hotel.price_per_night}/night` : 'N/A';
        hotelsHtml += `
            <li>
                <div class="results-list-content">
                    <strong>${hotel.name}</strong><br>
                    Location: ${hotel.location}<br>
                    Price: <span class="price-display">${priceDisplay}</span><br>
                    Rooms Available: ${hotel.rooms_available || 'N/A'}
                </div>
                <button class="book-now-button" data-type="hotel" data-id="${hotel.id}" data-name="${hotel.name}" data-price="${priceDisplay}">Book Now</button>
            </li>
        `;
    });
    hotelResultsDiv.innerHTML = hotelsHtml + '</ul>';
    addBookNowListeners();
}

// --- Payment Form Submission Logic (Sequential Success with Emojis) ---
if (paymentForm) {
    console.log("DEBUG: Payment form element found. Adding event listener.");
    paymentForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log("DEBUG: Payment form submitted.");

        const bookingId = bookingIdHiddenInput.value;
        const cardNumber = cardNumberInput.value;

        // --- NEW DEBUGGING LINE FOR FRONTEND ---
        console.log(`DEBUG (Frontend): Sending payment request. Booking ID from hidden input: ${bookingId}. Card Number: ${cardNumber}`);


        if (!cardNumber) {
            showBookingModal('Please fill in the card number.');
            console.log("DEBUG: Payment: Card number missing.");
            return;
        }

        // Disable button and show loading indicator
        const payButton = paymentForm.querySelector('.payment-button');
        payButton.disabled = true;
        payButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

        try {
            console.log(`DEBUG: Sending payment confirmation to backend for Booking ID: ${bookingId}`);
            const response = await fetch('/api/process_payment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ booking_id: bookingId, cardNumber }),
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // --- SHOW SUCCESS MODAL ONLY AFTER BACKEND CONFIRMATION ---
                showBookingModal('🎉 Thank you for choosing Smart Trip! Your payment is successful. ✈️ Have a happy journey! 🏨');
                console.log("DEBUG: Backend payment update successful, showing success modal.");
                
                // Redirect after a short delay for user to read message
                setTimeout(() => {
                    window.location.href = '/';
                }, 2500);

            } else {
                // --- SHOW FAILURE MODAL IF BACKEND REPORTS FAILURE ---
                showBookingModal(`Payment failed: ${result.message || 'Unknown payment error'}`);
                console.error("ERROR: Backend payment update failed:", result.message);
                payButton.disabled = false;
                payButton.innerHTML = 'Pay Now';
            }
        } catch (error) {
            console.error('ERROR: Network or API call error during payment confirmation:', error);
            showBookingModal('An error occurred during payment processing. Please try again.');
            payButton.disabled = false;
            payButton.innerHTML = 'Pay Now';
        }
    });
} else {
    console.warn("WARNING: Payment form element (ID 'payment-form') not found.");
}


// --- Initial Page Load Logic (Access Control and Animations) ---
document.addEventListener('DOMContentLoaded', () => {
    console.log("DEBUG: DOMContentLoaded event fired.");

    // Apply animations after content is loaded
    document.querySelectorAll('.animate-on-load').forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
        element.classList.add('animated-visible');
    });

    // Initial attachment of event listeners for search forms (main page)
    addBookNowListeners();
});
