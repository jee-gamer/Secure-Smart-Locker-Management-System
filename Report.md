# Smart/Secure Locker Management System (SSLMS) - Project Report

## 1. Project Overview
The Smart/Secure Locker Management System (SSLMS) is a web-based application designed to facilitate the secure sharing or transferring of physical items between users via managed lockers. Users can book a locker, deposit an item (optionally taking a picture of the item), and assign a receiver. The receiver can then view the locker status and retrieve the item, which completes the transaction and frees the locker for future use.

## 2. System Requirements
- **Functional Requirements:**
  - **User Authentication:** Users can register, log in, and maintain sessions securely.
  - **Locker Management:** View a grid of lockers with real-time status (available or occupied).
  - **Booking System:** Users can book a locker and assign a receiver from a searchable user list.
  - **Item Image Attachments:** Senders can upload an image of the item being placed in the locker.
  - **Unbooking System:** Receivers (or senders) can unbook/cancel a booking, freeing up the locker.
- **Non-Functional Requirements:**
  - **Usability:** A responsive and intuitive user interface using Tailwind CSS and Vue.js.
  - **Security:** Secure password hashing (Werkzeug) and managed file uploads.
  - **Performance:** Lightweight API requests with fast resolution via SQLite and Flask.

## 3. Architecture Characteristics
- **Client-Server Architecture:** Decoupling of the frontend (Vue.js) and backend (Flask) allows independent deployments and scaling.
- **RESTful API:** Communication between the client and server is handled via REST endpoints using JSON and Multipart form-data (for file uploads).
- **Modularity:** The backend is organized using the MVC software design pattern, featuring clear separation between Routes, Controllers (business logic), and Models (database access).
- **Statelessness (Backend):** Each API request provides the necessary context (e.g., user IDs) for processing.

## 4. Architecture Design
- **Frontend Layer:** Built with Vue 3 (Composition API) and Vite. Manages global state using Pinia-like structures (or simple reactive auth stores), handles routing (Vue Router), and communicates with the backend via Axios.
- **Backend Layer:** Built with Python and Flask. Uses Blueprints for modular routing (`booking_routes`, `user_routes`, `locker_routes`). 
- **Controller Layer:** Contains business logic (e.g., verifying locker availability, validating file extensions, managing filesystem operations for uploaded images).
- **Data Access Layer (Model):** Contains pure SQLite queries mapping directly to Python dictionaries.
- **Database Layer:** A local SQLite database (`locker.db`) storing structured data, coupled with a filesystem `/uploads` directory handling physical item images.

## 5. Database Design
The system uses SQLite with three core tables:
- **`users`**:
  - `id` (INTEGER PRIMARY KEY)
  - `username` (TEXT, UNIQUE, NOT NULL)
  - `password` (TEXT, NOT NULL)
  - `role` (TEXT, NOT NULL)
  - `created_at` (TIMESTAMP)
- **`lockers`**:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `status` (TEXT, CHECK: 'available' or 'occupied')
  - `item_image_path` (TEXT - File path to the uploaded image)
- **`bookings`**:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `user_id` (INTEGER, FOREIGN KEY to users)
  - `receiver_id` (INTEGER, FOREIGN KEY to users)
  - `locker_id` (INTEGER, FOREIGN KEY to lockers)
  - `start_time` (TIMESTAMP)
  - `end_time` (TIMESTAMP - represents checkout when not NULL)

## 6. Role & Permission Structure
- **User Role (`user`):** Standard users can view lockers, book an available locker for a specific receiver, upload an image of the item, and retrieve (unbook) items from lockers sent to them.
- **Admin Role (`admin`):** Reserved for administrative privileges (e.g., system management, potential overrides). Currently embedded in the schema but standard interactions map to user-level permissions.
- **Booking-Level Permissions:** Users can only open or view sensitive image details of lockers where they are either the explicit `sender_id` (`user_id`) or `receiver_id`.

## 7. Implementation Details
- **Frontend Framework:** Vue 3 + TailwindCSS.
- **Backend Framework:** Flask + Flask-CORS. 
- **Database:** SQLite3 managed via custom Python module mappings instead of an ORM (like SQLAlchemy) for absolute query control.
- **Upload Management:** Senders upload item photos using `multipart/form-data`. The Flask backend uses Python's `uuid.uuid4()` to generate collision-free filenames and saves the resources locally to an `uploads` folder outside the backend root, maintaining security.
- **File Deletion:** When a locker is unbooked/emptied, the application securely unlinks (deletes) the corresponding image from the local filesystem to save space and maintain privacy.
- **Database Migrations & Seeding:** Handled explicitly on application startup (`migrate.py`), ensuring 25 lockers and initial dummy users (`man`, `user1`, `user2`, `stupid`) are always seeded for ease of testing.
