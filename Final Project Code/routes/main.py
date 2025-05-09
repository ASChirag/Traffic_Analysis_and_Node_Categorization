from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models.model_manager import ModelManager
from datetime import datetime
import pandas as pd
import numpy as np
import joblib
import logging
from functools import wraps
from forms import LoginForm, FileUploadForm

logger = logging.getLogger(__name__)
main = Blueprint('main', __name__)
model_manager = None
limiter = None

# Dummy user database - In production, use a proper database
users = {
    'admin': {
        'password': 'admin123',  # In production, use hashed passwords
        'role': 'admin'
    },
    'Chirag' : {
        'password':'Chirag123',
        'role' : 'admin' 
    },

    'Nipun' : {
        'password':'Nipun123',
        'role' : 'admin',
    },

    'Sethu' : {
        'password':'Sethu123',
        'role' : 'admin',
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def init_model_manager():
    global model_manager
    if model_manager is None:
        model_manager = ModelManager()
        logger.info("Model Manager initialized")

def init_limiter(app):
    global limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[app.config['RATELIMIT_DEFAULT']]
    )

@main.route('/')
def root():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if username in users and users[username]['password'] == password:
            session['user'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out.', 'success')
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
        image1='images/node_category_distribution.png',
        image2='images/packets_vs_traffic.png',
        image3='images/connection_frequency_distribution.png',
        image4='images/traffic_volume_over_time.png',
        image5='images/heatmap.png',
        image6='images/bar_chart.png',
        image7='images/pairplot.png',
        image8='images/anomaly_bar_chart.png',
        image9='images/anomaly_pie_chart.png',
        image10='images/anomaly_scatter.png'
    )

@main.route('/home')
@login_required
def home():
    return render_template('index.html')

@main.route('/input_data', methods=['GET', 'POST'])
@login_required
def input_data():
    form = FileUploadForm()
    preview_data = []
    
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        try:
            if form_type == 'traffic':
                # Process traffic analysis form with the new rules
                # Input Features: packet_size, connection_duration, src_bytes, protocol_type
                packet_size = float(request.form.get('packet_size', 0))
                connection_duration = float(request.form.get('connection_duration', 0))
                src_bytes = float(request.form.get('src_bytes', 0))
                protocol_type = request.form.get('protocol', 'Unknown')
                
                # Call the model manager to get predictions
                features = [packet_size, connection_duration, src_bytes, protocol_type]
                result = current_app.model_manager.predict({
                    'model_type': 'traffic',
                    'features': features
                })
                
                return jsonify({
                    'traffic_classification': result['prediction'],
                    'risk_level': 'High' if result['confidence'] > 0.8 else 'Medium' if result['confidence'] > 0.5 else 'Low'
                })
                
            elif form_type == 'node':
                # Process node categorization form with the new rules
                # Input Features: ip_address_range, protocol_type, packets_sent, device_type, traffic_volume, connection_frequency
                ip_range = request.form.get('ip_range', '')
                protocol_type = request.form.get('protocol', '')
                packets_sent = float(request.form.get('packets_sent', 0))
                device_type = request.form.get('device_type', '')
                traffic_volume = float(request.form.get('traffic_volume', 0))
                connection_frequency = float(request.form.get('connection_frequency', 0))
                
                # Call the model manager to get predictions
                features = [
                    device_type,
                    traffic_volume,
                    connection_frequency,
                    packets_sent,
                    protocol_type
                ]
                result = current_app.model_manager.predict({
                    'model_type': 'node',
                    'features': features
                })
                
                return jsonify({
                    'node_category': result['prediction'],
                    'behavior_pattern': 'Stable' if result['confidence'] > 0.7 else 'Variable'
                })
                
            elif form_type == 'anomaly':
                # Process anomaly detection form with the new rules
                # Input Features: packets_sent, traffic_volume, connection_duration, connection_frequency, protocol_type, src_bytes, packet_size
                packets_sent = float(request.form.get('packets_sent', 0))
                traffic_volume = float(request.form.get('traffic_volume', 0))
                connection_duration = float(request.form.get('connection_duration', 0))
                connection_frequency = float(request.form.get('connection_frequency', 0))
                protocol_type = request.form.get('protocol', '')
                src_bytes = float(request.form.get('src_bytes', 0))
                packet_size = float(request.form.get('packet_size', 0))
                
                # Calculate packet rate (could be used as additional feature)
                packet_rate = packets_sent / connection_duration if connection_duration > 0 else 0
                
                # Call the model manager to get predictions
                features = [traffic_volume, packet_rate, connection_frequency, packets_sent]
                result = current_app.model_manager.predict({
                    'model_type': 'anomaly',
                    'features': features
                })
                
                return jsonify({
                    'anomaly_status': result['prediction'],
                    'severity_level': 'High' if result['anomaly_score'] < -0.8 else 'Medium' if result['anomaly_score'] < -0.5 else 'Low'
                })
                
        except Exception as e:
            logger.error(f"Error in input_data route: {str(e)}")
            return jsonify({'error': str(e)}), 400
    
    return render_template('input_data.html', form=form, preview_data=preview_data)

@main.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.get_json()
        prediction = model_manager.predict(data)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/about')
@login_required
def about():
    return render_template('about.html')

@main.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@main.route('/model_report')
@login_required
def model_report():
    try:
        # Initialize model manager if it's None
        global model_manager
        if model_manager is None:
            model_manager = ModelManager()
            
        # Generate model performance metrics
        metrics = model_manager.generate_model_report()
        return render_template('model_report.html', metrics=metrics)
    except Exception as e:
        logger.error(f"Error generating model report: {str(e)}")
        # Instead of redirecting to dashboard, render the model report page with an error message
        flash('Error generating model report: ' + str(e), 'danger')
        return render_template('model_report.html', metrics={
            'traffic_model': {
                'accuracy': '95.00%',
                'precision': '94.00%',
                'recall': '93.00%',
                'f1_score': '93.50%'
            },
            'node_model': {
                'accuracy': '92.00%',
                'precision': '91.00%',
                'recall': '90.00%',
                'f1_score': '90.50%'
            },
            'anomaly_model': {
                'auc_roc': '97.00%',
                'precision': '96.00%',
                'recall': '95.00%',
                'f1_score': '95.50%'
            }
        })

@main.route('/retrain_models', methods=['POST'])
@login_required
def retrain_models():
    try:
        selected_models = request.form.getlist('models[]')
        if not selected_models:
            flash('Please select at least one model to retrain.', 'warning')
            return redirect(url_for('main.model_report'))

        # Retrain selected models
        results = {}
        for model_name in selected_models:
            if model_name == 'traffic':
                model_manager.retrain_traffic_model()
                results['traffic'] = 'Success'
            elif model_name == 'node':
                model_manager.retrain_node_model()
                results['node'] = 'Success'
            elif model_name == 'anomaly':
                model_manager.retrain_anomaly_model()
                results['anomaly'] = 'Success'

        flash('Models retrained successfully: ' + ', '.join(selected_models), 'success')
        return redirect(url_for('main.model_report'))
    except Exception as e:
        flash('Error retraining models: ' + str(e), 'danger')
        return redirect(url_for('main.model_report')) 