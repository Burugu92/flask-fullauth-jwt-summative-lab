# 💰 Flask JWT Expense Tracker API

## 📌 Project Overview

This project is a **secure Flask REST API backend** for a productivity application that allows users to track personal expenses.

It implements:

* **JWT-based authentication**
* **User-specific data ownership**
* **Full CRUD operations**
* **Pagination for resource listing**
* **Secure access control**

Each user can create, view, update, and delete **only their own expenses**, ensuring full data privacy.

---

## 🚀 Features

### 🔐 Authentication

* User registration (`/signup`)
* User login with JWT token (`/login`)
* Retrieve current user (`/me`)
* Passwords securely hashed using **Flask-Bcrypt**

### 💰 Expense Management

* Create expenses
* View expenses (paginated)
* Update expenses
* Delete expenses

### 🔒 Security

* JWT required for all protected routes
* Users can only access their own data
* Unauthorized requests return proper HTTP status codes

### 📊 Pagination

* Implemented on expense listing endpoint
* Supports query parameters:

  * `page`
  * `per_page`

---

## 🛠️ Tech Stack

* Python 3.8+
* Flask 2.2.2
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Bcrypt
* Flask-JWT-Extended
* Marshmallow (optional serialization)
* Faker (database seeding)
* Pytest (testing)

---

## 📁 Project Structure


```
project-root/
│
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── seed.py
│
├── resources/
│   ├── __init__.py
│   ├── auth.py
│   ├── expenses.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_expenses.py
│
├── migrations/
├── Pipfile
└── README.md
```


## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone <your-repo-url>
cd <your-repo-name>
```

---

### 2. Install dependencies

```
pipenv install
pipenv shell
```

---

### 3. Set up the database

```
flask db init
flask db migrate
flask db upgrade
```

---

### 4. Seed the database

```
python server/seed.py
```

This will:

* Create a test user
* Generate sample expenses using Faker

---

### 5. Run the server

```
flask --app server.app run
```

Server will start at:

```
http://127.0.0.1:5000
```

---

## 🔐 Authentication Flow

1. Register a user → `/signup`
2. Login → `/login`
3. Receive JWT token
4. Include token in headers:

```
Authorization: Bearer <your_token>
```

---

## 📡 API Endpoints

### 🔐 Auth Routes

#### POST `/signup`

Create a new user

Request:

```
{
  "username": "user1",
  "password": "password123"
}
```

Response:

* 201 Created
* 400/409 if user exists

---

#### POST `/login`

Authenticate user and return JWT

Response:

```
{
  "access_token": "..."
}
```

---

#### GET `/me`

Get current logged-in user

Headers:

```
Authorization: Bearer <token>
```

---

## 💰 Expense Routes (Protected)

### GET `/expenses`

Retrieve paginated expenses

Query Params:

```
?page=1&per_page=5
```

Response:

```
{
  "expenses": [...],
  "page": 1,
  "pages": 2,
  "total": 10
}
```

---

### POST `/expenses`

Create a new expense

Request:

```
{
  "title": "Lunch",
  "amount": 20,
  "category": "Food",
  "description": "Burger",
  "date": "2026-04-21"
}
```

---

### PATCH `/expenses/<id>`

Update an expense (owner only)

---

### DELETE `/expenses/<id>`

Delete an expense (owner only)

---

## 🔒 Access Control Rules

* All expense routes require JWT authentication
* Users can only:

  * View their own expenses
  * Update their own expenses
  * Delete their own expenses
* Unauthorized access returns:

  * `401 Unauthorized` (no/invalid token)
  * `403 Forbidden` (accessing another user’s data)

---

## 🌱 Database Seeding

Run:

```
python server/seed.py
```

Creates:

* Sample user(s)
* Multiple expenses linked to users

---

## 🧪 Testing

This project includes a comprehensive **pytest test suite**.

### Run tests:

```
pytest -v
```

### Test Coverage:

* Authentication (signup, login, /me)
* JWT protection
* Expense CRUD operations
* Pagination
* Ownership enforcement
* Edge cases (invalid input, unauthorized access)

---

## ✅ Status Codes Used

* `200 OK`
* `201 Created`
* `400 Bad Request`
* `401 Unauthorized`
* `403 Forbidden`
* `404 Not Found`
* `422 Unprocessable Entity`

---

## 🎯 Key Learning Outcomes

* Building secure REST APIs with Flask
* Implementing JWT authentication
* Enforcing user-based data ownership
* Designing scalable API structures
* Writing comprehensive automated tests

---

## 👤 Author

Developed as part of a **Flask Backend Summative Lab**.
