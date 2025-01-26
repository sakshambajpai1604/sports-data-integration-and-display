# Strava Activity Dashboard

A Django-based web application to fetch and display recent activities from the Strava API, complete with visualizations and user authentication.

## Features

- OAuth2 Authentication with Strava
- Fetch and display recent activities, including distance, time, and calories
- Visualize activity data with dynamic bar charts using Matplotlib
- Error handling for API failures and invalid tokens

## Prerequisites

1. Python 3.8+
2. Django 4.x
3. A Strava Developer account and API credentials

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/strava-dashboard.git
cd strava-dashboard
```

### 2. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory and add the following:
```bash
CLIENT_ID=your_strava_client_id
CLIENT_SECRET=your_strava_client_secret
REDIRECT_URI=http://localhost:8000/exchange_token
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Run the Server
```bash
python manage.py runserver
```
Visit http://localhost:8000 in your browser.

## Usage
Navigate to the home page and click "Authorize with Strava."
Log in to Strava and authorize the app.
View your recent activities and their visualizations on the dashboard.

## Acknowledgments
Strava API Documentation: https://developers.strava.com

Django Documentation: https://docs.djangoproject.com
