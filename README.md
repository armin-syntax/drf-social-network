# Social Network API

A RESTful backend API for a social network built with **Django**, **Django REST Framework**, and **JWT Authentication**.

## Features

- JWT Authentication
- User Registration & Profiles
- Avatar Upload
- Posts (Image / Video)
- Comments
- Follow / Unfollow Users
- Search Users & Posts

---

## 📦 Installation

Run the following commands:

```bash
pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser   # Optional

python manage.py runserver
```

---

## Authentication

All protected endpoints require a JWT access token.

Example:

Authorization: Bearer <access_token>

---

## API Endpoints

### Authentication

| Endpoint | Method | Authentication | Required Fields |
|----------|--------|----------------|-----------------|
| `/api/token/` | POST | No | username, password |
| `/api/token/refresh/` | POST | No | refresh |

---

### Accounts

| Endpoint | Method | Authentication | Required Fields |
|----------|--------|----------------|-----------------|
| `/api/accounts/` | GET | Yes | None |
| `/api/accounts/` | POST | No | username, email, full_name, password, confirm_password |
| `/api/accounts/<username>/` | GET | Yes | None |
| `/api/accounts/<username>/` | PUT / PATCH | Yes | Any profile field (username, email, full_name, bio, avatar) |
| `/api/accounts/<username>/` | DELETE | Yes | None |
| `/api/accounts/<username>/follow/` | POST | Yes | None |
| `/api/accounts/<username>/unfollow/` | DELETE | Yes | None |
| `/api/accounts/<username>/followers/` | GET | Yes | None |
| `/api/accounts/<username>/following/` | GET | Yes | None |
| `/api/accounts/<username>/posts/` | GET | Yes | None |

---

### Posts

| Endpoint | Method | Authentication | Required Fields |
|----------|--------|----------------|-----------------|
| `/api/posts/` | GET | Yes | None |
| `/api/posts/` | POST | Yes | media, description |
| `/api/posts/<post_id>/` | GET | Yes | None |
| `/api/posts/<post_id>/` | PUT / PATCH | Yes | Any post field (media, description) |
| `/api/posts/<post_id>/` | DELETE | Yes | None |
| `/api/posts/<post_id>/comments/` | GET | Yes | None |
| `/api/posts/<post_id>/comments/` | POST | Yes | body |

---

## Response Format

Successful requests return JSON responses.

Validation errors are returned in the following format:

```json
{
    "username": [
        "This username already exists."
    ],
    "email": [
        "This email address already exists."
    ]
}
```

---
