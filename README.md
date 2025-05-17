# WeightWave

A modern web application for tracking body weight with animated trend graphs and insights.

## Features

-📊 Interactive Dashboard – Track weight entries over time with a clean interface

-📈 Animated Trend Graphs – Visualize progress using Chart.js

-📝 Daily Notes – Add personal notes to each weight entry

-🎯 Goal Tracking – Set and monitor your weight goals

-🧮 BMI Calculator – Auto-calculate your Body Mass Index

-📤 Data Export – Download your data for personal records

-📱 Responsive UI – Optimized for mobile and desktop

## Setup Instructions

1. Clone the repository
   ```
   git clone https://github.com/arpitjainnn14/weightwave.git
   cd weightwave
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the application:
   ```bash
   flask run
   ```
6. Visit `http://localhost:5003` in your browser

## Tech Stack

- Backend: Python Flask
- Database: SQLite with SQLAlchemy ORM
- Frontend: HTML5, CSS3, JavaScript
- Charts: Chart.js
- Forms: Flask-WTF

## Project Structure

```
weightwave/
├── app.py              # Main Flask application
├── forms.py            # Form classes (Flask-WTF)
├── models.py           # SQLAlchemy models
├── requirements.txt    # Python dependencies
├── static/             # Static assets (CSS, JS, images)
│   ├── css/
│   └── js/
├── templates/          # HTML templates
│   ├── base.html
│   └── index.html
├── migrations/         # Database migration files (Flask-Migrate)
├── instance/           # Instance folder for configs (if any)
└── README.md           # Project documentation
``` 
