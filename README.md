# ✈️ Travel Booker Application

A comprehensive full-stack web application designed to streamline **Flight** and **Hotel** bookings. This project features a secure user authentication system, a dynamic booking interface, and a dedicated Administrative Dashboard to manage user data.

---

## 🚀 Features

* **User Authentication:** Secure Registration and Login system for travelers.
* **Flight & Hotel Search:** Intuitive interface to browse travel options.
* **Admin Panel:** A restricted area for administrators to monitor and track all registered users.
* **Responsive Design:** Clean UI built with HTML5 and CSS3, enhanced with travel-themed icons.
* **Database Integration:** Powered by SQLite for reliable data storage and retrieval.
* **Payment Simulation:** Includes a dedicated payment processing page for a complete user flow.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (enhanced with Font Awesome icons)
* **Backend:** Python (Flask Framework)
* **Database:** SQLite
* **Documentation:** Project Report included (.docx)

---

## 📁 Project Structure

```text
travel_app/
├── app.py                  # Main Flask application logic
├── database.db             # SQLite database file
├── static/                 # CSS, Images, and JS files
└── templates/              # HTML files
    ├── index.html          # Homepage
    ├── login.html          # User Login
    ├── register.html       # User Registration
    ├── admin_login.html    # Admin Access
    ├── admin_dashboard.html# Admin User Management
    └── payment.html        # Booking Payment Page
