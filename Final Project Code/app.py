from flask import Flask, render_template, request, jsonify
from routes.main import main, init_model_manager, init_limiter
from models.model_manager import ModelManager
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
    
    # Configure app
    app.config.update(
        RATELIMIT_DEFAULT="50 per minute",
        PROTOCOL_MAPPING={
            "tcp": 1,
            "udp": 2,
            "icmp": 3,
            "mqtt": 4,
            "": 0
        },
        DEVICE_MAPPING={
            "router": 1,
            "switch": 2,
            "server": 3,
            "workstation": 4,
            "iot": 5,
            "": 0
        }
    )
    
    # Create and register model manager
    app.model_manager = ModelManager()
    logger.info("Model Manager initialized")
    
    # Register blueprints
    app.register_blueprint(main)
    
    # Initialize rate limiter
    init_limiter(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
