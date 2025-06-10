# MatkaMestre

**MatkaMestre** is a web platform designed to support and streamline mentorship journeys through dedicated dashboards for both mentors and mentees. It offers intuitive tools to manage tasks, schedule meetings, share resources, and track progress. Mentees join the platform through personalized invitations from their mentors, with each invitation link valid for 24 hours to ensure a secure and timely onboarding experience.


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Django Admin Access](#django-admin-access)
- [User Journey](#user-journey)
- [Docker Configuration](#docker-configuration)
- [License](#license)


## Overview

This platform streamlines effective collaboration and progress tracking between mentors and mentees. Mentors onboard new mentees through a secure invitation system, where each registration link automatically expires after 24 hours. Once connected, mentors can efficiently oversee their assigned mentees, manage availability, and assign tasks, while mentees track their progress, book meetings, and access shared resources.


## Features

The MatkaMestre Platform offers core functionalities for streamlined mentor-mentee interaction:

* **User Roles & Authentication:** Secure registration, login, and logout for both Mentors and Mentees.
* **Mentee Invitation System:** Mentors invite new mentees, who will receive an email with a unique registration link.
* **Profile Customization:**
    * **Profile Pictures:** Both mentors and mentees can upload and display a profile picture.
    * **Professional Description (Bio):** Mentors and mentees can add a personal or professional description (bio) to their profiles.
* **Mentor Dashboard:** Mentors get an overview of their assigned mentees, including their current business stage, pending tasks status, and upcoming scheduled meetings.
* **Mentee Profile View:** Mentors can view detailed profiles of individual mentees, including their bio, assigned tasks, and past meeting recordings.
* **Task Management:**
    * **Mentor:** Create, edit, and delete tasks for specific mentees.
    * **Mentee:** View their assigned tasks and mark them as completed.
    * **Task Status Tracking:** Mentors can see at a glance if a mentee has pending tasks.
* **Availability & Meeting Scheduling:**
    * **Mentor:** Set and manage their available time slots for meetings.
    * **Mentee:** View their assigned mentor's available slots and book meetings.
* **Meeting Recordings:**
    * **Mentor:** Upload video recordings of meetings, associating them with specific mentees.
    * **Mentor & Mentee:** View meeting recordings, grouped by mentee for easy navigation.
* **User Account Management:** Users can edit their email/password and delete their accounts.




## Technologies Used

This project is built as a monolithic Django application, utilizing standard Django templating for the frontend and Docker for containerization.


### Backend

* **Language:** [Python](https://docs.python.org/3.12/) – High-level programming language used for backend logic.
* **Framework:** [Django](https://docs.djangoproject.com/en/5.2/) – High-level Python web framework that encourages rapid development and clean, pragmatic design.
* **Configuration Management:** [Python Decouple](https://pypi.org/project/python-decouple/) – Separates configuration settings from source code using environment variables.
* **Database:** [SQLite3](https://www.sqlite.org/docs.html) – Lightweight file-based relational database used for local development and testing.
* **Database Schema Visualization:** [Django Schema Viewer](https://pypi.org/project/django-schema-viewer/) – Visualizes Django model relationships and database structure interactively.


### Frontend

* **Templating:** [Django Template Language](https://docs.djangoproject.com/en/5.2/ref/templates/language/) – Python-agnostic templating system for rendering dynamic HTML.
* **Styling:** [Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite) – Utility-first CSS framework for rapid and responsive UI design.


### DevOps

* **Docker:** [Docker](https://docs.docker.com/get-started/) – Containerization platform to isolate backend and frontend environments.
* **Docker Compose:** [Docker Compose](https://docs.docker.com/compose/) – Tool for defining and running multi-container Docker applications using a single configuration file.



## Project Structure

```
MatkaMestre/
├── accounts/               # User authentication, custom user model, and user profiles:
│   ├── models.py            (CustomUser, MentorProfile, MenteeProfile, InvitationToken)
│   ├── views.py
│   ├── urls.py
│   └── ...
├── core/                   # Core functionalities, common settings, and main URL configurations for the Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py             # If applicable for async features
│   └── ...
├── media/                  # Directory for user-uploaded files (e.g., profile pictures, meeting recordings)
├── mentee/                 # Mentee-specific application logic and views (e.g., task viewing, slot booking, recording access)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── mentor/                 # Mentor-specific application logic and views (e.g., task management, availability, recording uploads)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── static/                 # Collected static files (CSS, JavaScript, images) used by Django
├── templates/              # Project-wide base HTML templates
├── venv/                   # Python virtual environment (ignored by Git)
├── .env                    # Environment variables for Docker and Django settings (local only)
├── .gitignore              # Specifies intentionally untracked files to ignore by Git
├── db.sqlite3              # SQLite database file (for local development, tracked by Git due to bind mount)
├── docker-compose.yml      # Docker Compose configuration for defining and running the application services
├── Dockerfile              # Dockerfile for building the main Django application container
├── manage.py               # Django's command-line utility for administrative tasks
├── README.md               # This project's documentation file
└── requirements.txt        # Python dependency list for the project
```


## Prerequisites

Before running FreudLens, make sure you have:

- **Docker** and **Docker Compose** installed
- **GitHub** - https://github.com


## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/xxx/MatkaMestre.git](https://github.com/xxx/MatkaMestre.git)
   cd MatkaMestre
   ```

2. **Set up environment variables** (see [Configuration](#configuration) section)


3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

## Configuration

### Backend Environment Variables

Create a `.env` file in the root of your project with the following variables:

```env
# Django Setup
SECRET_KEY=your_django_secret_key_here       # Generate a strong, unique key for production
DEBUG=True                                   # Set to False for production
ALLOWED_HOSTS=localhost,127.0.0.1            # Or your development host, e.g., your WSL IP

# Database (SQLite3 for local development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# EMAIL SETUP
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend   # Use console backend for development
DEFAULT_FROM_EMAIL=no-reply@matkamestre.com 
SERVER_EMAIL=errors@matkamestre.com 
```



## Running the Application

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```


After starting the services will run on:
- **Application**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin/
- **Database Schema Visualization**: http://127.0.0.1:8000/schema-viewer/



## Django Admin Access

To access the Django administration panel, you first need to create a superuser account.

1.  **Create a Superuser:**
    Execute the following command in your terminal:
    ```bash
    docker-compose exec backend python manage.py createsuperuser
    ```
    Follow the prompts to set up your username, email and password.

2.  **Access Admin Panel:**
    Once the superuser is created, navigate to the following URL in your web browser:
    * **Django Admin**: `http://localhost:8000/admin/`




## User Journey

### Mentor Experience
1.  **Login:** Mentor logs into their account.
2.  **Mentee Invitation & Onboarding:**
    * The **only way for a mentee to register is via an invitation from a mentor.**
    * Mentors can invite new mentees, who will receive an email with a unique registration link.
    * This process allows mentors to build their network of mentees displayed on their dashboard.
3.  **Profile Customization:** Mentors can create their professional description (bio) and upload a profile picture.
4.  **Dashboard:** Accesses a personalized dashboard displaying an overview of their assigned mentees, including their business stage, pending tasks status, and upcoming scheduled meetings.
5.  **Mentee Profile View:** Can click on a specific mentee to view their detailed profile, including their bio, a list of assigned tasks, and all meeting recordings related to that mentee.
6.  **Task Management:** Create, edit, and delete tasks for assigned mentees.
7.  **Availability Management:** Set and manage their available time slots for new meetings.
8.  **Recording Upload:** Upload video recordings of completed meetings.


### Mentee Experience
1.  **Registration (via Invitation) & Login:** Mentee registers using a unique invitation link from their mentor, and then logs into their account.
2.  **Profile Customization:** Mentees can create their professional description (bio) and upload a profile picture.
3.  **Mentor Profile View:** Can view the profile of their assigned mentor, including their name, email, and bio.
4.  **Task Management:** View all tasks assigned by their mentor.
5.  **Task Completion:** Mark assigned tasks as completed.
6.  **Meeting Booking:** View their assigned mentor's available time slots and book a meeting.
7.  **Recording Access:** Access and view all meeting recordings they are associated with.



## Docker Configuration
This project uses a single Docker container for the Django backend, managing all application logic and database interactions (SQLite).

1. **Dockerfile:** Defines the build process for the Django application container.
2. **docker-compose.yml:** Orchestrates the single Django service for easy local setup and execution.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



