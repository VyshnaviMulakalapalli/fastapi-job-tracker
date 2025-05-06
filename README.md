# FastAPI Job Application Tracker
A modern, full-featured web API for tracking job applications, built with FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, and Celery for asynchronous email verification.

## Features
- User Registration & Login with JWT-based authentication

- Email Verification via Celery background tasks

- CRUD Operations for job applications (create, read, update, delete)

- Secure Password Hashing with Passlib

- Database Migrations with Alembic

- PostgreSQL as the backend database

- Environment-based Configuration via .env files

## Tech Stack
- FastAPI

- SQLAlchemy

- PostgreSQL

- Alembic

- Celery

- Redis (Celery broker)

- Passlib (password hashing)

- python-dotenv (environment variables)

- PyJWT via python-jose

## Getting Started
1. Clone the Repository

```bash
git clone https://github.com/yourusername/job-application-tracker.git
cd job-application-tracker
```

2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure Environment Variables
Create a .env file in the root directory:

```bash
EMAIL_USER=YOUR_EMAIL
EMAIL_PASSWORD=YOUR_PASSWORD
SECRET_KEY = YOUR_SECRET_KEY
ALGORITHM = YOUR_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = YOUR_ACCESS_TOKEN_EXPIRE_MINUTES
```


Note: Use a Gmail App Password if 2FA is enabled.

4. Set Up PostgreSQL: Make sure PostgreSQL is running and create the database:

```bash
CREATE DATABASE job_tracker;
```

Update config.py and alembic.ini if your DB credentials differ.

5. Run Database Migrations

```bash
alembic upgrade head
```

6. Start Redis (for Celery)

On Ubuntu/Debian

```bash
sudo service redis-server start
```

Or via Docker

```bash
docker run -p 6379:6379 redis
```


7. Start Celery Worker

```bash
celery -A celery_worker.celery worker --loglevel=info
```

8. Run the FastAPI Application

```bash
uvicorn main:app --reload
```


## API Endpoints
### Auth & User
POST /register: Register a new user (sends verification email)

POST /token: Obtain JWT access token (login)

GET /verify-email?token=...: Verify user email

### Job Applications
POST /applications/: Create a new job application

GET /applications/: List current user's job applications

GET /applications/{app_id}: Get a specific application

PUT /applications/{app_id}: Update an application

DELETE /applications/{app_id}: Delete an application

All job application endpoints require authentication via Bearer token.
