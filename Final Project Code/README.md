# Traffic Analysis System

A Flask-based web application for analyzing network traffic, detecting anomalies, and categorizing network nodes using machine learning models.

## Features

- Traffic Analysis: Classify network traffic as normal or malicious
- Node Categorization: Identify different types of network nodes
- Anomaly Detection: Detect unusual patterns in network traffic
- Real-time Visualization: Display traffic patterns and analysis results
- Model Performance Monitoring: Track and display model metrics

## Project Structure

```
traffic-analysis/
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
├── models/            # ML models and model management
│   └── model_manager.py
├── routes/            # Route handlers
│   └── main.py
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── logs/             # Application logs
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/traffic-analysis.git
cd traffic-analysis
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

## Configuration

The application uses different configuration classes for development, testing, and production environments. Set the `FLASK_CONFIG` environment variable to one of:
- `development`
- `testing`
- `production`

## Running the Application

1. Development mode:
```bash
python app.py
```

2. Production mode:
```bash
gunicorn app:create_app('production')
```

## API Endpoints

- `GET /`: Dashboard with visualizations
- `GET /input_data`: Form for inputting traffic data
- `POST /predict`: Endpoint for making predictions
- `GET /model_report`: Display model performance metrics

## Security Features

- CSRF Protection
- Rate Limiting
- Input Validation
- Secure Cookie Settings
- Error Logging

## Testing

Run tests using pytest:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 