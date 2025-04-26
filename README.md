# Development of a CRM system for automating and improving the efficiency of recruitment

**Development of a CRM system for automating and improving the efficiency of recruitment** is a web application built with Django and Django REST Framework, designed to automate and optimize the employee recruitment process within a company. The system provides a structured workflow for creating, approving, and managing vacancies, as well as managing candidates, with clear separation of roles and access rights.

## Table of Contents

*   [Key Features](#key-features)
*   [Technology Stack](#technology-stack)
*   [User Roles](#user-roles)
*   [Main Workflow](#main-workflow)
*   [Requirements](#requirements)
*   [Installation](#installation)
*   [Running](#running)
*   [Environment Variables](#environment-variables)
*   [API Documentation](#api-documentation)

## Key Features

*   **Vacancy Request Management:** Create, edit, approve, reject, and send requests for revision.
*   **Vacancy Management:** Maintain active vacancies, assign recruiters, track statuses.
*   **Candidate Management:** Add candidates to vacancies, track stages (screening, HR interview, technical interview, offer).
*   **Role-Based Access Model:** Clear separation of rights and capabilities for Department Heads, Head of Recruiters, and Recruiters.
*   **Approval Workflow:** Multi-stage process for approving requests before they become active vacancies.
*   **Commenting:** Ability to leave comments when making decisions (approval, rejection, sending for revision).
*   **RESTful API:** Flexible API for interacting with the system and potential integration with other services.
*   **Rich Text Editor:** Use of CKEditor for convenient formatting of requirements and responsibilities in vacancies.

## Technology Stack

*   **Backend:** Python 3.10, Django 4.2, Django REST Framework
*   **Database:** PostgreSQL (or other relational DB)
*   **Dependency Management:** pip, `requirements.txt`
*   **(Optional):** Celery & Redis for background tasks (e.g., notifications)
*   **(Optional):** Docker, Docker Compose for containerization

## User Roles

The system defines the following main roles:

1.  **Department Head:**
    *   Creates "Vacancy Requests".
    *   Sees only their own requests.
    *   Can edit their requests *only* when the status is "Needs Revision".
    *   Can resubmit a request for review after revision.
    *   Participates in candidate screening (approval/rejection with comments).
2.  **Head of Recruiters:**
    *   Sees *all* "Vacancy Requests".
    *   Approves, rejects, or sends requests for revision.
    *   *Cannot* edit the content of the requests.
    *   After approving a request, creates a "Vacancy".
    *   Assigns a Recruiter to an active "Vacancy".
3.  **Recruiter:**
    *   *Does not see* "Vacancy Requests".
    *   Sees and works with assigned "Vacancies".
    *   Adds Candidates to vacancies.
    *   Submits Candidates for screening by the Department Head.
    *   Conducts HR interviews.
    *   Manages Candidate statuses (interview, offer, etc.).

## Main Workflow

1.  **Request:** Department Head creates a `VacancyRequest`.
2.  **Approval:** Head of Recruiters reviews the request:
    *   **Approve:** Request approved. A `Vacancy` is created based on it, recruiter assigned.
    *   **Reject:** Request rejected (with reason). Process ends.
    *   **Send for Revision:** Request returned to the Department Head for revision (with comments).
3.  **Revision (if needed):** Department Head edits the request and resubmits it. Request goes back to step 2.
4.  **Working with Vacancy:** Recruiter receives the assigned `Vacancy`.
5.  **Sourcing and Adding Candidates:** Recruiter sources and adds candidates.
6.  **Screening:** Recruiter submits suitable candidates to the Department Head.
7.  **Department Head Decision:** Department Head approves or rejects candidates (with comments).
8.  **Interviews:** Approved candidates go through interview stages (HR, technical).
9.  **Offer and Closing:** A successful candidate receives an offer, the vacancy is closed.

## Requirements

*   Python 3.10+
*   Pip
*   PostgreSQL 16.4+ (or other configured DB)
*   (Optional) Docker and Docker Compose

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Baizaknew/CRM_HR.git
    cd CRM_HR
    ```

2.  **Set up a virtual environment and install dependencies:**
    *   Create and activate a virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate  # for Linux/macOS
        # or
        venv\Scripts\activate  # for Windows
        ```
    *   Install dependencies:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Next steps:**
    *   Configure environment variables by creating a `.env` file (see [Environment Variables](#environment-variables)).
    *   Apply database migrations (`python manage.py migrate`).
    *   If necessary, create a superuser (`python manage.py createsuperuser`).

## Running

To run the development server, execute:

```bash
python manage.py runserver
```

## Environment Variables

Environment variables are used to configure the application. You need to create a `.env` file in the project's root directory (next to `manage.py`). You can copy `.env.example` (if it exists) or create the file from scratch using the variables listed below.

| Variable              | Description                                                 | Example Value                                   | Required |
| --------------------- | ----------------------------------------------------------- | ----------------------------------------------- | -------- |
| `SECRET_KEY`          | Django secret key.                                          | `'your_very_strong_secret_key_here!@#$'`        | Yes      |
| `DEBUG`               | Django debug mode (`True` for development, `False` in prod) | `True`                                          | Yes      |
| `ALLOWED_HOSTS`       | List of allowed hosts/domains (comma-separated)             | `localhost,127.0.0.1,[your_domain.com]`         | Yes      |
| `DB_NAME`             | Database name                                               | `hire_flow_db`                                  | Yes      |
| `DB_USER`             | Database user                                               | `postgres`                                      | Yes      |
| `DB_PASSWORD`         | Database user password                                      | `'your_db_password'`                            | Yes      |
| `DB_HOST`             | Database server host (address)                              | `localhost`                                     | Yes      |
| `DB_PORT`             | Database server port                                        | `5432`                                          | Yes      |
| `EMAIL_BACKEND`       | Email sending backend (if used)                             | `django.core.mail.backends.smtp.EmailBackend` | No       |
| `EMAIL_HOST`          | SMTP host (if used)                                         | `smtp.example.com`                              | No       |
| `EMAIL_PORT`          | SMTP port (if used)                                         | `587`                                           | No       |
| `EMAIL_USE_TLS`       | Use TLS for SMTP (`True` or `False`)                        | `True`                                          | No       |
| `EMAIL_HOST_USER`     | Username for SMTP authentication                            | `user@example.com`                              | No       |
| `EMAIL_HOST_PASSWORD` | Password for SMTP authentication                            | `'your_email_password'`                         | No       |
| `CORS_ALLOWED_ORIGINS`| List of origins for CORS (frontend URL, comma-separated)    | `http://localhost:3000,http://127.0.0.1:3000` | No       |


## API Documentation

API documentation is automatically generated using Swagger UI / Redoc (if configured in DRF). Available URLs (may differ depending on `urls.py` settings):

*   **Swagger UI:** `http://{YOUR_HOST}/api/swagger/`
*   **Redoc:** `http://{YOUR_HOST}/api/schema/redoc/`

The documentation describes all available endpoints, required parameters, request and response formats, as well as access rights for each action.