

# ERISA Claims Management Dashboard

A full-stack web application built with Django and HTMX that provides a lightweight system for analyzing and managing insurance claims.

[](https://www.python.org/) [](https://www.djangoproject.com/) [](https://htmx.org/)

-----

## ✨ Features

  * **Dynamic UI**: Search, filter, and view claim details without full page reloads, powered by HTMX.
  * **User Authentication**: Secure login system with role-based permissions.
  * **Admin Dashboard**: A staff-only dashboard with key performance indicators and statistics.
  * **Interactive Annotations**: Add notes to claims, flag items for review, and manage workflow.
  * **Data Ingestion**: Custom management command to load initial claims data from CSV files.
  * **Responsive Design**: A clean, two-column layout that is functional on various screen sizes.

-----

## 🚀 Live Demo

A live version of the application is hosted on Render:

**[https://er-challenge.onrender.com](https://er-challenge.onrender.com)**

-----

## 🛠️ Tech Stack

  * **Backend**: Django, Python
  * **Frontend**: HTML, CSS, HTMX, Alpine.js
  * **Database**: SQLite
  * **Deployment**: Gunicorn, Render

-----

## ⚙️ Getting Started

Follow these instructions to set up and run the project on your local machine for development and testing.

### Prerequisites

  * Python 3.10+
  * `pip` and `venv`

### Local Setup & Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd er-challenge
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Load initial claims data from the CSV files:**

    ```bash
    python manage.py load_claims claim_list_data.csv claim_detail_data.csv
    ```

6.  **Create a superuser account for admin access:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000`.

-----

## 👤 Demo Credentials

For demonstration purposes, a sample user account has been created on the live demo site and credentials are mentioned in the Additional Notes in the Submission.