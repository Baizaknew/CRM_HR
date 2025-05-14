# Development of a CRM system for automating and improving the efficiency of recruitment

**Development of a CRM system for automating and improving the efficiency of recruitment** - a project that is designed to automate, simplify, and accelerate employee recruitment. The users are HR managers, recruiters, department heads

## Technology Stack

*   Python 3.10
*   Django 4.2
*   Django REST Framework
*   PostgreSQL
*   Docker(optional)


## Requirements

*   Python 3.10+
*   PostgreSQL 16.4+ (or other configured DB)
*   (Optional) Docker and Docker Compose
*   Redis 5+

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Baizaknew/CRM_HR.git
    cd CRM_HR
    cd backend
    ```

2.  **Set up a virtual environment and install dependencies:**
    *   Create and activate a virtual environment:

        For Linux or macOS

        ```bash
        python -m venv venv
        source venv/bin/activate
        ```

        for windows

        ```
        source venv\Scripts\activate
        ```
    *   Install dependencies:

        ```bash
        pip install -r requirements.txt
        ```

3.  **Preparing for started project**
    *   Create an `.env` file and fill in all the necessary variables. An example can be found in the `env_template` file.
    *   Сreate a database if necessary
    *   Apply database migrations
        ```
        python manage.py migrate
        ```
    *   If necessary, create a superuser
        ```
        python manage.py createsuperuser
        ```

4.  **Running**

    *   To run the development server, execute:

        ```
        python manage.py runserver
        ```

    *   Make sure that the redis server is running
    *   Running celery
        ```
        celery -A core worker -l INFO
        ```

## Environment Variables

Environment variables are used to configure the application. You need to create a `.env` file in the project's root directory (next to `manage.py`). You can copy `env_template` (if it exists) or create the file from scratch using the variables listed below.

| Variable                | Description                                  | Example                              |
|-------------------------|----------------------------------------------|--------------------------------------|
| `SECRET_KEY`            | Django secret key                            | your-secret-key                      |
| `DEBUG`                 | Debug mode (True/False)                      | True                                 |
| `ALLOWED_HOSTS`         | Allowed hosts (comma-separated)              | localhost, 127.0.0.1                 |
| `DB_NAME`               | PostgreSQL database name                     | hireflow_db                          |
| `DB_USER`               | PostgreSQL user                              | postgres                             |
| `DB_PASSWORD`           | PostgreSQL password                          | your-db-password                     |
| `DB_HOST`               | Database host                                | localhost                            |
| `DB_PORT`               | Database port                                | 5432                                 |
| `REDIS_HOST`            | Redis server host                            | localhost                            |
| `REDIS_PORT`            | Redis port                                   | 6379                                 |
| `EMAIL_HOST`            | SMTP server                                  | smtp.gmail.com                       |
| `EMAIL_HOST_USER`       | Sender email address                         | example@gmail.com                    |
| `EMAIL_HOST_PASSWORD`   | Email password or app password               | your-email-password                  |
| `EMAIL_PORT`            | SMTP port                                    | 587                                  |
| `TELEGRAM_BOT_TOKEN`    | Telegram bot API token                       | your-bot-token                       |
| `TELEGRAM_HR_CHAT_ID`   | Telegram HR chat ID                          | your-chat-id                         |
| `FRONTEND_BASE_URL`     | Frontend base url for link in email message  | http://crm-hr.com                    |

---

## API Documentation

API documentation is automatically generated using Swagger UI / Redoc (if configured in DRF). Available URLs (may differ depending on `urls.py` settings):

*   **Swagger UI:** `https://crm-hr/api/swagger/`
*   **Redoc:** `https://crm-hr/api/schema/redoc/`
*   **Admin Panel:** `https://crm-hr/admin`

The documentation describes all available endpoints, required parameters, request and response formats, as well as access rights for each action.
