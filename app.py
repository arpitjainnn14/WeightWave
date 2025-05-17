from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_wtf import FlaskForm
from wtforms import FloatField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional, NumberRange
from models import db, WeightEntry, User
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from forms import LoginForm, RegistrationForm
import csv
from io import StringIO
from datetime import datetime
from io import BytesIO
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weightwatchr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# Add context processor for current datetime
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

class WeightEntryForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    weight = FloatField('Weight (kg)', validators=[DataRequired(), NumberRange(min=20, max=300)])
    height = FloatField('Height (m)', validators=[Optional(), NumberRange(min=0.5, max=3.0)])
    note = TextAreaField('Note', validators=[Optional()])
    target_weight = FloatField('Target Weight (kg)', validators=[Optional(), NumberRange(min=20, max=300)])

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Welcome back!', 'success')
            return redirect(next_page or url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Main routes
@app.route('/')
@login_required
def index():
    form = WeightEntryForm()
    entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.date.desc()).all()
    return render_template('index.html', form=form, entries=entries)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    form = WeightEntryForm()
    if form.validate_on_submit():
        entry = WeightEntry(
            date=form.date.data,
            weight=form.weight.data,
            height=form.height.data,
            target_weight=form.target_weight.data,
            note=form.note.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'errors': form.errors})

@app.route('/data')
@login_required
def get_data():
    entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.date.asc()).all()
    return jsonify([{
        'date': entry.date.strftime('%Y-%m-%d'),
        'weight': entry.weight,
        'height': entry.height,
        'target_weight': entry.target_weight,
        'note': entry.note,
        'bmi': entry.calculate_bmi()
    } for entry in entries])

@app.route('/stats')
@login_required
def get_stats():
    entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.date.desc()).all()
    if not entries:
        return jsonify({
            'current_weight': 0,
            'highest_weight': 0,
            'lowest_weight': 0,
            'average_weight': 0,
            'total_entries': 0,
            'weight_change': 0,
            'percent_change': 0
        })

    weights = [entry.weight for entry in entries]
    current_weight = weights[0]
    highest_weight = max(weights)
    lowest_weight = min(weights)
    average_weight = sum(weights) / len(weights)
    total_entries = len(entries)
    
    # Calculate weight change
    if len(weights) > 1:
        weight_change = current_weight - weights[-1]
        percent_change = (weight_change / weights[-1]) * 100
    else:
        weight_change = 0
        percent_change = 0

    return jsonify({
        'current_weight': current_weight,
        'highest_weight': highest_weight,
        'lowest_weight': lowest_weight,
        'average_weight': average_weight,
        'total_entries': total_entries,
        'weight_change': weight_change,
        'percent_change': percent_change
    })

@app.route('/export')
@login_required
def export_data():
    entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.date.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Weight (kg)', 'Height (m)', 'BMI', 'Target Weight (kg)', 'Note'])
    
    for entry in entries:
        writer.writerow([
            entry.date.strftime('%Y-%m-%d'),
            entry.weight,
            entry.height or '',
            entry.calculate_bmi() or '',
            entry.target_weight or '',
            entry.note or ''
        ])
    
    # Create the response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'weightwatchr_export_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True,port=5003) 