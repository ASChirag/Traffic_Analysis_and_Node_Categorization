import os
from datetime import timedelta

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    DEBUG = False
    
    # Model paths
    TRAFFIC_MODEL_PATH = 'traffic_analysis_model.pkl'
    NODE_MODEL_PATH = 'node_cat_model.pkl'
    ANOMALY_MODEL_PATH = 'anomaly_detection_model.pkl'
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100 per minute"
    
    # Cache settings
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Model mappings
    PROTOCOL_MAPPING = {'TCP': 0, 'UDP': 1}
    DEVICE_MAPPING = {'router': 0, 'iot': 1, 'server': 2}
    TRAFFIC_CATEGORY_MAPPING = {0: "Normal Traffic", 1: "Malicious Traffic"}
    NODE_CATEGORY_MAPPING = {
        0: "Normal User",
        1: "Server Node",
        2: "Router/Switch",
        3: "IoT Device",
        4: "Malicious Node"
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 