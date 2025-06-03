<h1 align="center">Hi there, I'm Baizak 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

# Development of a CRM system for automating and improving the efficiency of recruitment

**Development of a CRM system for automating and improving the efficiency of recruitment** - a project that is designed to automate, simplify, and accelerate employee recruitment. The users are HR managers, recruiters, department heads

## 🚀 Key Features

| Feature               | Description |
|------------------------|-------------|
| 📝 **Job Requests**       | Submit structured vacancy requests with fields like department, position, and urgency. |
| 🧑‍💼 **Role-Based Access** | Different roles (HR, Recruiter, Manager) see only what they need — nothing more.|
| 👥 **Candidate Tracking** | Full pipeline with custom statuses: *screening → tech interview → HR interview → offer → accepted.* (you can update and add more if you wish) |
| 🗂 **Vacancy Management** | Track and update job openings with statuses like: *taken into work, under consideration, closed.* (you can update and add more if you wish) |
| 🌐 **Source Tracking**    | Track where candidates came from: *LinkedIn, Telegram, job boards, recommendations.. and others* |
| 📎 **File Attachments**   | Store CVs, cover letters, documents per candidate |   

## Technology Stack

* Programming language: Python 3.10+
* Backend: Django 4.2+ , Django REST Framework  
* Database: PostgreSQL 16+
* Task Queue: Celery, Redis 5+  
* Containerization: Docker 23+ , Docker Compose  
* Deployment: Google Cloud Platform (VM), Nginx, Gunicorn  
* Version Control: Git, GitHub  

## 🧱 System Architecture
![image](https://github.com/user-attachments/assets/55596bea-ebaa-4c72-a64d-2366484c2df2)

## 🗄️ Database Diagram
The database is designed using relational principles and normalized structure.  

![image](https://github.com/user-attachments/assets/2ef96726-586b-4523-84ae-b8ce841296ec)
🔗 [Click here to view full interactive ERD](https://dbdiagram.io/d/crm_db_diagram-67f780f34f7afba18411b5f4)

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
| `FRONTEND_BASE_URL`     | Frontend base url for link in email message  | http://crm-hr.site                   |

---

## API Documentation

API documentation is automatically generated using Swagger UI / Redoc (if configured in DRF). Available URLs (may differ depending on `urls.py` settings):

*   **Swagger UI:** `https://crm-hr.site/api/swagger/`
*   **Redoc:** `https://crm-hr.site/api/schema/redoc/`
*   **Admin Panel:** `https://crm-hr.site/admin`

The documentation describes all available endpoints, required parameters, request and response formats, as well as access rights for each action.

## 🎨 UI Prototype (Frontend Preview)

Although the current system is backend-focused, here are mockups of how the frontend interface could look in the future.

![image](https://github.com/user-attachments/assets/ef621c29-fe75-4e6d-9d26-109a3ae6c863)
![image](https://github.com/user-attachments/assets/4ab47bdf-6afd-4bcf-adc0-56798c93f203)
![image](https://github.com/user-attachments/assets/cd3b695c-a1ad-4472-91ce-09eec03d7631)
![image](https://github.com/user-attachments/assets/7530f029-532f-497e-8762-12cc62c3e2fa)
![image](https://github.com/user-attachments/assets/877b89e3-1c8d-443c-8196-46494016eaa4)


## 🔮 Future Plans

| Feature                 | Description                                      |
|-------------------------|--------------------------------------------------|
| 🤖 AI Integration       | Implement AI models to automatically screen and rank candidates based on CV data, job requirements, and historical feedback. |
| 🌐 React Frontend       | Full user interface for HR teams                |
| 🔄 CI/CD Pipeline       | Auto-deploy with GitHub Actions or Gitlab CI    |
| 📈 Analytics Dashboard  | Track HR performance and conversion rates       |
| 📱 Mobile Version       | Lightweight mobile interface                    |
| 🧩 1C / ERP Integration | Connect the system to enterprise tools like 1C for contract processing and onboarding|


## 📫 Contact

Created by **Baizak Zhumaev**  
If you have any questions — feel free to reach out:

📧 [baizak.zhumaev@alatoo.edu.kg](mailto:baizak.zhumaev@alatoo.edu.kg)
