# WeightWatchr

A modern web application for tracking body weight with animated trend graphs and insights.

## Features

- 📊 Interactive weight tracking dashboard
- 📈 Animated trend graphs with Chart.js
- 📱 Responsive design for mobile and desktop
- 📝 Optional notes for each weight entry
- 🎯 Goal tracking and progress visualization
- 📊 BMI calculation
- 📤 Data export functionality

## Setup Instructions

1. Clone the repository
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
weightwatchr/
├── app.py              # Main application file
├── models.py           # Database models
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
└── templates/         # HTML templates
    ├── base.html
    └── index.html
``` 